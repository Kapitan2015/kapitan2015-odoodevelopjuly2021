//console.log("custom callleddddddddddddddddddddd")
odoo.define('pos_advance_order_note.pos', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var gui = require('point_of_sale.gui');
    var popups = require('point_of_sale.popups');

    var _t = core._t;
    
    models.load_models({
        model: 'pos.order.note',
        fields: ['sequence','order_note'],
        domain: null,
        loaded: function(self, pos_adv_order_note) {
            
            self.pos_adv_order_note = pos_adv_order_note;
        },

    });
    
    // Start POSBarcodeReturnWidget
	
    var POSAdvOrderNoteWidget = screens.ActionButtonWidget.extend({
        template: 'POSAdvOrderNoteWidget',

        button_click: function() {
            var self = this;
            var order_note = self.pos.pos_adv_order_note;
		    var note_items = [];
		    
		    for (var i =0; i< order_note.length; i++){ 
		        note_items.push(order_note[i])
		    }

            this.gui.show_popup('pos_order_note_popup_widget', {'notes': note_items});
        },
        
    });

    screens.define_action_button({
        'name': 'POS Order Note',
        'widget': POSAdvOrderNoteWidget,
        'condition': function() {
            return true;
        },
    });
    
    
    // End POSBarcodeReturnWidget	

    var PosOrderNotePopupWidget = popups.extend({
        template: 'PosOrderNotePopupWidget',
        init: function(parent, args) {
            this._super(parent, args);
            this.options = {};
            this.product_notes = false;
            this.order_notes = false;
        },
        
        
        show: function(options) {
        	options = options || {};
            var self = this;
            this._super(options);
            var notes = self.pos.pos_adv_order_note;
            
            notes.forEach(function(note) {
                note.active = false;
            });

        },
        
        events: {
            'click .product_note1 .button': 'update_note',
            // 'click .note_category .button': 'product_note',
            'click .product_type': 'product_note',
            'click .order_type': 'order_note',
            'click .button.confirm-note': 'confirm_notes',
            'click .button.cancel': 'click_cancel',
        },

        order_note: function(event) {
            var self = this;
            if ($(event.target).hasClass("highlight")) {
                $(event.target).removeClass('highlight');
                this.order_notes = false;

            } else {
                var state = event.currentTarget.getAttribute('data-id');
                $(event.target).addClass("highlight");
                this.order_notes = true;
                state = true;
            }
        },
        
        product_note: function(event) {
            var self = this;
            if ($(event.target).hasClass("highlight")) {
                $(event.target).removeClass('highlight');
                this.product_notes = false;

            } else {
                var state = event.currentTarget.getAttribute('data-id');
                $(event.target).addClass("highlight");
                this.product_notes = true;
                state = true;
            }
        },
        
        update_note: function(event) {
            var self = this;
            var id = event.currentTarget.getAttribute('data-id');
            var entered_note = $("#enter_note");
            var notes_order = self.pos.pos_adv_order_note;
		    self.active_order_note($(event.target), id);

            
        },
        
        active_order_note: function(note_obj, id){

            if (note_obj.hasClass("highlight")) {
                note_obj.removeClass('highlight');
                this.get_note_by_id(id).active = false;
            } else {
                note_obj.addClass("highlight");
                this.get_note_by_id(id).active = true;
            }
        },
        
        get_note_by_id: function(id) {
            var self = this;
            return _.find(self.pos.pos_adv_order_note, function(item) {
                return item.id === Number(id);
            });
        },
        
        
        
        confirm_notes: function(event, $el) {
            var self = this;
            var note1 = self.pos.pos_adv_order_note;
            var order = this.pos.get_order();
            var selectedOrder = self.pos.get('selectedOrder');
            var partner_id = false
            var pre_notes = '';
            if (order.get_client() != null)
                partner_id = order.get_client();
            var product_id = false
            for (var j =0; j< note1.length; j++){ 
                if (note1[j]['active'] == true){
                    pre_notes += ' '+ note1[j]['order_note'] + ','
                    note1[j]['active'] = false;
                }
                
            }
            var entered_note = $("#enter_note").val();
            if (entered_note){
                pre_notes += ' '+ entered_note +',';
            }
            //this.$('.note_category .button').click(function(){
            //}
            
            if(order.orderlines.length != 0){
                if (order.get_selected_orderline().product.id != null)
                    product_id = order.get_selected_orderline().product.id

                    var orderlines = order.orderlines;
                    
                   var selectedOrderLine = order.get_selected_orderline();

            if (this.product_notes) {
                selectedOrderLine.set_staystr(pre_notes);
                // $(event.target).removeClass('highlight');
                this.product_notes = false;
               
            }
            //  else {
            //     selectedOrder.set_staystr(pre_notes);
            // }

            if (this.order_notes) {
               selectedOrder.set_staystr(pre_notes);
               // $(event.target).removeClass('highlight');
               this.order_notes = false;
            }
             // else {
            //     selectedOrderLine.set_staystr(pre_notes);
            // }
                   
            // var note_type = $(".order_type .button .highlight").find('button highlight');
              // if($(".order_type .button .highlight")){
              //   console.log('++++++++++++++++++++++++++++++++++++++++++++++++++++', $el, event);
              // }
              // if($(".product_type .button .highlight")){
              //   console.log('****************************************************', $el, event);
              // }
              // if($(".order_type .button .highlight")){
              //   console.log('++++++++++++++++++++++++++++++++++++++++++++++++++++', $el, event);
              // }
               
              
		       // selectedOrderLine.set_staystr(pre_notes);
		       // selectedOrder.set_staystr(pre_notes);
		       self.gui.close_popup();
		   }
		   else{
		        self.gui.show_popup('error', {
                    'title': _t('Empty Order'),
                    'body': _t('There must be at least one product in your order before you want to apply Notes'),
                });
		   }
		    
        },
        
        renderElement: function() {
            var self = this;
            this._super();
            
            
        },

    });
    
    gui.define_popup({
        name: 'pos_order_note_popup_widget',
        widget: PosOrderNotePopupWidget
    });
    
    
    
        // exports.Orderline = Backbone.Model.extend ...
    var OrderlineSuper = models.Orderline;
    models.Orderline = models.Orderline.extend({
		initialize: function(attr,options){
		OrderlineSuper.prototype.initialize.apply(this, arguments);
        this.pos   = options.pos;
        this.order = options.order;
        
        if (options.json) {
            this.init_from_JSON(options.json);
            return;
        }

        this.set_staystr();

    },
    clone: function(){
        var orderline = new exports.Orderline({},{
            pos: this.pos,
            order: null,
            product: this.product,
            price: this.price,
        });
        
        orderline.quantity = this.quantity;
        orderline.quantityStr = this.quantityStr;
        orderline.stayStr = this.stayStr;
        orderline.discount = this.discount;
        orderline.type = this.type;
        orderline.selected = false;
        return orderline;
    },
    
    set_staystr: function(entered_note){
	  this.stayStr = entered_note;
	  this.trigger('change',this);
    },

    get_to_stay: function(){
        return this.stayStr;
    },

    export_as_JSON: function() {
        var pack_lot_ids = [];
        if (this.has_product_lot){
            this.pack_lot_lines.each(_.bind( function(item) {
                return pack_lot_ids.push([0, 0, item.export_as_JSON()]);
            }, this));
        }
        return {
            qty: this.get_quantity(),
            price_unit: this.get_unit_price(),
            price_subtotal: this.get_price_without_tax(),
            price_subtotal_incl: this.get_price_with_tax(),
            discount: this.get_discount(),
            product_id: this.get_product().id,
            tax_ids: [[6, false, _.map(this.get_applicable_taxes(), function(tax){ return tax.id; })]],
            id: this.id,
            pack_lot_ids: pack_lot_ids,
	        notes_line: this.get_to_stay()

        };
    },

    
    
    });
    // End Orderline start
    
    
    var OrderSuper = models.Order;
    models.Order = models.Order.extend({

		init: function(parent, options) {
		    var self = this;
		    this._super(parent,options);

		    this.set_staystr();

		},
		
		set_staystr: function(entered_charge){
		
		  this.stayStr = entered_charge;
		  this.trigger('change',this);
		},
		
		get_to_stay: function(){
            return this.stayStr;
        },
        
        export_as_JSON: function() {
            var self = this;
            var loaded = OrderSuper.prototype.export_as_JSON.call(this);
            loaded.get_to_stay = self.get_to_stay();
            return loaded;
        },

		
    });
    
    var OrderWidgetExtended = screens.OrderWidget.include({

		update_summary: function(){
		    var order = this.pos.get_order();
		    if (!order.get_orderlines().length) {
		        return;
		    }

		    var total     = order ? order.get_total_with_tax() : 0;
		    var taxes     = order ? total - order.get_total_without_tax() : 0;
		    var order_note    = order ? order.get_to_stay() : 0;

		    this.el.querySelector('.summary .total > .value').textContent = this.format_currency(total);
		    this.el.querySelector('.summary .total .subentry .value').textContent = this.format_currency(taxes);
		    this.el.querySelector('.items .value').textContent = order_note;

		},
    });

});
