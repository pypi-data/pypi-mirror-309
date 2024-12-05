import logging
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

# Configure logger
logger = logging.getLogger("TranslationLogger")
logger.setLevel(logging.INFO)

# Create console handler and set level to info
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Add formatter to console handler
console_handler.setFormatter(formatter)

# Add console handler to logger
logger.addHandler(console_handler)

class Translator:
    # Define LANGUAGE_CODES as a class-level variable
    LANGUAGE_CODES = {
        "ar": "ar_AR", "cs": "cs_CZ", "de": "de_DE", 
        "en": "en_XX", "es": "es_XX", "et": "et_EE",
        "fi": "fi_FI", "fr": "fr_XX", "gu": "gu_IN", 
        "hi": "hi_IN", "it": "it_IT", "ja": "ja_XX", 
        "kk": "kk_KZ", "ko": "ko_KR", "lt": "lt_LT", 
        "lv": "lv_LV", "my": "my_MM", "ne": "ne_NP", 
        "nl": "nl_XX", "ro": "ro_RO", "ru": "ru_RU", 
        "si": "si_LK", "tr": "tr_TR", "vi": "vi_VN", 
        "zh": "zh_CN", "af": "af_ZA", "az": "az_AZ", 
        "bn": "bn_IN", "fa": "fa_IR", "he": "he_IL", 
        "hr": "hr_HR", "id": "id_ID", "ka": "ka_GE", 
        "km": "km_KH", "mk": "mk_MK", "ml": "ml_IN", 
        "mn": "mn_MN", "mr": "mr_IN", "pl": "pl_PL", 
        "ps": "ps_AF", "pt": "pt_XX", "sv": "sv_SE", 
        "sw": "sw_KE", "ta": "ta_IN", "te": "te_IN", "th": "th_TH", 
        "tl": "tl_XX", "uk": "uk_UA", "ur": "ur_PK", "xh": "xh_ZA", 
        "gl": "gl_ES", "sl": "sl_SI"
    }

    def __init__(self):
        try:
            self.model_name = "facebook/mbart-large-50-many-to-many-mmt"
            self.model = MBartForConditionalGeneration.from_pretrained(self.model_name)
            self.tokenizer = MBart50TokenizerFast.from_pretrained(self.model_name)
            logger.info("Model and tokenizer loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading model or tokenizer: {e}")
            raise e

    def translate(self, text: str, lang: str):
        try:
            # Debugging: Print the language input and check mapping
            logger.info(f"Received language: {lang}")

            lang_code = None
            if lang in self.LANGUAGE_CODES:
                lang_code = self.LANGUAGE_CODES[lang]  # Language name to language code
                logger.info(f"Mapped language '{lang}' to language code '{lang_code}'")
            elif lang in self.LANGUAGE_CODES.values():
                lang_code = lang  # Language code already passed
                logger.info(f"Using language code '{lang_code}' directly")
            else:
                raise ValueError(f"Invalid language: {lang}")

            logger.info(f"Translating to {lang_code} ({lang})")

            # Tokenize the input text
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)

            # Translate
            translated = self.model.generate(
                inputs["input_ids"],
                forced_bos_token_id=self.tokenizer.lang_code_to_id[lang_code]  # Use lang_code for forced BOS token
            )

            # Decode the translated tokens back into text
            translation = self.tokenizer.decode(translated[0], skip_special_tokens=True)
            return translation

        except Exception as e:
            logger.error(f"Error during translation: {e}")
            raise e
