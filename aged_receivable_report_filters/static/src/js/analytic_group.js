odoo.define('aged_receivable_report_filters.group', function (require){
"use strict";

var core = require('web.core');
var Context = require('web.Context');
var Widget = require('web.Widget');
var account_reports = require('account_reports.account_report')

var QWeb = core.qweb;
var _t = core._t;

// Include widget
account_reports.include({
    render_searchview_buttons: function(){
        //To get value of group filter
        var self = this;
        this._super();
        this.$searchview_buttons.find('.js_account_reports_analytic_group').select2();
        if (self.report_options.analytic_group) {
            self.$searchview_buttons.find('[data-filter="analytic_group"]').select2("val",
             self.report_options.analytic_group);
        }
        this.$searchview_buttons.find('.js_account_reports_analytic_group').on('change',
        function(){
            self.report_options.analytic_group = self.$searchview_buttons.find('[data-filter="analytic_group"]').val();
            return self.reload().then(function(){
                self.$searchview_buttons.find('.account_analytic_filter').click();
            })
        });
    },
  });
});
