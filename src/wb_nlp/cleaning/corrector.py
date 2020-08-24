import re
import wordninja


# General Text Processors

def recover_segmented_words(raw_input: str, max_len: int=5) -> str:
    '''This algorithm processes and input text to detect and fix any malformed words.

    Example:
        input: "million p rote c te d   by u n h c r Of the world's displaced"
        output: "million protected by unhcr Of the world's displaced"

    '''
    MAX_LEN = max_len

    alpha_streak = 0
    word_streak = 0
    val_span = ''
    temp_span = ''
    ends_space = False
    spaces = {' ', '\n', '\t'}

    # Handle plural form of acronyms, e.g., IDPs -> IDP
    ss = re.sub(r'(\W[A-Z]{2,})(s)(\W)', r'\1\3', raw_input)

    text = ''

    for i in ss:
        if i.isalpha():
            alpha_streak += 1
            temp_span += i
            ends_space = False
        else:
            if (alpha_streak and alpha_streak <= MAX_LEN) or (val_span and ends_space):
                if i in spaces:
                    val_span += temp_span + i
                    word_streak += 1
                    temp_span = ''
                    ends_space = True  # Speeds up processing vs. using val_span[-1].isspace()!
                    alpha_streak = 0
                    continue

            if word_streak >= 2:
                text += ' '.join(wordninja.split(''.join(val_span.split())))
                text += ' ' + temp_span + i
            else:
                text += val_span + temp_span + i

            word_streak = 0
            temp_span = ''
            val_span = ''
            ends_space = False
            alpha_streak = 0

    return text
