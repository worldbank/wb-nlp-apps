# World Bank Knowledge for Change NLP Project

This repository contains all the codes and jupyter notebooks used to experiment and implement various NLP solutions to develop components for a document and data discovery application.

## About the Knowledge for Change NLP Project

The project is broken down into the following components:

1. Web scraping and automation (`/src/wb_nlp/scraping`)
2. Metadata extraction (`/src/wb_nlp/extraction`)
3. Document preprocessing and cleaning (`/src/wb_nlp/cleaning`)
4. NLP modeling (`/src/wb_nlp/modeling`)
5. Application development (`/src/wb_nlp/app`)

## Web scraping

The objective of this project is to use NLP models to learn topics, embedding, and other representations that could be useful for improving discoverability of documents. A major requirement for this undertaking is the availability of data that can be used to train machine learning models. We aim to use web scraping and API access when possible to aggregate a large collection of documents. The document aggregation will focus on documents produced by international organizations and multilateral development banks to generate a specialized collection of economic and development centric corpus.

Technologies such as [Scrapy](https://scrapy.org/) and [NiFi](https://nifi.apache.org/), as well as vanilla implementations of API access are used to implement the web scraping part of the project.

## Metadata extraction


## Document preprocessing and cleaning


## NLP modeling


## Application development


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
