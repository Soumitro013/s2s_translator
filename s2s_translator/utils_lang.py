# Language utilities and mappings

# ISO-639-1 codes for common Indic + English
LANG_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam",
    "gu": "Gujarati",
    "mr": "Marathi",
    "pa": "Punjabi",
    "or": "Odia",
    "kn": "Kannada",
}

# MarianMT (Helsinki-NLP opus-mt) model names for **direct** pairs.
# For pairs not present, the pipeline pivots via English.
LANG_PAIR_TO_MARIAN = {
    ("hi", "en"): "Helsinki-NLP/opus-mt-hi-en",
    ("en", "hi"): "Helsinki-NLP/opus-mt-en-hi",
    ("bn", "en"): "Helsinki-NLP/opus-mt-bn-en",
    ("en", "bn"): "Helsinki-NLP/opus-mt-en-bn",
    ("ta", "en"): "Helsinki-NLP/opus-mt-ta-en",
    ("en", "ta"): "Helsinki-NLP/opus-mt-en-ta",
    ("te", "en"): "Helsinki-NLP/opus-mt-te-en",
    ("en", "te"): "Helsinki-NLP/opus-mt-en-te",
    ("ml", "en"): "Helsinki-NLP/opus-mt-ml-en",
    ("en", "ml"): "Helsinki-NLP/opus-mt-en-ml",
    ("gu", "en"): "Helsinki-NLP/opus-mt-gu-en",
    ("en", "gu"): "Helsinki-NLP/opus-mt-en-gu",
    ("mr", "en"): "Helsinki-NLP/opus-mt-mr-en",
    ("en", "mr"): "Helsinki-NLP/opus-mt-en-mr",
    ("pa", "en"): "Helsinki-NLP/opus-mt-pa-en",
    ("en", "pa"): "Helsinki-NLP/opus-mt-en-pa",
    ("or", "en"): "Helsinki-NLP/opus-mt-or-en",
    ("en", "or"): "Helsinki-NLP/opus-mt-en-or",
    ("kn", "en"): "Helsinki-NLP/opus-mt-kn-en",
    ("en", "kn"): "Helsinki-NLP/opus-mt-en-kn",
}

def has_direct_marian(src: str, tgt: str) -> bool:
    return (src, tgt) in LANG_PAIR_TO_MARIAN

def get_marian_name(src: str, tgt: str):
    return LANG_PAIR_TO_MARIAN.get((src, tgt), None)
