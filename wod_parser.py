'''
There are presented different parsing functions to work with wod_bot.py
Each function parses text.data from prepeared url links of 'word of a day' and 'english-russian translator' websites.
Then drops useless data from html and prepeare text information for exporting in word_bot for Telegram bot uses.
'''


import requests

def request_wod():
    '''
    Parses data from 'word of a day' site URL.
    Searches for tag with word of a day and for word's definition
    Then returns this text information for exporting in word_bot for Telegram bot uses.

    :return: tuple of str
    '''
    request = requests.get('https://www.learnersdictionary.com/word-of-the-day')
    text = request.text
    # Use for checking parsed html.
    # with open('parsed_text.txt', 'w', encoding='utf_8') as save:
    #     save.write(text)
    start_head = text.find('"hw_txt">') + len('"hw_txt">')
    stop_head = text.find('</span>', start_head)
    word = text[start_head: stop_head]
    start_defin = text.find('</strong>', text.find('<!--mid-->', start_head)) + len('</strong>')
    stop_defin = text.find('</p>', start_defin)
    definition = text[start_defin: stop_defin].capitalize()
    return word, definition


# Alternative source with obscene words filter.
# def request_trans(word):
#     translation = requests.get('https://wooordhunt.ru/word/'+word)
#     text = translation.text
#     start = text.find('<div class="t_inline_en">')  + len('<div class="t_inline_en">')
#     stop = text.find('</div>', start)
#     return text[start:stop]


def request_trans(word:str) -> str:
    '''
    Parses data from from prepeared url links of 'english-russian translator' website.
    Prepeared link is the result of concatenating of basic url for site and '/word' argument.
    The resulted link leads to the page with words translation and definition.
    After that searches in html text for info with word translation.

    :param word: user defined word to translate (from Telegram)
    :return: str with translation or failure phrase.
    '''
    # Different links for translation directions.
    english_russian = 'https://ru.pons.com/%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4/%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9-%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9/'
    russian_english = 'https://ru.pons.com/%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4/%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9/'
    # If there is nothing to translate.
    if not word.rstrip():
        return 'Looks like you forgot to write a word. Or maybe you want to know that "nothing" is "ничего"?'
    # Parsing part for 'word' with are some russian letters.
    if not set('йцукенгшщзхъфывапролджэячсмитьбюё').intersection(set(word.lower())):
        request_base = english_russian
        translation = requests.get(request_base + word)
        text = translation.text
        search_text = text[text.find('<h3 class="">\n1.'):]
        stop = search_text.find('</a> <span class="genus">')
    # Parsing part for 'word' with english letters only.
    else:
        request_base = russian_english
        word = str(word.encode(encoding='utf_8'))[2:-1].replace(r'\x', '%').upper()
        translation = requests.get(request_base + word)
        text = translation.text
        search_text = text[text.find("a href='" + english_russian[19:]):]
        stop = search_text.find('</a>')
    search_text = search_text[:stop]
    start = search_text.rfind('>') + 1
    result = '= ' + search_text[start:stop]
    return result if result != '= ' else '...are you shure? There is not such word in my dictionaries'