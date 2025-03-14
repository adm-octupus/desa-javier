/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class OttPaqtanaWorkspaceListController extends ListController {
    setup() {
        super.setup();
        this.action = useService("action");
        this.orm = useService("orm");
    }

    async onClickSyncWorkspace() {
        const action = await this.orm.call("ott.paqtana.workspace", "action_sync_workspace", []);
        if (action) {
            await this.action.doAction(action);
        }
        await this.model.load();  // recarga la lista después
    }
}

export const ottPaqtanaWorkspaceTreeView = {
    ...listView,
    Controller: OttPaqtanaWorkspaceListController,
    buttonTemplate: "OttPaqtanaWorkspaceListController.Buttons",
};

registry.category("views").add("ott_paqtana_workspace_tree", ottPaqtanaWorkspaceTreeView);
