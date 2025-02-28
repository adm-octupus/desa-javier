odoo.define('l10n_ec_edi_pos.PaymentScreen', function (require) {
    'use strict';

    const { _t } = require('web.core');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const ExtendedPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            async _isOrderValid(isForceValidate) {
                if (this.env.pos.isEcuadorianCompany()) {
                    if (this.currentOrder._isRefundOrder() && this.currentOrder.get_partner().id === this.env.pos.get_final_consumer_id()) {
                        this.showPopup('ErrorPopup', {
                            title: _t('Refund not possible'),
                            body: _t('You cannot refund orders for Consumidor Final.'),
                        });
                        return false;
                    }
                }
                return super._isOrderValid(...arguments);
            }

            shouldDownloadInvoice() {
                return this.env.pos.isEcuadorianCompany() ? false : super.shouldDownloadInvoice();
            }
            
        };

    Registries.Component.extend(PaymentScreen, ExtendedPaymentScreen);

    return ExtendedPaymentScreen;
});

