# **Translation Package**

**Overview**
This package provides a translation service using the facebook/mbart-large-50-many-to-many-mmt model. It supports translating text between multiple languages, including automatic language detection. This is useful for integrating translation capabilities into your applications.

**Features**                                             
Multi-language translation: Supports 50+ languages.
Automatic language detection: Detects the language of the input text.
Uses facebook/mbart-large-50-many-to-many-mmt model: State-of-the-art multilingual translation model.
Simple API: Easy integration into your Python projects.
Installation
Using Poetry
If you're using Poetry to manage dependencies, follow these steps:

**Clone this repository:**

git clone https://github.com/manojprabhakar90/translation.git

You can directly install the package through pip install translation-new

# Usage

from translation_new.translator import Translator

translator = Translator()

translated_text = translator.translate("Hello, how are you?", lang="hi")

print(translated_text)

# Supported Languages

This package supports translation between the following languages (identified by their ISO codes):

Arabic (ar)
Bengali (bn)
Chinese (zh)
French (fr)
German (de)
Hindi (hi)
Spanish (es)
And many more!
For a complete list of supported languages, please check the LANGUAGE_CODES in the Translator class.

# **Contributions** 
We welcome contributions to improve the translation package. If you'd like to contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Push to the branch (git push origin feature-branch).
5. Create a pull request with a description of your changes.

# **License**

This project is licensed under the MIT License - see the LICENSE file for details.


