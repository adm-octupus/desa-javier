odoo.define('ott_pos_tc_payment_offline.PaymentScreen', function (require) {
    'use strict';

    const { _t } = require('web.core');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { onRendered } = owl;
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { useState, useRef } = owl;

    _t("Card Credit");
    _t("Card Debit");
    _t("Deferred");
    _t("Immediate");

    const ExtendedPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {

            setup() {
                super.setup();
                this.card_red_list = this.env.pos.card_red_list || [];
                this.card_brand_list = this.env.pos.card_brand_list || [];     
                this.card_type_list = this.env.pos.card_type_list || [];
                this.card_payment_terms_list = this.env.pos.card_payment_terms_list || [];
                this.card_period_list = this.env.pos.card_period_list || [];
            
                this.state = useState({
                    ott_card_red_id: this.selectedPaymentLine?.ott_card_red_id ?? null,
                    ott_card_brand_id: this.selectedPaymentLine?.ott_card_brand_id ?? null,
                    ott_card_type: this.selectedPaymentLine?.ott_card_type ?? null,
                    ott_card_payment_terms: this.selectedPaymentLine?.ott_card_payment_terms ?? null,
                    ott_card_period_id: this.selectedPaymentLine?.ott_card_period_id ?? null,
                });

            }

            selectPaymentLine(event) {     
                super.selectPaymentLine(event);
                this.state.ott_card_red_id = this.selectedPaymentLine?.ott_card_red_id;  
                this.state.ott_card_brand_id = this.selectedPaymentLine?.ott_card_brand_id; 
                this.state.ott_card_type = this.selectedPaymentLine?.ott_card_type;           
                this.state.ott_card_payment_terms = this.selectedPaymentLine?.ott_card_payment_terms; 
                this.state.ott_card_period_id = this.selectedPaymentLine?.ott_card_period_id;           
            }

            addNewPaymentLine({ detail: paymentMethod }) {
                const result = super.addNewPaymentLine({ detail: paymentMethod });
                this.state.ott_card_red_id = null;  
                this.state.ott_card_brand_id = null;  
                this.state.ott_card_type = null;  
                this.state.ott_card_payment_terms = null;  
                this.state.ott_card_period_id = null;  
                return result;
            }

            isCreditCard(){
                const paymentMethod = this.selectedPaymentLine?.payment_method;
                if (paymentMethod && paymentMethod.is_credit_card) {
                    return true;
                }else{
                    return false;
                }
            }

            getCardRedList() {
                return this.card_red_list;
            }

            getCardBrandsForPaymentMethod() {
                const paymentMethod = this.selectedPaymentLine?.payment_method;
            
                if (!paymentMethod || !paymentMethod.ott_card_brands_ids) {
                    return [];
                }
                const card_brand_list = this.env.pos.card_brand_list || [];
                const data = paymentMethod.ott_card_brands_ids.map(id => {
                    return card_brand_list.find(brand => brand.id === id);
                }).filter(brand => brand);
    
                return data;

            }

            getCardTypeList() {
                return this.card_type_list.map(type => ({
                    ...type,
                    name: _t(type.name)
                }));
            }

            getCardPaymentTermsList() {
                return this.card_payment_terms_list.map(term => ({
                    ...term,
                    name: _t(term.name)
                }));
            }
            
            getCardPeriodList() {
                return this.card_period_list;
            }
            
            onCardRedChange(event) {
                this.handleComboChange(event, 'ott_card_red_id', this.card_red_list, true);
            }
            
            onCardBrandChange(event) {
                this.handleComboChange(event, 'ott_card_brand_id', this.card_brand_list, true);
            }
            
            onCardTypeChange(event) {
                this.handleComboChange(event, 'ott_card_type', this.card_type_list);
                if (!this.state.ott_card_type || this.state.ott_card_type === "debit") {
                    this.selectedPaymentLine.ott_card_payment_terms = null;
                    this.selectedPaymentLine.ott_card_period_id = null;
                    this.state.ott_card_payment_terms = null;
                    this.state.ott_card_period_id = null;
                }
            }
            
            onCardPaymentTermsChange(event) {
                this.handleComboChange(event, 'ott_card_payment_terms', this.card_payment_terms_list);
                if (!this.state.ott_card_payment_terms || this.state.ott_card_payment_terms === "deferred") {
                    this.selectedPaymentLine.ott_card_period_id = null;
                    this.state.ott_card_period_id = null;
                }
            }
            
            onCardPeriodChange(event) {
                this.handleComboChange(event, 'ott_card_period_id', this.card_period_list, true);
            }
            
            handleComboChange(event, fieldKey, list, parseAsInt = false) {
                let value = event.target.value;
                if (parseAsInt) {
                    value = parseInt(value);
                }
                const selected = list.find(item => item.id === value);
                if (this.selectedPaymentLine && selected) {
                    this.selectedPaymentLine[fieldKey] = selected.id;
                    this.state[fieldKey] = selected.id;
                } else {
                    this.selectedPaymentLine[fieldKey] = null;
                    this.state[fieldKey] = null;
                }
            }
            
            validateCardFields() {

                const alwaysRequired = [
                    { key: 'ott_card_red_id', label: _t("Card Red") },
                    { key: 'ott_card_brand_id', label: _t("Card Brand") },
                    { key: 'ott_card_type', label: _t("Card Type") },
                ];
            
                let missingFields = [];
            
                this.paymentLines.forEach((line) => {
                    if (line.payment_method && line.payment_method.is_credit_card) {
    
                        alwaysRequired.forEach((field) => {
                            if (!line[field.key] || line[field.key] === "") {
                                missingFields.push(field.label);
                            }
                        });
            
                        if (line.ott_card_type === 'credit' && (!line.ott_card_payment_terms || line.ott_card_payment_terms === "")) {
                            missingFields.push(_t("Card Payment Terms"));
                        } else if (line.ott_card_payment_terms === 'deferred' && (!line.ott_card_period_id || line.ott_card_period_id === "")) {
                            missingFields.push(_t("Card Period"));
                        }
                    }
                });
            
                // Eliminamos duplicados
                return [...new Set(missingFields)];
            }
            
            
            validateOrder(isForceValidate) {
                const missingFields = this.validateCardFields();
                if (missingFields.length) {
                    const message = _t("Please complete the following fields for credit card payments: ") + missingFields.join(', ');
                    this.showPopup('ErrorPopup', {
                        title: _t('Missing Required Fields'),
                        body: message,
                    });
                    return false;
                }
                return super.validateOrder(isForceValidate);
            }


        };

    ExtendedPaymentScreen.template = 'ott_pos_tc_payment_offline.PaymentScreen';
    Registries.Component.extend(PaymentScreen, ExtendedPaymentScreen);

    return ExtendedPaymentScreen;
});