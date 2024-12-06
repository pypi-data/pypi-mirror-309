import logging
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast, MarianMTModel, MarianTokenizer

# Configure logger
logger = logging.getLogger("TranslationLogger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
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
            self.mbart_model_name = "facebook/mbart-large-50-many-to-many-mmt"
            self.mbart_model = MBartForConditionalGeneration.from_pretrained(self.mbart_model_name)
            self.mbart_tokenizer = MBart50TokenizerFast.from_pretrained(self.mbart_model_name)
            logger.info("MBart model and tokenizer loaded successfully.")

            # Load Helsinki-NLP model for German translations
            self.helsinki_model_name = "Helsinki-NLP/opus-mt-en-de"
            self.helsinki_model = MarianMTModel.from_pretrained(self.helsinki_model_name)
            self.helsinki_tokenizer = MarianTokenizer.from_pretrained(self.helsinki_model_name)
            logger.info("Helsinki model and tokenizer loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading models or tokenizers: {e}")
            raise e

    def translate(self, text: str, lang: str):
        try:
            logger.info(f"Received language: {lang}")

            # Use Helsinki model for German translations
            if lang == "de" or lang == "de_DE":
                logger.info("Using Helsinki model for German translation.")
                inputs = self.helsinki_tokenizer(text, return_tensors="pt", padding=True, truncation=True)
                translated = self.helsinki_model.generate(inputs["input_ids"])
                translation = self.helsinki_tokenizer.decode(translated[0], skip_special_tokens=True)
                return translation

            # Use MBart model for other languages
            lang_code = None
            if lang in self.LANGUAGE_CODES:
                lang_code = self.LANGUAGE_CODES[lang]
                logger.info(f"Mapped language '{lang}' to language code '{lang_code}'")
            elif lang in self.LANGUAGE_CODES.values():
                lang_code = lang
                logger.info(f"Using language code '{lang_code}' directly")
            else:
                raise ValueError(f"Invalid language: {lang}")

            logger.info(f"Translating to {lang_code} ({lang})")
            inputs = self.mbart_tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            translated = self.mbart_model.generate(
                inputs["input_ids"],
                forced_bos_token_id=self.mbart_tokenizer.lang_code_to_id[lang_code]
            )
            translation = self.mbart_tokenizer.decode(translated[0], skip_special_tokens=True)
            return translation

        except Exception as e:
            logger.error(f"Error during translation: {e}")
            raise e



