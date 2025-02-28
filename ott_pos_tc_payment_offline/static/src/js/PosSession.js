/** @odoo-module **/
//    Extend POS global state
var { PosGlobalState, Order } = require('point_of_sale.models');
var { Payment, Order } = require('point_of_sale.models');
const Registries = require('point_of_sale.Registries');

const NewPosGlobalState = (PosGlobalState) => class NewPosGlobalState extends PosGlobalState {
    async _processData(loadedData) {
      await super._processData(...arguments);
      this.card_red_list = loadedData['ott.card.red'];
      this.card_brand_list = loadedData['ott.card.brand'];
      this.card_type_list = loadedData['ott_card_type'];
      this.card_payment_terms_list = loadedData['ott_card_payment_terms'];
      this.card_period_list = loadedData['ott.card.period'];
    }
}

const NewPayment = (Payment) => class NewPayment extends Payment {
  constructor(obj, options) {
    super(obj, options);
    this.ott_card_red_id = options.ott_card_red_id || null;
    this.ott_card_brand_id = options.ott_card_brand_id || null;
    this.ott_card_type = options.ott_card_type || null;
    this.ott_card_payment_terms = options.ott_card_payment_terms || null;
    this.ott_card_period_id = options.ott_card_period_id || null;
  }

  init_from_JSON(json) {
    super.init_from_JSON(json);
    this.ott_card_red_id = json.ott_card_red_id;
    this.ott_card_brand_id = json.ott_card_brand_id;
    this.ott_card_type = json.ott_card_type;
    this.ott_card_payment_terms = json.ott_card_payment_terms;
    this.ott_card_period_id = json.ott_card_period_id;
  }

  export_as_JSON() {
    const json = super.export_as_JSON();
    json.ott_card_red_id = this.ott_card_red_id;
    json.ott_card_brand_id = this.ott_card_brand_id;
    json.ott_card_type = this.ott_card_type;
    json.ott_card_payment_terms = this.ott_card_payment_terms;
    json.ott_card_period_id = this.ott_card_period_id;
    return json;
  }

}


Registries.Model.extend(PosGlobalState, NewPosGlobalState);
Registries.Model.extend(Payment, NewPayment);
