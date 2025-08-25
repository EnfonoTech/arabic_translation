frappe.ui.form.on('Item', {
    custom_translate: function(frm) {
        if (frm.doc.item_name) {
            frappe.call({
                method: "arabic_translation.api.translation.translate_to_arabic",
                args: {
                    text: frm.doc.item_name
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value("custom_item_name_arabic", r.message);
                        frappe.show_alert({
                            message: "Item Name translated to Arabic",
                            indicator: "green"
                        })
                    }
                }
            });
        } else {
            frappe.msgprint(__('Please enter Item Name first.'));
        }
    }
});
