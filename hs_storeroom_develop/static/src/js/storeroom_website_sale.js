odoo.define('hs_storeroom_develop.storeroom', function (require) {
	"use strict";

	// var ajax = require('web.ajax');
	// var Widget = require("web.Widget");
	// var rpc = require("web.rpc");
	var sAnimations = require('website.content.snippets.animation');

	console.log("Hola Mundo")
	sAnimations.registry.storeroom = sAnimations.Class.extend({
		selector: '#hs_website_storeroom_forms',
		read_events: {
			'change': '_onChangeStoreRoom',
		},
		start: function () {
			
			var def = this._super.apply(this, arguments);
			return def
		},
		_onChangeStoreRoom: function (ev) {
			var $input = $(ev.target);

			var value = $input.val();
			if (isNaN(value)) {
				return;
			};
			$('#strifund').val(value);
			// $('.o_website_form_send').attr('disabled', false);
			$('.o_website_form_send').removeClass('disabled');
		},
	});

});