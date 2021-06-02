import re
import enchant
import pandas as pd
from scipy.stats import beta


def filter_document_by_language(txt, pval=0.05, en_dict=enchant.Dict("en_US"), return_en=True, return_df=False):
    '''Remove contents of documents that are unlikely to be in English.

    This uses statistical hypothesis testing to automate the removal of tokens.

    Other formulation:
    compute overlap in distribution of average (a, b) and the sentence.
    '''

    # delta = np.finfo(np.float).tiny
    delta = 1
    alpha_pattern = re.compile(r'[a-z]+')
    # In case a word is cut in newline
    newline_dash_sub = re.compile(r'(\S*)-\s+(\S*)')
    non_en_spell = []
    # sents = sent_tokenize(txt)
    txt = newline_dash_sub.sub(r'\1\2', txt)
    sents = txt.split('\n')
    for idx in range(len(sents)):
        sent = sents[idx].lower()
        tokens = alpha_pattern.findall(sent)

        candidate_tokens = list(filter(lambda x: len(x) > 1 and x.isalpha(),
                                       tokens))
        if not candidate_tokens:
            continue
        # Total number of tokens
        n = len(candidate_tokens)
        # number of success -> alpha parameter for the beta distribution.
        a = len(list(filter(en_dict.check, candidate_tokens)))
        # number of failures -> beta parameter for the beta distribution.
        b = n - a

        non_en_spell.append(
            {'sent': sents[idx], 'clean': sent, 'score': a/n, 'a': a, 'b': b})

    non_en_spell_df = pd.DataFrame(non_en_spell)
    if non_en_spell_df.empty:
        return None

    means = non_en_spell_df[['score', 'a', 'b']].mean()
    rvb = beta(means['a'] + delta, means['b'] + delta)
    non_en_spell_df['pval'] = non_en_spell_df['score'].map(rvb.cdf)

    if return_df:
        return non_en_spell_df

    if return_en:
        filter_set = non_en_spell_df['pval'] > pval
    else:
        filter_set = non_en_spell_df['pval'] <= pval

    return '\n'.join(non_en_spell_df[filter_set]['sent'])
