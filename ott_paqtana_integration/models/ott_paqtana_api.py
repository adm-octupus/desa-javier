# -*- coding: utf-8 -*-
import json
import requests
from odoo import models, api, fields, _

class OttPaqtanaAPIValueError(ValueError):

    def __init__(self, type, message, data=None):
        self.type = type
        self.message = message
        self.data = data
        super().__init__(f"{self.type}: {self.message}")

    def get_json(self):
        return json.loads(self.data) if self.data else None


class OttPaqtanaAPI(models.AbstractModel):
    _name = 'ott.paqtana.api'
    _description = 'API Paqtana Integration'
    _auto = False

    TYPE_INFO = 'info'
    TYPE_SYNC = 'sync'
    TYPE_WARNING = 'warning'
    TYPE_ERROR = 'error'
    TYPE_CRITICAL = 'critical'

    def _log_error(self, company, error, json=None):
        ott_paqtana_log_enabled = company.ott_paqtana_log_enabled
        if ott_paqtana_log_enabled and error:
            self.env['ott.paqtana.error'].create({'company_id': company.id, 'error_type': error.type, 'error_message': error.message, 'json_data': self.save_json_to_db(json)})

    def _log_info(self, company, message, json=None):
        ott_paqtana_log_enabled = company.ott_paqtana_log_enabled
        if ott_paqtana_log_enabled and message:
            self.env['ott.paqtana.error'].create({'company_id': company.id, 'error_type': self.TYPE_INFO, 'error_message': message, 'json_data': self.save_json_to_db(json)})

    def save_json_to_db(self, json_string):
        try:
            if json_string:
                json_data = json.loads(json_string) if isinstance(json_string, str) else json_string
                formatted_json = json.dumps(json_data, indent=4, ensure_ascii=False)
                return formatted_json
            return None

        except json.JSONDecodeError as error:
            raise OttPaqtanaAPIValueError(
                self.TYPE_CRITICAL, 
                _("Error processing JSON: %s") % (error), 
                json_string
            )


    def _execute_paqtana_request(self, company, method, url, json=None, **kwargs):
        """
        Método centralizado para realizar solicitudes HTTP a Paqtana con autenticación basada en token.
        `method` es la función de requests (post, patch, get, etc.).
        """
        response = None
        try:
            self._log_info(company, _('URL: %s') % url)
            self._log_info(company, _('method: %s') % method)
            if json:
                self._log_info(company, _('Json'), json)
            
            paqtana_token = company.ott_paqtana_token
            if not paqtana_token:
                raise OttPaqtanaAPIValueError(
                    self.TYPE_CRITICAL, 
                    _("Authentication error: No Paqtana token found. Please configure the API token."), 
                    json
                )

            default_headers = {
                "Authorization": f"Bearer {paqtana_token}",
                "Content-Type": "application/json",
            }

            connect_timeout = company.ott_paqtana_connect_timeout
            read_timeout = company.ott_paqtana_read_timeout
            verify = company.ott_paqtana_use_checked_ssl

            response = method(
                url, 
                headers=default_headers, 
                json=json, 
                timeout=(connect_timeout, read_timeout), 
                verify=verify, 
                **kwargs
            )

            response.raise_for_status()
            return response

        except requests.exceptions.ConnectionError:
            raise OttPaqtanaAPIValueError(
                self.TYPE_CRITICAL, 
                _("Connection error: Could not connect to Paqtana server. Please check your network connection or the server status."), 
                json
            )
        except requests.exceptions.Timeout:
            raise OttPaqtanaAPIValueError(
                self.TYPE_CRITICAL, 
                _("Timeout error: The request to Paqtana server timed out. Please try again later."), 
                json
            )
        except requests.exceptions.HTTPError as http_err:
            try:
                error_response = response.json()  # Convertir a JSON
                error_code = error_response.get("operation_type", "Unknown operation")
                validation_error = error_response.get("operation_info", {}).get("validation_error", "Unknown error")
                file_type = error_response.get("operation_info", {}).get("file_type", "Unknown file type")
                error_message = f"Operation: {error_code} | Validation: {validation_error} | File Type: {file_type}"
            except (ValueError, KeyError):
                error_message = f"HTTP error occurred: {http_err}"
                raise OttPaqtanaAPIValueError(self.TYPE_CRITICAL,error_message, json)
            raise OttPaqtanaAPIValueError(
                self.TYPE_CRITICAL, 
                _("Paqtana Error %s: %s" % (error_code, error_message)), 
                json
            )
        except requests.exceptions.RequestException as req_err:
            raise OttPaqtanaAPIValueError(
                self.TYPE_CRITICAL, 
                _("Request error: %s" % req_err), 
                json
            )
        except Exception as e:
            raise OttPaqtanaAPIValueError(
                self.TYPE_CRITICAL, 
                _("An unexpected error occurred: %s" % str(e)), 
                json
            )