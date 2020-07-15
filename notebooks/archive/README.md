# Document Semantic Similarity Project



This project applies NLP techniques to build a semantic similarity engine that can identify similar documents from a corpus. Scripts for acquiring data, processing and cleaning the raw documents, generation of metadata, e.g., country and acronyms, training the models are available.

The project is structured as follows:


```
ROOT
├── APP
│   ├── frontend
│   ├── services
│   └── views
├── CORPUS
│   ├── <CORPUS_ID>
│   │   ├── PDF
│   │   ├── TXT_CLEAN
│   │   └── TXT_ORIG
├── MODELS
│   ├── LDA
│   │   └── <CORPUS_ID>-<model_id>
│   │       ├── data
│   │       └── mallet
│   └── WORD2VEC
│       ├── <CORPUS_ID>-<model_id>
│       │   └── data
├── SCRIPTS
│   ├── acronyms
│   ├── cleaner
│   ├── logs
│   ├── models
│   │   ├── lda
│   │   ├── lsa
│   │   ├── Mallet
│   │   └── word2vec
│   ├── ngrams
│   ├── pdf2text
│   ├── TIKA
│   └── whitelists
```


## Corpus

The `CORPUS` directory contains data acquired from different sources. Scripts to scrape or collect data from APIs are implemented for each corpus and can be found in the `SCRIPTS` directory. Text and pdf type documents can be collected as part of the corpus and must be stored in `CORPUS/<CORPUS_ID>/TXT_ORIG` and `CORPUS/<CORPUS_ID>/PDF`, respectively. 

The contents of the `CORPUS/<CORPUS_ID>/PDF` directory are converted into text by running scripts found in `SCRIPTS/pdf2text` (currently implemented for the IMF corpus). The converted texts are saved in the `CORPUS/<CORPUS_ID>/TXT_ORIG` directory. The same directory is used for storing raw data of type text from arbitrary corpus.

## Preprocessing

Scripts to augment originally obtained metadata from the corpus source are implemented. There are currently two scripts performing:

- **Country detection** - detecting the presence of countries and regions in each document. This is implemented in the `SCRIPTS/country_detector.ipynb` notebook.
    - The country detector depends on the `SCRIPTS/whitelists/whitelist_countries_multilingual.csv` file.
    - The script generates a `CORPUS/<CORPUS_ID>/<corpus_id>_country_counts.csv` file.

- **Acronyms detection** - detecting the acronyms in the documents. This is implemented in the `SCRIPTS/acronyms/acronym_detector.ipynb`.
    - The script generates a `CORPUS/<CORPUS_ID>/<corpus_id>_detected_acronyms_prototypes.csv`.
    - Used to build a whitelist of acronyms as basis for later online replacement of acronyms into full versions.

## Cleaning

Raw texts from a corpus are cleaned. The following sequence of steps are done for each document:

- Load text from file (`CORPUS/<CORPUS_ID>/TXT_ORIG`)
- Text with length less than `ignore_length` (default=50) are skipped.
- Continuous whitespaces are normalized and treated as line breaks and replaced with a period (sentence stop).
- Lemmatization of the text is done with an option to use SpaCy or NLTK (default=SpaCy).
- A cleanup of the lemmatized text is performed.
    - Removal of tokens with character length greater than or equal to 25.
    - Removal of tokens having less than or equal to 2 characters.
- Check text if it still has content after the initial normalization; if not, then skip.
- Predict language of the text.
- Check if the language is in the list of supported languages (default=en) and has a language probability greater than a threshold (default=0.98).
- Perform spell check. The following tasks are executed:
    - Use enchant to identify valid and invalid tokens.
    - For invalid tokens, an inferencer for correction is executed to try to find a valid version if the token is misspelled.
    - Apply plural to singular mapping using the whitelist file `SCRIPS/whitelists/whitelist_replacements_plurals_to_singular.csv`.
    - Remove stopword lists.
- Output:
    - **lang**: Language detected and probability.
    - **tokens**: Number of tokens in the document after cleaning.
    - **text**: If no errors or exceptions, this will contain the cleaned text. If an error occurs in the process, the original text will be return.
    - **spell_errors**: Tokens that are misspelled or not in the dictionary.
    - **skipped**: Message for skipping the document.
    - **exception**: Errors encountered.
    - **write_status**: Flag indicating whether the returned text is clean or not. If `write_status` is `True`, then the text has been successfully cleaned.
- Note: Only documents with `write_status == True` should be included in the `CORPUS/<CORPUS_ID>/<corpus_id>_metadata_complete.csv` file.

Scripts for cleaning specific corpus are found in `SCRIPTS/cleaner`:
- `wb_data_cleaner.ipynb`
- `imf_data_cleaner.ipynb`

## N-grams detection

As part of preprocessing, an n-gram detector is used against the cleaned corpus. The detected ngrams will be stored in `CORPUS/<CORPUS_ID>/<corpus_id>_ngrams.csv` file. The ngram files for each corpus will be used to generate a master whitelist of ngrams. The master whitelist will be used during model training and online queries to dynamically convert individual tokens to their respective ngrams if present in the whitelist.

## Models

#### LDA

Run `SCRIPTS/models/lda/lda_training.ipynb` and set the proper `CORPUS_ID` element of `WB` and `IMF`.

#### Word2Vec

Run `SCRIPTS/models/word2vec/word2vec_training.ipynb` and set the proper `CORPUS_ID` element of `WB` and `IMF`.

#### LSA

Run `SCRIPTS/models/lsa/lsa_training.ipynb` and set the proper `CORPUS_ID` element of `WB` and `IMF`.Run `SCRIPTS/models/lsa/lsa_training.ipynb` and set the proper `CORPUS_ID` element of `WB` and `IMF`.


```python

```
