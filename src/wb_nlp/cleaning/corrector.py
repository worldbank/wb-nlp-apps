import itertools
import re
import wordninja
from wb_nlp.cleaning.respelling import Respeller, OptimizedSpellChecker

# General Text Processors
class SpellingModels:
    def __init__(self, config: dict):
        self.config = config

        self.spell_checker = OptimizedSpellChecker(
            **self.config["spell_checker"]["__init__"]
        )
        self.respeller = Respeller(**self.config["respeller"]["__init__"])

    def fix_spellings(self, tokens: list) -> list:
        self.spell_checker.set_tokens(tokens)

        unfixed_tokens, fixed_tokens_map = self.respeller.infer_correct_words(
            [err_word.word for err_word in self.spell_checker],
            infer_correct_word_params=self.config["respeller"]["infer_correct_word"],
            **self.config["respeller"]["infer_correct_words"],
        )

        tokens = list(
            itertools.chain.from_iterable(
                [
                    fixed_tokens_map.get(token, [token])
                    for token in tokens
                    if token not in unfixed_tokens
                ]
            )
        )

        return tokens

    @staticmethod
    def recover_segmented_words(raw_input: str, max_len: int = 5) -> str:
        """This algorithm processes and input text to detect and fix any malformed words.

        Example:
            input: "million p rote c te d   by u n h c r Of the world's displaced"
            output: "million protected by unhcr Of the world's displaced"

        """

        alpha_streak = 0
        word_streak = 0
        val_span = ""
        temp_span = ""
        ends_space = False
        spaces = {" ", "\n", "\t"}

        # Handle plural form of acronyms, e.g., IDPs -> IDP
        raw_text = re.sub(r"(\W[A-Z]{2,})(s)(\W)", r"\1\3", raw_input)

        text = ""

        for i in raw_text:
            if i.isalpha():
                alpha_streak += 1
                temp_span += i
                ends_space = False
            else:
                if (alpha_streak and alpha_streak <= max_len) or (
                    val_span and ends_space
                ):
                    if i in spaces:
                        val_span += temp_span + i
                        word_streak += 1
                        temp_span = ""
                        ends_space = True  # Speeds up processing vs. using val_span[-1].isspace()!
                        alpha_streak = 0
                        continue

                if word_streak >= 2:
                    text += " ".join(wordninja.split("".join(val_span.split())))
                    text += " " + temp_span + i
                else:
                    text += val_span + temp_span + i

                word_streak = 0
                temp_span = ""
                val_span = ""
                ends_space = False
                alpha_streak = 0

        return text
