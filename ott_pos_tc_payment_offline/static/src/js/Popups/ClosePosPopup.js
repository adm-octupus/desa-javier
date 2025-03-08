odoo.define('ott_pos_tc_payment_offline.ClosePosPopup', function (require) {
    'use strict';

    const { _t } = require('web.core');
    const ClosePosPopup = require('point_of_sale.ClosePosPopup');
    const Registries = require('point_of_sale.Registries');
    const { useState } = owl;

    const ExtendedClosePosPopup = (ClosePosPopup) =>
        class extends ClosePosPopup {

            setup() {
                super.setup();
            }

            openDetailsPopup() {
                super.openDetailsPopup();
                this.state.lotMedianet = "";
                this.state.lotDatafast = "";
            }

            async confirm() {
                const response = await this.rpc({
                    model: 'pos.session',
                    method: 'validate_card_red_lot_session_close',
                    args: [this.env.pos.pos_session.id, this.state.lotMedianet, this.state.lotDatafast]
                })

                if (!response.successful) {
                    await this.showPopup('ErrorPopup', {title: _t('Red batch record error'), body: response.message});
                    return;
                } else {
                    await super.confirm();
                }
            }



            async closeSession() {
                await super.closeSession();

                // await this.rpc({
                //     model: 'pos.session',
                //     method: 'validate_card_red_lot_record_session_close',
                //     args: [this.env.pos.pos_session.id, this.state.lotMedianet, this.state.lotDatafast]
                // })


                await this.rpc({
                    model: 'pos.session',
                    method: 'close_session_tc_payment_offline_from_ui',
                    args: [this.env.pos.pos_session.id, this.state.lotMedianet, this.state.lotDatafast],
                });
            }



        };

    // ExtendedClosePosPopup.template = 'ott_pos_tc_payment_offline.ClosePosPopup';
    Registries.Component.extend(ClosePosPopup, ExtendedClosePosPopup);

    return ExtendedClosePosPopup;

});