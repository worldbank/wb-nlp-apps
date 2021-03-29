import re
import enchant
from wb_nlp import dir_manager
en_dict = enchant.Dict("en_US")
VALID_TOKEN_PAT = re.compile('^[a-z]+$')

with open(dir_manager.get_data_dir("whitelists", "whitelists", "wordfreq-enwiki-latest-pages-articles.xml.bz2.txt")) as fl:
    with open(dir_manager.get_data_dir("whitelists", "whitelists", "wordfreq-enwiki-latest-pages-articles.xml.bz2.pwl.txt"), "w") as wfl:
        with open(dir_manager.get_data_dir("whitelists", "whitelists", "wordfreq-enwiki-latest-pages-articles.xml.bz2.non_en.txt"), "w") as nfl:

            for l in fl:
                w, c = l.strip().split()
                if VALID_TOKEN_PAT.match(w):
                    wfl.write(w.strip() + "\n")
                if not en_dict.check(w):
                    nfl.write(w.strip() + "\n")
