# World Bank Knowledge for Change NLP Project

This repository contains all the codes and jupyter notebooks used to experiment and implement various NLP solutions to develop components for a document and data discovery application.

## About the Knowledge for Change (KCP) NLP Project

The objective of this KCP project is to address the knowledge discoverability issue that is common in traditional document databases. This project expects to catalyze the utility and use of the immense volume of knowledge on economic and social development stored across development organizations.  We will develop new data and data discovery products using state-of-the-art machine learning techniques and artificial intelligence models. These solutions will rely exclusively on open source software and algorithms.

The project will develop models that require a massive corpus and intensive computational resources. We aim to make these models easily accessible to organizations that will not have access to such resources. The outputs (scripts, search tools, and derived datasets) will be made openly accessible to allow adaptation and use in resource-constrained environments.

The scripts, codebase, and guidelines are also intended to be used as training materials.
<!--
### Addressable use cases

#### Search by topic composition

An environment economist is tasked to write a report on the impact of climate change on poverty. To address the “cold start” problem, s/he searches the World Bank document repository by setting thresholds on this specific combination of topics. The output of the topic models tells us that the share of topic 27 “climate change” in the available documents  ranges from 0 to 95%, and that the share of topic 12 “poverty” ranges from 0 to 52%. Setting a threshold on each topic (e.g., respectively 30% and 20%) will identify documents that cover both significantly (documents that are “at least” 30% about climate change and 20% about poverty). This approach returns more relevant documents, and a more relevant ranking of these documents, than what a keyword-based search, or filtering based on documents tags , would return. Additional filters (by country, year, others) could be applied as relevant.

![search-by-topic-composition](/docs/_static/img/search-by-topic-composition.png) -->

## Project components

The project is broken down into the following components:

- Web scraping and automation: `/src/wb_nlp/scraping`
- Metadata extraction: `/src/wb_nlp/processing/extraction`
- Document preprocessing and cleaning: `/src/wb_nlp/processing/cleaning`
- NLP modeling: `/src/wb_nlp/modeling`
- Application development: `/src/wb_nlp/app`

### Web scraping

The objective of this project is to use NLP models to learn topics, embedding, and other representations that could be useful for improving discoverability of documents. A major requirement for this undertaking is the availability of data that can be used to train machine learning models.

We aim to use web scraping and API access when possible to aggregate a large collection of documents. The document aggregation will focus on documents produced by international organizations and multilateral development banks to generate a specialized collection of economic and development centric corpus.

Technologies such as [Scrapy](https://scrapy.org/) and [NiFi](https://nifi.apache.org/), as well as vanilla implementations of API access are used to implement the web scraping part of the project.

### Metadata extraction

Useful metadata that are directly available from the source websites are also collected to enrich the information and expressivity of downstream features. We also implement various knowledge extraction modules designed to capture named entities and extract keywords from the documents to complement the originally published metadata. We are using [SpaCy](https://spacy.io/) and regex to power most of our knowledge extraction implementations.

Later, results from the NLP models will also be integrated into the metadata such as automatically learned LDA topics of documents, inferred topic classifications based on a model trained to predict topics from a predefined taxonomy, translated titles for non-english documents, etc.

### Document preprocessing and cleaning

Most of the raw data that we are using are in the form of PDF and text documents. We develop a suite of preprocessing and cleaning modules to handle the transformations required to generate a high quality input to our models.

An overview of the pipeline is as follows:
- Convert pdf to text
- Parse the text document and perform sentence tokenization.
- Lemmatize the tokens and remove stop words.
- Drop all non-alphabetical tokens.
- Apply spell check and try to recover misspelled words.
- Normalize tokens by converting to lowercase.

#### Phrase detection

Part of the preprocessing is also the inference of phrases in the documents. Phrases are logical grouping of tokens that represent an intrinsic meaning.

We are primarily leveraging the [Gensim](https://radimrehurek.com/gensim/) NLP toolkit and Spacy to develop the phrase detection algorithms.

#### Acronym detection

Acronyms are fairly common in documents from development organizations and multilateral development banks. In this project, we include in our pipeline an acronym detector and expander. The idea is to detect acronyms in a document and replace all of the acronyms with the appropriate expansion.

We also keep track of multiple instances of an acronym and generate prototypes for each that encodes the information of the acronym, e.g., PPP -> private-public partnership or purchasing power parity.

### NLP modeling

The above processes are precursor to generate inputs to the different NLP models. The NLP models are trained to generate derived data that could be used in downstream use-cases. Primarily, the models are unsupervised which are classified into two categories: topic models and embedding models.

#### Latent Dirichlet Allocation (LDA) topic model

The topic model employed in this project is an LDA implementation under the [Mallet](http://mallet.cs.umass.edu/topics.php) language toolkit. A Gensim wrapper is used as interface to interact with the original Java implementation.

The resulting topics learned by the model are used to characterize documents. With this, we build a search tool

#### Embedding models (word2vec)

The Gensim implementation for the word2vec model is used in this project. We extract the learned word embeddings and use them to represent documents by taking the mean of the word vectors in the document. This simple strategy allows us to have a semantic based search of documents using keywords or full document inputs.

## Guide for reproducibility

1. Upload the document metadata into the mongodb `nlp` database under the `docs_metadata` collection. Refer to [load_json_dump_to_db.py](/scripts/metadata/load_json_dump_to_db.py) for an example.

2. Configure the cleaning config file ([lda.yml](/configs/cleaning/lda.yml)) for the LDA model.

3. Run the [clean_corpus.py](/scripts/cleaning/clean_corpus.py) script to perform the cleaning of the documents to be used by the LDA model.

4. Configure the model config file ([lda/default.yml](/configs/models/lda/default.yml)) for the LDA model.

5. Run the [train_lda_model.py](/scripts/models/train_lda_model.py) to train the LDA model with the cleaned text.


## Alternative workflow

1. Upload the document metadata into the mongodb `nlp` database under the `docs_metadata` collection. Refer to [load_json_dump_to_db.py](/scripts/metadata/load_json_dump_to_db.py) for an example. Make sure that the `path_original` field corresponds to the path where the corresponding document is stored. Documents should ideally be stored following this convention: `/data/corpus/<corpus_id>/*.txt`.

2. Create a cleaning config based on the `/configs/cleaning/default.yml` and upload to mongodb at the `nlp/cleaning_configs` collection. It is recommended to add some description about the configuration in the `meta` field of the configuration file. You can use the `/scripts/configs/load_configs_to_db.py` script to load the configuration into the database.

3. To start the cleaning of the corpus, run the script `scripts/cleaning/clean_docs_from_db.py`. Provide the `cleaning_config_id` of the configuration that you want to use in cleaning the documents. This assumes that all the documents in the `docs_metadata` will be cleaned. The cleaning script will store the cleaned data at `/data/corpus/cleaned/<cleaning_config_id>/<corpus>/<file_name>`. The `file_name` and the `corpus` will be extracted from the metadata corresponding to the document in the `nlp/docs_metadata` collection.

## Training a model

### LDA

When you want to train an LDA model, you need to first generate a valid configuration. This configuration must be uploaded to mongodb under the `nlp/model_configs` collection. You can use the `/scripts/configs/load_configs_to_db.py` script to load the configuration into the database.

After the configuration is uploaded, select which cleaned documents (defined by the `cleaning_config_id`) will be used. Also provide the `model_config_id` that will be used for the model.

The script `scripts/models/train_lda_model_from_db.py` can be used to train an LDA model given a valid `cleaning_config_id` and `model_config_id`. Implemented in the script are the following steps:

1. Perform validity checks of the configuration. This is done by making sure that the `model_name = "lda"`. It also checks whether the version of the installed library matches with the one defined in the config. This reduces the likelihood of bugs in model training that may be introduced when updates in the implementation of the model occurs across different versions of the library.

2. Check whether the a processed corpus is already available. If yes, load it. Otherwise, create a dictionary to process the cleaned data. Then, create the corpus and save the dictionary and process the cleaned documents. Save all to disk so that there's no need to recreate the corpus.

3. Create a summary of the model run (`model_run_info`) to summarize the details of the experiment. This will be saved in mongodb for tracking of which models are available.

4. Train the model using the parameters in the `model_config`.

5. Save the model to disk and insert the `model_run_info` into the database.


## Instruction for contributors

Please read the [DEVELOPERS.md](/DEVELOPERS.md) for more details about the development workflow.
