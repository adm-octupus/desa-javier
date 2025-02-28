odoo.define('l10n_ec_edi_pos.PartnerDetailsEdit', function (require) {
    'use strict';

    const { _t } = require('web.core');
    const PartnerDetailsEdit = require('point_of_sale.PartnerDetailsEdit');
    const Registries = require('point_of_sale.Registries');

    const ExtendedPartnerDetailsEdit = (PartnerDetailsEdit) =>
        class extends PartnerDetailsEdit {

            setup() {
                super.setup();
                this.intFields.push("l10n_latam_identification_type_id");
                const partner = this.props.partner;
                this.changes.l10n_latam_identification_type_id = partner.l10n_latam_identification_type_id && partner.l10n_latam_identification_type_id[0]
            }

            trigger(event, payload) {
                // Interceptamos el evento "save-changes" para validar los campos obligatorios.
                if (event === "save-changes") {
                    const processedChanges = payload.processedChanges;
                    if (!processedChanges.l10n_latam_identification_type_id || processedChanges.l10n_latam_identification_type_id === "" || processedChanges.l10n_latam_identification_type_id === "None") {
                        return this.showPopup("ErrorPopup", {
                            title: _t("Missing Required Field"),
                            body: _t("Please fill in the mandatory field: Type ID"),
                        });
                    }else if (!processedChanges.vat || processedChanges.vat === "") {
                        return this.showPopup("ErrorPopup", {
                            title: _t("Missing Required Field"),
                            body: _t("Please fill in the mandatory field: ID"),
                        });
                    }else if (!processedChanges.email || processedChanges.email === "") {
                        return this.showPopup("ErrorPopup", {
                            title: _t("Missing Required Field"),
                            body: _t("Please fill in the mandatory field: Email"),
                        });
                    }

                }
                return super.trigger(event, payload);
            }

        };

    Registries.Component.extend(PartnerDetailsEdit, ExtendedPartnerDetailsEdit);

    return ExtendedPartnerDetailsEdit;
});

