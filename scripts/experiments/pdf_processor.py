import re
import spacy
import nltk
from haystack.preprocessor.preprocessor import PreProcessor
from haystack.file_converter.pdf import PDFToTextConverter
from haystack.file_converter.pdf import PDFToTextConverter, PreProcessor
In[89]: % history
fname = 'WDR 2013 low res.pdf'
converter = PDFToTextConverter(
    remove_numeric_tables=True, valid_languages=["de", "en"])
%time doc = converter.convert(file_path=fname, meta=None)
converter = PDFToTextConverter(
    remove_numeric_tables=True, valid_languages=["de", "en"])
%time doc = converter.convert(file_path=fname, meta=None)
processor = PreProcessor(clean_empty_lines=True,
                         clean_whitespace=True,
                         clean_header_footer=True,
                         split_by="word",
                         split_length=200,
                         split_respect_sentence_boundary=True)
d = processor.process(doc)
d[0]
d[1]
print()d[1]
print(d[1])
print(d[1]['text'])
print(d[1]['text'])
doc['text'][:1000]
print(doc['text'][:1000])
dd = doc['text'].splitlines()
dd[0]
dd[1]
dd[2]
dd[3]
dd[4]
dd[5]
dd[6]
dd[:10]
dd[:100]
print(d[1]['text'])
print(d[10]['text'])
print(d[50]['text'])
nltk.sent_tokenize(d[50]['text'])
len(nltk.sent_tokenize(d[50]['text']))
len(nltk.sent_tokenize(d[50]['text'].replace('\n', ' ')))
nltk.sent_tokenize(d[50]['text'].replace('\n', ' '))
nltk.sent_tokenize(d[50]['text'].replace('\n', ' ').replace('.', '. '))
nltk.sent_tokenize(d[90]['text'].replace('\n', ' ').replace('.', '. '))
nltk.sent_tokenize(d[90]['text'])
doc['text']
dc = processor.clean(doc)
dc[0]
dc['text'][:100]
doc['text'][:100]
print(dc['text'][1000:2000])
print(doc['text'][1000:2000])
print(doc['text'][5000:6000])
print(doc['text'][10000:11000])
print(doc['text'][20000:21000])
print(doc['text'][27000:28000])
print(doc['text'][37000:38000])
print(dc['text'][37000:38000])
print(doc['text'][37000:38000])
sentences = nltk.sent_tokenize(dc['text'][37000:38000])
len(sentences)
sentences
nlp = spacy.load('en_core_web_md')
nlp = spacy.load('en_core_web_sm')
doc = nlp(dc['text'][37000:38000])
doc.sents
for s in doc.sents:
    print(s)
for s in doc.sents:
    print(s)
[s for s in doc.sents]
len([s for s in doc.sents])
len([s.replace('\n', ' ') for s in doc.sents])
len([s.text.replace('\n', ' ') for s in doc.sents])
[s.text.replace('\n', ' ') for s in doc.sents]
sentences
sents = nltk.sent_tokenize(doc['text'])
%time doc = converter.convert(file_path=fname, meta=None)
sents = nltk.sent_tokenize(doc['text'])
len(sents)
sents[100:110]
sents[:100]
%time doc = converter.convert(file_path=fname, meta=None)
doc['text'][:100]
sents[:10]
sents = nltk.sent_tokenize(doc['text'])
sents[:10]
print(sents[0])
print(sents[0].replace('\n', ' '))
print(sents[0].replace('\n', ' ').strip())
for s in sents:
    print(s.replace('\n', ' ').strip())
    print()
for s in sents:
    print(s.replace('\n', ' ').strip())
    print()
for s in sents:
    print(s.replace('\n', ' ').strip())
    print('------------------------------------')
for s in sents[:500]:
    print(s.replace('\n', ' ').strip())
    print('------------------------------------')
   def normalize_footnote_citations(text: str) -> str:
        r"""This method tries to detect footnotes and normalizes them.

        This is essential to improve the accuracy of SpaCy's sentence
        detector. Sometimes footnote citations are connected with sentence
        endings that prevents the detection of proper sentence boundary.

        The transformation handles common footnote citation formats:
            pattern: ((?:[a-zA-Z\)]+[.,]|\)))(\d+)(\s)
                - This is a normalizer.1 We will use this.
                - This is a normalizer (great).2 We will use this.
                - This is a normalizer (great).3\nWe will use this.
                - The normalizer (2020)8 is working.
            transforms to:
                - This is a normalizer. _1 We will use this.
                - This is a normalizer (great). _2 We will use this.
                - This is a normalizer (great). _3\nWe will use this.
                - The normalizer (2020) _8 is working.

        Args:
            text:
                Text that will be checked and normalized for footnote
                citations.

        Returns:
            normalized text

        """
        footnote_patterns = [
            r'((?:[a-zA-Z\)]+[.,]|\)))(\d+)(\s)'
        ]

        footnote_patterns = '|'.join(footnote_patterns)

        return re.sub(footnote_patterns, r'\1 _\2\3', text)
%time sents = nltk.sent_tokenize(doc['text'])
%time sents = nltk.sent_tokenize(normalize_footnote_citations(doc['text']))
for s in sents[:500]:
    print(s.replace('\n', ' ').strip())
    print('------------------------------------')
%history
