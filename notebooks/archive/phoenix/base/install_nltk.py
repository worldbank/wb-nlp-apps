import nltk


for token in ("stopwords", "wordnet", "wordnet_ic", "sentiwordnet", "punkt"):
    nltk.download(token)
