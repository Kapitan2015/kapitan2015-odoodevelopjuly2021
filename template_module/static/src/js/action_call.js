// alert("TEST1");
odoo.define('template_module.action_call', function (require) {

    "use strict";       
    var core = require('web.core');
    var ListView = require('web.ListView'); 
    var ListController = require("web.ListController");
    
    var includeDict = {
        renderButtons: function () {
            this._super.apply(this, arguments);
            if (this.modelName === "muki.rest") {
                var your_btn = this.$buttons.find('button.oe_action_button')
                your_btn.on('click', this.proxy('oe_action_button'))
            }
        },
        oe_action_button: function(){
            this.do_action({
                type: "ir.actions.act_window",
                name: "Search Visitor",
                res_model: "muki.rest",
                views: [[false,'form']],
                target: 'new',
                view_type : 'form',
                view_mode : 'form',
        });
        }
    };
    ListController.include(includeDict);
    });
    
    
    
