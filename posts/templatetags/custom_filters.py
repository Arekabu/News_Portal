from django import template
import os

register = template.Library()

@register.filter()
def censor(text):
    text_words = text.split()
    bad_words = []
    path = file_path = os.path.join(os.path.dirname(__file__), 'bad_words.txt')
    with open(path, 'r', encoding='utf-8') as b_words_file:
        for word in b_words_file:
            bad_words.append(word.strip())
    censored_text = []
    for word in text_words:
        if word.find('-'):
            complex_word = []
            for sub_word in word.split('-'):
                if sub_word in bad_words:
                    complex_word.append(sub_word[0].ljust(len(sub_word), '*'))
                else:
                    complex_word.append(sub_word)
            censored_text.append('-'.join(complex_word))

        elif word.lower().strip(' ,.!?') in bad_words:
            censored_text.append(word[0].ljust(len(word),'*'))
        else: censored_text.append(word)

    censored_text = ' '.join(censored_text)
    return censored_text