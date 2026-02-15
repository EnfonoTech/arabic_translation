import frappe
from frappe.integrations.utils import make_post_request

# Context: "customer_name" = phonetic name, "address" = place/location, None = default
def _get_prompt_and_system(text, context):
    if context == "customer_name":
        system = (
            "You are an expert in Arabic transliteration for personal and company names. "
            "Give the phonetic Arabic form: how the name is pronounced and written in Arabic, "
            "using standard Arabic spelling that preserves the sound. Do not translate meaning."
        )
        prompt = f"""Convert this name to its phonetic Arabic form (how it sounds and is written in Arabic):
"{text}"

- Use standard Arabic transliteration that preserves pronunciation
- This is a person or company name, not a phrase to translate literally
- Return ONLY the Arabic form, no explanations or quotation marks"""
        return prompt, system

    if context == "address":
        system = (
            "You are an expert in Arabic for places and locations. "
            "Treat the text as address parts: street, area, city, or location names. "
            "Use standard Arabic transliteration for place names; keep addresses natural and readable."
        )
        prompt = f"""This text is a place or location (address line, area, city, or similar):
"{text}"

- Give the appropriate Arabic form for a place/location
- Use standard Arabic transliteration for place names
- Return ONLY the Arabic form, no explanations or quotation marks"""
        return prompt, system

    # default
    system = f"You are an expert translator. Translate text naturally to Arabic, preserving meaning and business context."
    prompt = f"""Translate this English text to Arabic:
"{text}"

- Make it sound natural in Arabic
- Preserve meaning and tone; use appropriate business terminology
- Return ONLY the translation, no explanations or quotation marks

Translation:"""
    return prompt, system


@frappe.whitelist()
def translate_to_arabic(text, context=None):
    """
    Translate the given text from English to Arabic using Groq API.
    context: "customer_name" for phonetic name, "address" for place/location, or None for default.
    Returns translated Arabic text as string.
    """
    try:
        result = translate_with_groq_natural(
            text, target_lang="Arabic", source_lang="English", context=context
        )
        return result.get("translated_text")
    except Exception as e:
        frappe.throw(f"Translation failed: {str(e)}")


def translate_with_groq_natural(text, target_lang, source_lang, context=None):
    api_key = get_groq_api_key()
    if not api_key:
        raise Exception("Groq API key not configured")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt, system = _get_prompt_and_system(text, context)

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1024,
        "top_p": 0.9
    }

    response = make_post_request(url, headers=headers, json=payload)
    translated_text = response["choices"][0]["message"]["content"].strip()
    return {"translated_text": translated_text}


def get_groq_api_key():
    """Get Groq API key from Arabic Translation Key doctype (singleton). Falls back to site config if not set in doctype."""
    key = None
    try:
        # Use doc.get_password with raise_exception=False so we get None instead of throw when not in __Auth
        doc = frappe.get_single("Arabic Translation Key")
        key = doc.get_password("groq_api_key", raise_exception=False)
    except Exception:
        pass
    if key and key.strip():
        return key.strip()
    # Fallback: read from __Auth in case doc.get_password didn't return it (e.g. cached doc with dummy value)
    try:
        from frappe.utils.password import get_decrypted_password
        key = get_decrypted_password(
            "Arabic Translation Key",
            "Arabic Translation Key",
            "groq_api_key",
            raise_exception=False,
        )
    except Exception:
        pass
    if key and key.strip():
        return key.strip()
    return frappe.conf.get("groq_api_key")
    
