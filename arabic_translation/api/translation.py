import frappe
from frappe.integrations.utils import make_post_request

@frappe.whitelist()
def translate_to_arabic(text):
    """
    Translate the given text from English to Arabic using Groq API.
    Returns translated Arabic text as string.
    """
    try:
        result = translate_with_groq_natural(text, target_lang="Arabic", source_lang="English")
        return result.get("translated_text")
    except Exception as e:
        frappe.throw(f"Translation failed: {str(e)}")


def translate_with_groq_natural(text, target_lang, source_lang):
    api_key = get_groq_api_key()
    if not api_key:
        raise Exception("Groq API key not configured")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""You are a professional translator specializing in natural, fluent translations.

Translate this {source_lang} text to {target_lang}:
"{text}"

Requirements:
- Make it sound completely natural in {target_lang}
- Preserve the original meaning and tone
- Use appropriate business terminology
- Don't add explanations or notes
- Return ONLY the translation
- Don't add quotation marks

Translation:"""

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "system",
                "content": f"You are an expert translator. Translate text naturally to {target_lang}, preserving meaning and business context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 1024,
        "top_p": 0.9
    }

    response = make_post_request(
        url,
        headers=headers,
        json=payload
    )

    translated_text = response["choices"][0]["message"]["content"].strip()
    return {"translated_text": translated_text}


def get_groq_api_key():
    return frappe.conf.get("groq_api_key")
    
