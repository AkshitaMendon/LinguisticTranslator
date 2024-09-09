from flask import Flask, request, render_template
from easygoogletranslate import EasyGoogleTranslate
import os

app = Flask(__name__)

def get_iso_from_name(language_name):
    # Get the absolute path to the 'static' folder
    static_folder = os.path.join(app.root_path, 'static')

    # Construct the full path to the languages.txt file
    languages_file_path = os.path.join(static_folder, 'languages.txt')

    # Read the languages.txt file to map language names to iso codes
    with open(languages_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            name = parts[:-1]
            iso_code = parts[-1]
            if ' '.join(name) == language_name:
                return iso_code

@app.route('/', methods=['GET', 'POST'])
def page():
    if request.method == 'POST':
        source_lang_name = request.form.get('sourceLang')
        target_lang_name = request.form.get('targetLang')
        sentence = request.form.get('sentence')

        # Get ISO codes from language names
        source_lang_iso = get_iso_from_name(source_lang_name)
        target_lang_iso = get_iso_from_name(target_lang_name)

        # Translate the sentence
        translator = EasyGoogleTranslate(source_language=source_lang_iso, target_language=target_lang_iso)
        result = translator.translate(sentence)

        # Additional translation step for each phrase to the chosen source language
        additional_words = ['yes', 'no', 'thank you', 'please', 'food', 'water', 'sorry']   # Add your additional words here
        additional_translations = []
        for word in additional_words:
            additional_translations.append(f"{translate_to_source_language(word, target_lang_iso, source_lang_iso)} - {translator.translate(word)}")

        # Combine the primary translation and additional translations
        response = "\n".join([result] + additional_translations)
        return response

    # If it's a GET request, render the HTML page
    return render_template('page.html')

@app.route('/india')
def india():
    return render_template('india.html')

@app.route('/world')
def world():
    return render_template('world.html')

def translate_to_source_language(text, from_lang, to_lang):
    # Use EasyGoogleTranslate for source language translation
    translator = EasyGoogleTranslate(source_language=from_lang, target_language=to_lang)
    translated_text = translator.translate(text)
    return translated_text

if __name__ == '__main__':
    app.run(debug=True)
