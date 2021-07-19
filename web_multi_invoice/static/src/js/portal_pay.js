odoo.define('web_multi_invoice.portal_pay', function (require) {
'use strict';

var ajax = require('web.ajax')
var Dialog = require('web.Dialog');
var payment_process = require('payment.processing')
var payment_event = require('payment.payment_form')

$(document).ready(function (){
    $('.select_invoice_cls').click(function(event){
         var tbody_id = $(event.currentTarget).parent().parent().parent().next()
         var invoice_list = [];
         var self = this
         var access_token = $("input[name='access_token']").val() || $("input[name='token']").val() || '';
          $.each($("input[name='portal_invoice']:checked"), function(){
                invoice_list.push($(this).val());

            });
         if (invoice_list.length > 0){
            document.getElementById("pay_multi_portal_id").style.display = 'block';
         }else{
            document.getElementById("pay_multi_portal_id").style.display = 'none';
         }
         $('#multi_invoices').val(invoice_list)
    })
 })

return payment_process.include({
        processPolledData: function (transactions) {
            var render_values = {
                'tx_draft': [],
                'tx_pending': [],
                'tx_authorized': [],
                'tx_done': [],
                'tx_cancel': [],
                'tx_error': [],
            };
            if (transactions.length > 0 && transactions[0].acquirer_provider == 'transfer') {
                window.location = transactions[0].return_url;
                return;
            }
            // group the transaction according to their state
            transactions.forEach(function (tx) {
                var key = 'tx_' + tx.state;
                if(key in render_values) {
                    render_values[key].push(tx);
                }
            });

            function countTxInState(states) {
                var nbTx = 0;
                for (var prop in render_values) {
                    if (states.indexOf(prop) > -1 && render_values.hasOwnProperty(prop)) {
                        nbTx += render_values[prop].length;
                    }
                }
                return nbTx;
            }
            // if there's only one tx to manage
            if(countTxInState(['tx_done', 'tx_error'])) {
                var tx = render_values['tx_done'][0] || render_values['tx_error'][0];
                if (tx) {
                    window.location = tx.return_url;
                    return;
                }
            }

            this.displayContent("payment.display_tx_list", render_values);
        },
})

});