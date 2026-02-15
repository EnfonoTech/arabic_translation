# Copyright (c) 2025, arabic_translation and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class ArabicTranslationKey(Document):
	"""Store Groq API key for Arabic translation (singleton)."""
	pass
