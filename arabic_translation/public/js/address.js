frappe.ui.form.on('Address', {
	custom_translate: function(frm) {
		var fields_to_translate = [
			{ source: 'address_line1', target: 'custom_address_line1_arabic', label: 'Address Line 1' },
			{ source: 'custom_area', target: 'custom_area_arabic', label: 'Area' },
			{ source: 'city', target: 'custom_city_arabic', label: 'City' },
			{ source: 'country', target: 'custom_country_arabic', label: 'Country' }
		];

		var has_any = fields_to_translate.some(function(f) { return frm.doc[f.source]; });
		if (!has_any) {
			frappe.msgprint(__('Please enter at least one of: Address Line 1, Area, City, or Country.'));
			return;
		}

		var translated = 0;
		var total = 0;
		fields_to_translate.forEach(function(f) {
			if (frm.doc[f.source]) total++;
		});

		function do_translate(idx) {
			if (idx >= fields_to_translate.length) {
				if (translated > 0) {
					frm.refresh_fields();
					frappe.show_alert({
						message: __('Translated to Arabic'),
						indicator: 'green'
					});
				}
				return;
			}
			var f = fields_to_translate[idx];
			if (!frm.doc[f.source]) {
				do_translate(idx + 1);
				return;
			}
			frappe.call({
				method: 'arabic_translation.api.translation.translate_to_arabic',
				args: { text: frm.doc[f.source], context: 'address' },
				callback: function(r) {
					if (r.message) {
						frm.set_value(f.target, r.message);
						translated++;
					}
					do_translate(idx + 1);
				}
			});
		}
		do_translate(0);
	}
});
