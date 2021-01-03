import re
from scipy.stats import beta
import numpy as np
import pandas as pd
import enchant
from langdetect import detector_factory
import langdetect
with open('/home/avsolatorio/Downloads/multi-language.txt', 'rb') as fl:
    txt = fl.read().decode('utf-8', errors='ignore')
from nltk import sent_tokenize
% % time
sents = sent_tokenize(txt)

non_en = []
for i in sents:
    try:
        if langdetect.detect(i) != 'en'':
            non_en.append(i)
    except:
        continue

# for f in fr[:10]:
#     print(f)
% % time
sents = sent_tokenize(txt)

non_en = []
for i in sents:
    try:
        if langdetect.detect(i) != 'en':
            non_en.append(i)
    except:
        continue

# for f in fr[:10]:
#     print(f)
non_en[:10]
non_en[:50]
for j in non_en[:50]:
    print(j)
sents[:10]
sents[0]
langdetect.detect_langs(sents[0])
langdetect.detect_langs(sents[1])
langdetect.detect_langs(sents[2])
langdetect.detect_langs(sents[3])
langdetect.detect_langs(sents[4])
sents[100]
sents[200]
sents[150]
langdetect.detect_langs(sents[150])
langdetect.detect_langs(sents[150].replace(' ', ''))
langdetect.detect_langs(sents[151])
sents[130]
sents[120]
sents[125]
langdetect.detect_langs(sents[125])
langdetect.detect_langs(sents[126])
langdetect.detect_langs(sents[127])
s = sents[126]
langdetect.detect_langs(s)
s
print("hello world"
      "the word is hello."
      "Testing multi-line print.")
print("hello world.\n"
      "the word is hello.\n"
      "Testing multi-line print.")
factory = detector_factory.init_factory()
_factory = None
detector_factory.init_factory()
_factory
factory = DetectorFactory()factory.load_profile(detector_factory.PROFILES_DIRECTORY)
factory = detector_factory.DetectorFactory()
factory.load_profile(detector_factory.PROFILES_DIRECTORY)
detector = factory.create()
detector._extract_ngrams()
s
detector.append(s)
detector._extract_ngrams()
detector.word_lang_prob_map['pt']
detector.word_lang_prob_map['refugee']
detector.word_lang_prob_map['refu']
detector.word_lang_prob_map['ref']
detector.word_lang_prob_map['gee']
detector.BASE_FREQ
en_dict = enchant.Dict('en_US')
en_dict.check(s)
en_dict.add?
en_dict(s.split())
en_dict.check(s.split())
s[0]
s.split()
len(filter(en_dict.check, s.split()))
len(list(filter(en_dict.check, s.split())))
len(list(filter(en_dict.check, s.split()))) / len(s)
len(list(filter(en_dict.check, sents[0].split()))) / len(s)
len(list(filter(en_dict.check, sents[100].split()))) / len(s)
len(list(filter(en_dict.check, sents[80].split()))) / len(s)
sents[80]
len(list(filter(en_dict.check, sents[90].split()))) / len(s)
sents[90]
len(list(filter(en_dict.check, sents[20].split()))) / len(s)
len(list(filter(en_dict.check, sents[100].split()))) / len(s)
sents[100]
sents[100].split()
len(list(filter(en_dict.check, sents[100].lower().split()))) / len(s)
sents[100].lower().split()
en_dict.check('reached')
en_dict.check('population')
s = sents[100]
len(list(filter(en_dict.check, s.lower().split()))) / len(s.lower().split())
# s = sents[idx]; len(list(filter(en_dict.check, s.lower().split()))) / len(s.lower().split())
idx = 120
s = sents[idx]
len(list(filter(en_dict.check, s.lower().split()))) / len(s.lower().split())
idx = 150
s = sents[idx]
len(list(filter(en_dict.check, s.lower().split()))) / len(s.lower().split())
s
s.split()
len(s.lower().split())
19 * 0.31
s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
len(list(filter(en_dict.check, s))) / len(s)
s
idx = 20
s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
len(list(filter(en_dict.check, s))) / len(s)
idx = 30
s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
len(list(filter(en_dict.check, s))) / len(s)
idx = 60
s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
len(list(filter(en_dict.check, s))) / len(s)
s
en_dict.check('60')
en_dict.check('60234')
en_dict.check('....')
en_dict.check('...@#.')
en_dict.check('...@.')
en_dict.check('viii')
en_dict.check('page')
langdetect.detect(' '.join(s))
idx = 30
s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
len(list(filter(en_dict.check, s))) / len(s)
s
langdetect.detect(' '.join(s))
idx = 125
s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
len(list(filter(en_dict.check, s))) / len(s)
s
langdetect.detect(' '.join(s))
idx = 126
s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
len(list(filter(en_dict.check, s))) / len(s)
s
idx = 127
s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
len(list(filter(en_dict.check, s))) / len(s)
s
non_en_spell = []
for idx in range(len(sent)):
    s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
    prop = len(list(filter(en_dict.check, s))) / len(s)
    non_en_spell.append({'sent': sents[idx], 'score': prop})
for idx in range(len(sents)):
    s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
    prop = len(list(filter(en_dict.check, s))) / len(s)
    non_en_spell.append({'sent': sents[idx], 'score': prop})
for idx in range(len(sents)):
    s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
    if not s:
        continue
    prop = len(list(filter(en_dict.check, s))) / len(s)
    non_en_spell.append({'sent': sents[idx], 'score': prop})
non_en_spell_df = pd.DataFrame(non_en_spell)
non_en_spell_df
non_en_spell_df['score'].describe()
len(sents)
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values('score')
non_en_spell_df[non_en_spell_df['score'] <
                0.5].sort_values('score', ascending=False)
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head()['sent']
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head()['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head(20).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head(30).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head(40).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head(50).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head(60).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head(70).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head(80).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head(90).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head(100).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.8].sort_values(
    'score', ascending=False).head(10).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.7].sort_values(
    'score', ascending=False).head(10).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.6].sort_values(
    'score', ascending=False).head(10).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head(10).tail(10)['sent'].values
non_en_spell = []
for idx in range(len(sents)):
    s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
    if not s:
        continue
    n = len(s)
    a = len(list(filter(en_dict.check, s)))
    b = n - a
    non_en_spell.append({'sent': sents[idx], 'score': prop, 'a': a, 'b': b})
non_en_spell_df = pd.DataFrame(non_en_spell)
non_en_spell_df['a']
non_en_spell_df['b']
non_en_spell_df['score'].mean()
non_en_spell_df['score'].std()
non_en_spell_df['score'].describe()
non_en_spell = []
for idx in range(len(sents)):
    s = list(filter(lambda x: len(x) > 1, sents[idx].lower().split()))
    if not s:
        continue
    n = len(s)
    a = len(list(filter(en_dict.check, s)))
    b = n - a
    non_en_spell.append({'sent': sents[idx], 'score': a/n, 'a': a, 'b': b})
non_en_spell_df = pd.DataFrame(non_en_spell)
non_en_spell_df['score'].mean()
non_en_spell_df['score'].std()
non_en_spell_df['score'].hist()
np.histogram(non_en_spell_df['score'])
np.histogram(non_en_spell_df['score'], bins=20)
np.histogram(non_en_spell_df['score'], bins=50)
np.histogram(non_en_spell_df['score'], bins=20)
non_en_spell = []
for idx in range(len(sents)):
    s = list(filter(lambda x: len(x) > 1 and s.isalpha(),
                    sents[idx].lower().split()))
    if not s:
        continue
    n = len(s)
    a = len(list(filter(en_dict.check, s)))
    b = n - a
    non_en_spell.append({'sent': sents[idx], 'score': a/n, 'a': a, 'b': b})
non_en_spell = []
for idx in range(len(sents)):
    s = list(filter(lambda x: len(x) > 1 and x.isalpha(),
                    sents[idx].lower().split()))
    if not s:
        continue
    n = len(s)
    a = len(list(filter(en_dict.check, s)))
    b = n - a
    non_en_spell.append({'sent': sents[idx], 'score': a/n, 'a': a, 'b': b})
non_en_spell = []
for idx in range(len(sents)):
    s = list(filter(lambda x: len(x) > 1 and x.isalpha(),
                    sents[idx].lower().split()))
    if not s:
        continue
    n = len(s)
    a = len(list(filter(en_dict.check, s)))
    b = n - a
    non_en_spell.append({'sent': sents[idx], 'score': a/n, 'a': a, 'b': b})
non_en_spell_df = pd.DataFrame(non_en_spell)
non_en_spell_df['score'].mean()
np.histogram(non_en_spell_df['score'], bins=20)
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head(10).tail(10)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.6].sort_values(
    'score', ascending=False).head(5).tail(5)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.75].sort_values(
    'score', ascending=False).head(5).tail(5)['sent'].values
en_dict.suggest('shortterm')
non_en_spell_df[non_en_spell_df['score'] < 0.75].sort_values(
    'score', ascending=False).head(5).tail(5)['sent'].values[-1]
non_en_spell_df[non_en_spell_df['score'] < 0.75].sort_values(
    'score', ascending=False).head(5).tail(5)['sent'].values[-1].split()
non_en_spell_df[non_en_spell_df['score'] < 0.75].sort_values(
    'score', ascending=False).head(5).tail(5)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.75].sort_values(
    'score', ascending=False).head(10).tail(5)['sent'].values
non_en_spell_df[non_en_spell_df['score'] < 0.8].sort_values(
    'score', ascending=False).head(10).tail(5)['sent'].values
np.histogram(non_en_spell_df['score'], bins=20)
non_en_spell_df['score'].median()
non_en_spell_df[['score', 'a', 'b']].mean()
np.random.beta(21, b)
np.random.beta(21, 3)
np.random.beta(21, 3)
np.random.beta(21, 3)
np.random.beta(21, 3)
np.random.beta(21, 3)
non_en_spell_df.head()
non_en_spell_df[non_en_spell_df['score'] < 0.3].sort_values(
    'score', ascending=False).head(10).tail(5)
np.random.beta(21+10, 3+24)
beta(21, 3)
rvb = beta(21, 3)
mean, var, skew, kurt = beta.stats(21, 3, moments='mvsk')
var
mean
var ** 0.05
var ** 0.5
mean - (var ** 0.5)
non_en_spell_df[non_en_spell_df['score'] < 0.5].sort_values(
    'score', ascending=False).head(10).tail(5)
non_en_spell_df[non_en_spell_df['score'] < 0.8].sort_values(
    'score', ascending=False).head(10).tail(5)
non_en_spell_df[non_en_spell_df['score'] < 0.8].sort_values(
    'score', ascending=False).head(10).tail(5).values
beta.stats(21 + 14, 3 + 4, moments='mvsk')
beta.stats(21 + 7, 3 + 2, moments='mvsk')
0.0037 ** 0.5
beta.cdf(10, 21, 3)
beta.cdf(0.4, 21, 3)
beta.cdf(0.6, 21, 3)
beta.cdf(0.7, 21, 3)
beta.cdf(0.8, 21, 3)
beta.cdf(0.76, 21, 3)
beta.cdf(0.75, 21, 3)
non_en_spell_df[['score', 'a', 'b']].mean()
beta.cdf(0.75, 21.897786, 3.115410)
beta.cdf(0.6, 21.897786, 3.115410)
beta.cdf(0.8, 21.897786, 3.115410)
beta.cdf(0.76, 21.897786, 3.115410)
beta.cdf(0.755, 21.897786, 3.115410)
beta.cdf(0.753, 21.897786, 3.115410)
beta.cdf(0.754, 21.897786, 3.115410)
beta.cdf(0.755, 21.897786, 3.115410)
beta.cdf(0.7545, 21.897786, 3.115410)
rvb.cdf(10)
rvb.cdf(0.7545)
rvb.cdf(0.753)
non_en_spell_df['pval'] = non_en_spell_df['score'].map(rvb.cdf)
non_en_spell_df.head()
non_en_spell_df[non_en_spell_df['pval'] < 0.05].head()
non_en_spell_df[non_en_spell_df['pval'] < 0.05].sort_values(
    'pval', ascending=False).head()
non_en_spell_df[non_en_spell_df['pval'] <= 0.05].sort_values(
    'pval', ascending=False).head()

alpha_pattern = re.compile('[a-z]+')
non_en_spell = []
for idx in range(len(sents)):
    tokens = alpha_pattern.findall(sents[idx].lower())
    s = list(filter(lambda x: len(x) > 1 and x.isalpha(),
                    tokens))
    if not s:
        continue
    n = len(s)
    a = len(list(filter(en_dict.check, s)))
    b = n - a
    non_en_spell.append({'sent': sents[idx], 'score': a/n, 'a': a, 'b': b})

non_en_spell_df = pd.DataFrame(non_en_spell)
means = non_en_spell_df[['score', 'a', 'b']].mean()
non_en_spell_df['pval'] = non_en_spell_df['score'].map(rvb.cdf)
non_en_spell_df[non_en_spell_df['pval'] <= 0.05].sort_values(
    'pval', ascending=False).head()
non_en_spell_df[non_en_spell_df['pval'] <= 0.05].sort_values(
    'pval', ascending=False).head()['sent'].values
non_en_spell_df[non_en_spell_df['pval'] <= 0.05].sort_values(
    'pval', ascending=False).head(20)['sent'].values
non_en_spell_df[non_en_spell_df['pval'] <= 0.05].sort_values(
    'pval', ascending=False).head(20).values
non_en_spell_df[non_en_spell_df['pval'] <= 0.05].sort_values(
    'pval', ascending=False).head(30).tail(10).values
re.match('\S*-\S*', 'hello -\r\ndsf')
re.match('\s*-\s*', 'hello -\r\ndsf')
re.search('\s*-\s*', 'hello -\r\ndsf')
re.search('\S*-\s*', 'hello -\r\ndsf')
re.search('\s*-\s*', 'hello -\r\ndsf')
re.sub('\s*-\s*', '',  'hello -\r\ndsf')
alpha_pattern = re.compile(r'[a-z]+')
dash_sub = re.compile(r'\s*-\s*')
non_en_spell = []
for idx in range(len(sents)):
    s = dash_sub.sub('', sents[idx].lower())
    tokens = alpha_pattern.findall(sents[idx].lower())
    s = list(filter(lambda x: len(x) > 1 and x.isalpha(),
                    tokens))
    if not s:
        continue
    n = len(s)
    a = len(list(filter(en_dict.check, s)))
    b = n - a
    non_en_spell.append({'sent': sents[idx], 'score': a/n, 'a': a, 'b': b})

non_en_spell_df = pd.DataFrame(non_en_spell)
means = non_en_spell_df[['score', 'a', 'b']].mean()
rvb = beta(means['a'], means['b'])
non_en_spell_df['pval'] = non_en_spell_df['score'].map(rvb.cdf)
non_en_spell_df[non_en_spell_df['pval'] <= 0.05].sort_values(
    'pval', ascending=False).head(30).tail(10).values
alpha_pattern = re.compile(r'[a-z]+')
dash_sub = re.compile(r'\s*-\s*')
non_en_spell = []
for idx in range(len(sents)):
    ssub = dash_sub.sub('', sents[idx].lower())
    tokens = alpha_pattern.findall(ssub)
    s = list(filter(lambda x: len(x) > 1 and x.isalpha(),
                    tokens))
    if not s:
        continue
    n = len(s)
    a = len(list(filter(en_dict.check, s)))
    b = n - a
    non_en_spell.append(
        {'sent': sents[idx], 'clean': ssub, 'score': a/n, 'a': a, 'b': b})

non_en_spell_df = pd.DataFrame(non_en_spell)
means = non_en_spell_df[['score', 'a', 'b']].mean()
rvb = beta(means['a'], means['b'])
non_en_spell_df['pval'] = non_en_spell_df['score'].map(rvb.cdf)
non_en_spell_df[non_en_spell_df['pval'] <= 0.05].sort_values(
    'pval', ascending=False).head(30).tail(10).values
non_en_spell_df[non_en_spell_df['pval'] <= 0.07].sort_values(
    'pval', ascending=False).head(30).tail(10).values
non_en_spell_df[non_en_spell_df['pval'] <= 0.10].sort_values(
    'pval', ascending=False).head(30).tail(10).values
beta(means['a'] + 6, means['b'] + 2)
beta(means['a'] + 6, means['b'] + 2).mean()
beta(means['a'] + 6, means['b'] + 2).std()
non_en_spell_df[non_en_spell_df['pval'] <= 0.05].sort_values(
    'pval', ascending=False).head(30).tail(10).values
beta(means['a'] + 4, means['b'] + 2).std()
beta(means['a'] + 4, means['b'] + 2).mean()
beta(means['a'] + 22, means['b'] + 10).mean()
rbv.cdf(0.7656)
rvb.cdf(0.7656)
non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head()
non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head().values
' '.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head().values)
print(' '.join(
    non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head().values))
print(' '.join(
    non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(20).values))
non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head().values
non_en_spell_df[non_en_spell_df['pval'] > 0.05].head().values
non_en_spell_df[non_en_spell_df['pval'] > 0.05].head(20).values
print(' '.join(
    non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(20).values))
print(' '.join(
    non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(50).values))
print(' '.join(
    non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(100).values))
print(' '.join(non_en_spell_df[non_en_spell_df['pval']
                               > 0.05]['sent'].head(150).tail(60).values))
print(' '.join(
    non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(100).values))
print(' '.join(non_en_spell_df[non_en_spell_df['pval']
                               > 0.05]['sent'].head(150).tail(60).values))
alpha_pattern = re.compile(r'[a-z]+')
dash_sub = re.compile(r'\s*-\s*')
non_en_spell = []
# sents = sent_tokenize(txt)
sents = sents.split('\n')
for idx in range(len(sents)):
    ssub = dash_sub.sub('', sents[idx].lower())
    tokens = alpha_pattern.findall(ssub)
    s = list(filter(lambda x: len(x) > 1 and x.isalpha(),
                    tokens))
    if not s:
        continue
    n = len(s)
    a = len(list(filter(en_dict.check, s)))
    b = n - a
    non_en_spell.append(
        {'sent': sents[idx], 'clean': ssub, 'score': a/n, 'a': a, 'b': b})

non_en_spell_df = pd.DataFrame(non_en_spell)
means = non_en_spell_df[['score', 'a', 'b']].mean()
rvb = beta(means['a'], means['b'])
non_en_spell_df['pval'] = non_en_spell_df['score'].map(rvb.cdf)
alpha_pattern = re.compile(r'[a-z]+')
dash_sub = re.compile(r'\s*-\s*')
non_en_spell = []
# sents = sent_tokenize(txt)
sents = txt.split('\n')
for idx in range(len(sents)):
    ssub = dash_sub.sub('', sents[idx].lower())
    tokens = alpha_pattern.findall(ssub)
    s = list(filter(lambda x: len(x) > 1 and x.isalpha(),
                    tokens))
    if not s:
        continue
    n = len(s)
    a = len(list(filter(en_dict.check, s)))
    b = n - a
    non_en_spell.append(
        {'sent': sents[idx], 'clean': ssub, 'score': a/n, 'a': a, 'b': b})

non_en_spell_df = pd.DataFrame(non_en_spell)
means = non_en_spell_df[['score', 'a', 'b']].mean()
rvb = beta(means['a'], means['b'])
non_en_spell_df['pval'] = non_en_spell_df['score'].map(rvb.cdf)
print(' '.join(non_en_spell_df[non_en_spell_df['pval']
                               > 0.05]['sent'].head(150).tail(60).values))
len(sents)
non_en_spell_df.head()
means
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    150).tail(60).values))
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    100).tail(60).values))
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    100).tail(100).values))
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    300).tail(100).values))
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    250).tail(100).values))
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    100).tail(100).values))
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    150).tail(100).values))
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    150).tail(100).values))
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    250).tail(100).values))
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    350).tail(100).values))
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    450).tail(100).values))
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    550).tail(100).values))
print('\n'.join(non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(
    650).tail(100).values))
langdetect.detect_langs(
    """tee oP'p 11I tluatendaufooneeoutrtdbotEtiss-d Relet- Pu-ey I.-on   1e-n  (US1 peP capital - t-ban and rural""")
non_en_spell_df['score'].describe()
non_en_spell_df['score'].quantile(0.05)
non_en_spell_df['score'].quantile(0.95)
print('\n'.join(
    non_en_spell_df[non_en_spell_df['pval'] > 0.05]['sent'].head(650).tail(100)))
for j in enumerate(3):
    print(j)
t = [1, 3, 4]
for j in enumerate(len(t)):
    print(j)


def filter_document_by_language(txt, pval=0.05):
    '''Remove contents of documents that are unlikely to be in English.

    This uses statistical hypothesis testing to automate the removal of tokens.
    '''

    alpha_pattern = re.compile(r'[a-z]+')
    dash_sub = re.compile(r'\s*-\s*')
    non_en_spell = []
    # sents = sent_tokenize(txt)
    sents = txt.split('\n')
    for idx in range(len(sents)):
        ssub = dash_sub.sub('', sents[idx].lower())
        tokens = alpha_pattern.findall(ssub)

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
            {'sent': sents[idx], 'clean': ssub, 'score': a/n, 'a': a, 'b': b})

    non_en_spell_df = pd.DataFrame(non_en_spell)
    means = non_en_spell_df[['score', 'a', 'b']].mean()
    rvb = beta(means['a'], means['b'])
    non_en_spell_df['pval'] = non_en_spell_df['score'].map(rvb.cdf)

    return '\n'.join(non_en_spell_df[non_en_spell_df['pval'] > pval]['sent'])


clean_doc = filter_document_by_language(txt)
len(clean_doc)
print(clean_doc[:1000])
print(clean_doc[:10000])
print(clean_doc[:100000])
alpha_pattern.findall(
    'En el sector de la educaci6n, las principales prioridades son las')
alpha_pattern.findall(
    'En el sector de la educaci6n, las principales prioridades son las'.lower())
tokens = alpha_pattern.findall(
    'En el sector de la educaci6n, las principales prioridades son las'.lower())
candidate_tokens = list(filter(lambda x: len(x) > 1 and x.isalpha(),
                               tokens))
candidate_tokens
len(list(filter(en_dict.check, candidate_tokens)))
len(candidate_tokens)
7/11
tokens = alpha_pattern.findall('En el sector de la educaci6n, las principales prioridades son las'.lower())    alpha_pattern = re.compile(r'[a-z]+')
dash_sub = re.compile(r'\s*-\s*')
 non_en_spell = []
  # sents = sent_tokenize(txt)
  sents = txt.split('\n')
   for idx in range(len(sents)):
        ssub = dash_sub.sub('', sents[idx].lower())
        tokens = alpha_pattern.findall(ssub)

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
            {'sent': sents[idx], 'clean': ssub, 'score': a/n, 'a': a, 'b': b})

    non_en_spell_df = pd.DataFrame(non_en_spell)
    means = non_en_spell_df[['score', 'a', 'b']].mean()
    rvb = beta(means['a'], means['b'])
    non_en_spell_df['pval'] = non_en_spell_df['score'].map(rvb.cdf)
    alpha_pattern = re.compile(r'[a-z]+')
    dash_sub = re.compile(r'\s*-\s*')
    non_en_spell = []
    # sents = sent_tokenize(txt)
    sents = txt.split('\n')
    for idx in range(len(sents)):
        ssub = dash_sub.sub('', sents[idx].lower())
        tokens = alpha_pattern.findall(ssub)

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
            {'sent': sents[idx], 'clean': ssub, 'score': a/n, 'a': a, 'b': b})

    non_en_spell_df = pd.DataFrame(non_en_spell)
    means = non_en_spell_df[['score', 'a', 'b']].mean()
    rvb = beta(means['a'], means['b'])
    non_en_spell_df['pval'] = non_en_spell_df['score'].map(rvb.cdf)
non_en_spell_df[non_en_spell_df['sent'].str.contains(
    'En el sector de la educaci6n, las principales prioridades son las')]
rvb.cdf(0.63)
rvb.cdf(0.636364)
langdetect.detect_langs(
    "initialement plus faible et l'incertitude relative & l'evolution a plus")
langdetect.detect_langs
langdetect.detect_langs(
    'En el sector de la educaci6n, las principales prioridades son las')
means
rvb
rvb.alpha
rvb.a
rvb.b
means['a']
rvb.args
rvb.mean()
rvb.std
rvb.std()
7.7 + 1.3
beta(4.5, 4.5)
beta(4.5, 4.5).mean()
beta(4.5, 4.5).std()
rvb.cdf(0.7)
beta(9, 0).std()
beta(9, 0.01).std()
beta(9, 0.001).std()
beta(9, 0.001).cdf(0.9)
beta(9, 0.001).cdf(0.8)
beta(9, 0.001).cdf(0.99)
beta(9, 0.001).cdf(0.995)
beta(9, 0.001).cdf(0.999)
beta(9, 0.001).cdf(0.9999)
