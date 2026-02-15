frappe.ui.form.on('Customer', {
	custom_translate: function(frm) {
		if (frm.doc.customer_name) {
			frappe.call({
				method: 'arabic_translation.api.translation.translate_to_arabic',
				args: { text: frm.doc.customer_name, context: 'customer_name' },
				callback: function(r) {
					if (r.message) {
						frm.set_value('custom_customer_name_arabic', r.message);
						frappe.show_alert({
							message: __('Customer Name translated to Arabic'),
							indicator: 'green'
						});
					}
				}
			});
		} else {
			frappe.msgprint(__('Please enter Customer Name first.'));
		}
	}
});
