# Copyright (c) 2025, arabic_translation and contributors
# License: MIT

import frappe
from arabic_translation.api.translation import auto_translate_disabled, translate_to_arabic


def translate_customer_on_save(doc, method=None):
	"""Translate customer_name to Arabic on save when Arabic field is empty."""
	if auto_translate_disabled():
		return
	source_value = doc.get("customer_name")
	target_value = doc.get("custom_customer_name_arabic")
	if not source_value or (target_value and target_value.strip()):
		return
	try:
		translated = translate_to_arabic(source_value, context="customer_name")
		if translated:
			doc.set("custom_customer_name_arabic", translated)
	except Exception as e:
		frappe.log_error(
			title="Customer Arabic Translation Failed",
			message=frappe.as_json({"error": str(e), "customer": doc.name}),
		)
