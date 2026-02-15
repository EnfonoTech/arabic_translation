# Copyright (c) 2025, arabic_translation and contributors
# License: MIT

import frappe
from arabic_translation.api.translation import translate_to_arabic

ADDRESS_FIELD_MAP = [
	("address_line1", "custom_address_line1_arabic"),
	("custom_area", "custom_area_arabic"),
	("city", "custom_city_arabic"),
	("country", "custom_country_arabic"),
]


def translate_address_on_save(doc, method=None):
	"""Translate address fields to Arabic on save when Arabic field is empty."""
	for source_field, target_field in ADDRESS_FIELD_MAP:
		source_value = doc.get(source_field)
		target_value = doc.get(target_field)
		if not source_value or (target_value and target_value.strip()):
			continue
		try:
			translated = translate_to_arabic(source_value, context="address")
			if translated:
				doc.set(target_field, translated)
		except Exception as e:
			frappe.log_error(
				title="Address Arabic Translation Failed",
				message=frappe.as_json({"field": source_field, "error": str(e), "address": doc.name}),
			)
