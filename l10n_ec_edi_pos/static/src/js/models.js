/** @odoo-module **/
var { PosGlobalState, Order } = require('point_of_sale.models');
const Registries = require('point_of_sale.Registries');

const NewPosGlobalState = (PosGlobalState) => class NewPosGlobalState extends PosGlobalState {
  async _processData(loadedData) {
    await super._processData(...arguments);
    this.final_consumer = loadedData['final_consumer']
    this.final_consumer_id = loadedData['final_consumer_id']
    this.l10n_latam_identification_type = loadedData['l10n_latam.identification.type'];
  }

  isDefaultCreateInvoceActive() {
    return this.config.ott_default_create_invoice
  }

  isEcuadorianCompany() {
      return this.company.country?.code == "EC";
  }

  get_final_consumer() {
      return this.final_consumer;
  }

  get_final_consumer_id() {
    return this.final_consumer_id;
  }

}

const NewOrder = (Order) => class NewOrder extends Order {
  constructor(obj, options) {
    super(obj, options);

    if (this.pos.isEcuadorianCompany() && this.pos.isDefaultCreateInvoceActive()) {
      this.set_to_invoice(true);
    }
  
    if (!this.partner) {
      this.partner = this.pos.get_final_consumer();
    }
    
  }

  _isRefundOrder() {
    const lines = this.get_orderlines();
    if (lines.length > 0 && lines[0].refunded_orderline_id) {
        return true;
    }
    return false;
  }

}

Registries.Model.extend(PosGlobalState, NewPosGlobalState);
Registries.Model.extend(Order, NewOrder);
