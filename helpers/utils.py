from guideposts.guidepost import result_path
import datetime
import re


def todays_date():
    today_date = datetime.date.today()
    formatted_date = today_date.strftime("%d-%m-%Y")
    return formatted_date

def write_down_to_txt(element_to_safe):
    with open(result_path(), "a") as file:
        file.write(f'{todays_date()} -> {element_to_safe} \n')

def encode(list):
    return [list_element.replace(u'\xa0', ' ') for list_element in list]

def eliminate_redundant_words(list):
    words_to_eliminate =['1 uncja Srebra', 'srebrna moneta', '1 uncja srebra', 'Srebrna Moneta',
                         'Srebrna moneta', 'Srebrny medal', '1 oz', '1oz', '1 uncja', '1 uncja (proof-color)',
                         '1 uncja (proof)', '(proof)', '(proof-color)']
    result = []
    for sentence in list:
        for element in words_to_eliminate:
            sentence = sentence.replace(element, '')
        result.append(sentence)
    return result

def create_dict_with_name_and_price(scrapper_list):
    price_pattern = r'\b\d{1,3}(?:,\d{3})*(?:\.\d{2})? zł\b'
    price_dict = {}
    for item in scrapper_list:
        price_dict[item.split(',', 1)[0].strip()] = item.split(',', 1)[1].strip()
    return price_dict

def translate_sentence(sentence, target_language='pl'):
    from googletrans import Translator
    translator = Translator()
    translated_sentence = translator.translate(sentence, dest=target_language).text
    return translated_sentence


