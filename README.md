# World Bank Knowledge for Change NLP Project

This repository contains all the codes and jupyter notebooks used to experiment and implement various NLP solutions to develop components for a document and data discovery application.

## About the Knowledge for Change NLP Project

The project is broken down into the following components:

- Web scraping and automation: `/src/wb_nlp/scraping`
- Metadata extraction: `/src/wb_nlp/processing/extraction`
- Document preprocessing and cleaning: `/src/wb_nlp/processing/cleaning`
- NLP modeling: `/src/wb_nlp/modeling`
- Application development: `/src/wb_nlp/app`

## Web scraping

The objective of this project is to use NLP models to learn topics, embedding, and other representations that could be useful for improving discoverability of documents. A major requirement for this undertaking is the availability of data that can be used to train machine learning models.

We aim to use web scraping and API access when possible to aggregate a large collection of documents. The document aggregation will focus on documents produced by international organizations and multilateral development banks to generate a specialized collection of economic and development centric corpus.

Technologies such as [Scrapy](https://scrapy.org/) and [NiFi](https://nifi.apache.org/), as well as vanilla implementations of API access are used to implement the web scraping part of the project.

## Metadata extraction

Useful metadata that are directly available from the source websites are also collected to enrich the information and expressivity of downstream features. We also implement various knowledge extraction modules designed to capture named entities and extract keywords from the documents to complement the originally published metadata. We are using [SpaCy](https://spacy.io/) and regex to power most of our knowledge extraction implementations.

Later, results from the NLP models will also be integrated into the metadata such as automatically learned LDA topics of documents, inferred topic classifications based on a model trained to predict topics from a predefined taxonomy, translated titles for non-english documents, etc.

## Document preprocessing and cleaning

Most of the raw data that we are using are in the form of PDF and text documents. We develop a suite of preprocessing and cleaning modules to handle the transformations required to generate a high quality input to our models.

An overview of the pipeline is as follows:
- Convert pdf to text
- Parse the text document and perform sentence tokenization.
- Lemmatize the tokens and remove stop words.
- Drop all non-alphabetical tokens.
- Apply spell check and try to recover misspelled words.
- Normalize tokens by converting to lowercase.

### Phrase detection

Part of the preprocessing is also the inference of phrases in the documents. Phrases are logical grouping of tokens that represent an intrinsic meaning.

We are primarily leveraging the [Gensim](https://radimrehurek.com/gensim/) NLP toolkit and Spacy to develop the phrase detection algorithms.

### Acronym detection


## and NLP modeling


### Latent Dirichlet Allocation (LDA) topic model

### Embedding models (word2vec)


## Application development

## Setting up the environment

```
$ python -m ipykernel install --user --name=wb_nlp
```

## Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.

> ##### PyScaffold includes a pre-commit config
> ---
> A `.pre-commit-config.yaml` file was generated inside your project but in order to make sure the hooks will run, please don't forget to install the `pre-commit` package:

    $ cd wb_nlp
    $ # it is a good idea to create and activate a virtualenv here
    $ pip install pre-commit
    $ pre-commit install
    $ # another good idea is update the hooks to the latest version
    $ # pre-commit autoupdate
> ---
