odoo.define('ott_pos_tc_payment_offline.CashOpeningPopup', function (require) {
    'use strict';

    const { _t } = require('web.core');
    const CashOpeningPopup = require('point_of_sale.CashOpeningPopup');
    const Registries = require('point_of_sale.Registries');
    const { useState } = owl;

    const ExtendedCashOpeningPopup = (CashOpeningPopup) =>
        class extends CashOpeningPopup {

            setup() {
                super.setup();
                this.state.lotMedianet = "";
                this.state.lotDatafast = "";
            }

            openDetailsPopup() {
                super.openDetailsPopup();
                this.state.lotMedianet = "";
                this.state.lotDatafast = "";
            }

        };

    // ExtendedCashOpeningPopup.template = 'ott_pos_tc_payment_offline.CashOpeningPopup';
    Registries.Component.extend(CashOpeningPopup, ExtendedCashOpeningPopup);

    return ExtendedCashOpeningPopup;

});