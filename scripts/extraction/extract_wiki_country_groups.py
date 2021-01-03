import requests
import pandas as pd
import spacy
from bs4 import BeautifulSoup


def extract_group_name(li):
    ch = list(li.children)
    if ch:
        group = ch[0]
    else:
        return None

    if group.name == 'a':
        return group.text
    elif ':' in group and ',' in group:
        if group.index(':') < group.index(','):
            return group.split(':')[0]
        else:
            return group.split(',')[0]
    elif ':' in group:
        return group.split(':')[0]
    elif ',' in group:
        return group.split(',')[0]

    return None


url = 'https://en.wikipedia.org/wiki/List_of_country_groupings'

nlp = spacy.load('en_core_web_sm')

wiki = requests.get(url)
soup = BeautifulSoup(wiki.content)

h2_list = soup.find_all('h2')

country_groups = []
undetected_groups = []


for h2 in h2_list:
    ul = h2.next_sibling.next_sibling
    if ul is None or ul.name != 'ul':
        continue

    li_list = ul.find_all('li')
    for li in li_list:
        group_name = extract_group_name(li)
        if group_name is None:
            undetected_groups.append(li.text)
        else:
            country_group = dict(
                group_name=group_name,
                countries=', '.join(list(map(str, filter(lambda ent: ent.label_ ==
                                                         'GPE' and ent.text[0].isupper(), nlp(li.text.replace('[', ' [').replace('.', ' .')).ents)))),
                orig=li.text
            )
            country_groups.append(country_group)

country_groups_df = pd.DataFrame(country_groups)
