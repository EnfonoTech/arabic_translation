import requests

import frappe

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-oss-120b"
DEFAULT_FALLBACKS = ("qwen/qwen3.8-27b", "openai/gpt-oss-20b")
TIMEOUT = 12

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


def get_model_chain():
    """The model to use, then the ones to fall back to.

    Groq retires models without notice: the previous hard-coded
    `meta-llama/llama-4-scout-17b-16e-instruct` started answering 404 `model_not_found` and every
    Customer and Address save logged a failure until somebody read the traceback. The chain lives
    in settings so the next retirement is a field edit, and it is walked automatically so in most
    cases nobody has to notice at all.
    """
    model, fallbacks = None, None
    try:
        settings = frappe.get_single("Arabic Translation Key")
        model = (settings.get("model") or "").strip()
        fallbacks = settings.get("fallback_models") or ""
    except Exception:
        pass

    chain = [model or DEFAULT_MODEL]
    for line in (fallbacks or "\n".join(DEFAULT_FALLBACKS)).splitlines():
        line = line.strip()
        if line and line not in chain:
            chain.append(line)
    return chain


def _clean(text):
    """Return only the Arabic. Models like to wrap the answer in quotes, and gpt-oss pads digits
    inside an address with narrow no-break spaces that read as boxes in a PDF."""
    text = (text or "").strip().strip('"').strip("\u201c\u201d").strip()
    return text.replace("\u202f", " ").replace("\u2009", " ").strip()


def _ask(model, system, prompt, headers):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1024,
        "top_p": 0.9,
    }
    # a reasoning model spends max_tokens thinking and can return an EMPTY content field --
    # measured on gpt-oss-20b, which answered "" for a customer name it clearly understood
    if "gpt-oss" in model:
        payload["reasoning_effort"] = "low"

    response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=TIMEOUT)
    if not response.ok:
        raise Exception(f"{response.status_code} from Groq for model {model}: "
                        f"{response.text[:200]}")
    return _clean(response.json()["choices"][0]["message"].get("content"))


def translate_with_groq_natural(text, target_lang, source_lang, context=None):
    api_key = get_groq_api_key()
    if not api_key:
        raise Exception("Groq API key not configured")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    prompt, system = _get_prompt_and_system(text, context)

    # An Address save translates up to four fields one after another, in before_save. Without
    # this memo a retired model is re-tried on every field of every save -- four dead calls per
    # address, and the user waits for all of them.
    dead = getattr(frappe.local, "arabic_translation_dead_models", None)
    if dead is None:
        dead = set()
        frappe.local.arabic_translation_dead_models = dead

    last_error = None
    for model in get_model_chain():
        if model in dead:
            continue
        try:
            translated = _ask(model, system, prompt, headers)
        except Exception as e:
            last_error = e
            # 404 means retired, 401/403 means the key cannot use it: no point asking again this
            # request. A timeout or a 429 might pass next time, so those are not remembered.
            if any(code in str(e) for code in ("404", "401", "403")):
                dead.add(model)
            continue
        if translated:
            return {"translated_text": translated}
        # an empty answer is a failure of this model, not of the text -- try the next one
        last_error = Exception(f"{model} returned an empty translation")

    raise Exception(str(last_error) if last_error else "No Groq model produced a translation")


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
    
