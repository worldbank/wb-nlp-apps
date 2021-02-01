'''
This module contains the type definitions for the configuration parameters
of the model inference.

This typed data structure will be used in the implementation of the API using
FastAPI.
'''

import enum
import json
from typing import List, Any
from pydantic import BaseModel, Field, validator, AnyUrl
from wb_nlp.utils.scripts import generate_model_hash
from fastapi import File, UploadFile


class ModelTypes(enum.Enum):
    '''Types of models available.
    '''
    lda = "lda"  # Gensim LDA implementation
    mallet = "mallet"  # Mallet LDA implementation
    word2vec = "word2vec"  # Gensim Word2vec implementation


class TextInputParams(BaseModel):
    model_id: str = Field(
        ..., description="Identification of the desired model configuration to use for the operation. The cleaning pipeline associated with this model will also be applied.")
    model_type: ModelTypes = Field(
        ..., description="Model type.")


class Word2VecGetVectorParams(TextInputParams):
    raw_text: str = Field(
        ..., description="Input text to transform.")
    model_type: ModelTypes = ModelTypes.word2vec


class Word2VecTransformParams(TextInputParams):
    raw_text: str = Field(
        ..., description="Input text to transform.")

    # file: UploadFile = File(None, description='File to upload.')

    topn_words: int = Field(
        10, ge=1, description='Number of similar words to return.')
    topn_docs: int = Field(
        10, ge=1, description='Number of similar docs to return.')

    show_duplicates: bool = Field(
        False, description='Flag that indicates whether to return highly similar or possibly duplicate documents.'
    )
    duplicate_threshold: float = Field(
        0.98, ge=0, description='Threshold to use to indicate whether a document is highly similar or possibly a duplicate of the input.'
    )
    return_related_words: bool = Field(
        True, description='Flag indicating an option to return similar or topic words to the document.')
    translate: bool = Field(
        True, description='Flag indicating an option to translate the input data.'
    )


class LDATransformParams(TextInputParams):
    # file: UploadFile = File(None, description='File to upload.')
    topn_words: int = Field(
        10, ge=1, description='Number of similar words to return.')
    topn_docs: int = Field(
        10, ge=1, description='Number of similar docs to return.')
    show_duplicates: bool = Field(
        False, description='Flag that indicates whether to return highly similar or possibly duplicate documents.'
    )
    duplicate_threshold: float = Field(
        0.98, ge=0, description='Threshold to use to indicate whether a document is highly similar or possibly a duplicate of the input.'
    )
    topic_id: int = Field(
        0, description="Topic id of interest."
    )
    topn_topics: int = Field(
        10, ge=1, description='Return at most `topn_topics` topics.')
    topn_topic_words: int = Field(
        10, ge=1, description='Return at most `topn_topic_words` words in topic.')

    total_topic_score: float = Field(
        0.8, ge=0, description="Return at most `total_topic_score` cumulative proportion topics."
    )
    total_word_score: float = Field(
        0.8, description="Return at most `total_word_score` cumulative proportion words in topic."
    )

    translate: bool = Field(
        True, description='Flag indicating an option to translate the input data.'
    )


class ModelMeta(BaseModel):
    model_name: ModelTypes = Field(
        ...,
        description="Short name of the model."
    )
    library: str = Field(
        ...,
        description="Name of the library where the model comes from. Example: Gensim."
    )
    model_implementation: str = Field(
        ...,
        description="Name of the specific model implementation selected. Example: `LDA Multicore` if the multicore implementation is used."
    )
    library_version: str = Field(
        ...,
        description="The exact version of the library that was used. Example: 3.8.3"
    )
    docs: AnyUrl = Field(
        ...,
        description="Link to the documentation of the model. Example: https://radimrehurek.com/gensim/models/ldamulticore.html"
    )
    references: List[str] = Field(
        None,
        description="List of other references. Could be links to resources or brief notes on the model. Example: https: // markroxor.github.io/gensim/static/notebooks/lda_training_tips.html"
    )


class DictionaryConfig(BaseModel):
    dictionary_config_id: str = Field(
        '', description="Configuration id derived from the combination of the parameters.")

    no_below: int = Field(
        10,
        description="""Used in `filter_extremes`. Keep tokens which are contained in at least no_below documents."""
    )

    no_above: float = Field(
        0.98,
        description="""Used in `filter_extremes`. Keep tokens which are contained in no more than no_above documents (fraction of total corpus size, not an absolute number)."""
    )
    keep_n: int = Field(
        200000,
        description="""Used in `filter_extremes`. Keep only the first keep_n most frequent tokens."""
    )
    keep_tokens: list = Field(
        None,
        description="""Used in `filter_extremes`. Iterable of tokens that must stay in dictionary after filtering."""
    )

    def __init__(self, **data: Any) -> None:
        temp_data = dict(data)

        if 'dictionary_config_id' in temp_data:
            # Remove `cleaner_config_id` if exists since it will be
            # computed as unique id from other fields.
            temp_data.pop('dictionary_config_id')

        super().__init__(**temp_data)

        self.dictionary_config_id = generate_model_hash(
            json.loads(self.json()))


class LDAConfig(BaseModel):
    '''Definition of parameters for the Gensim LDA model.

    Parameter descriptions are based from the official documentation https://radimrehurek.com/gensim/models/ldamulticore.html.
    '''

    lda_config_id: str = Field(
        '', description="Configuration id derived from the combination of the parameters.")

    num_topics: int = Field(
        100,
        description="""The number of requested latent topics to be extracted from the training corpus."""
    )

    id2word: dict = Field(
        None,
        description="""Mapping from word IDs to words. It is used to determine the vocabulary size, as well as for debugging and topic printing."""
    )

    workers: int = Field(
        4,
        description="""Number of workers processes to be used for parallelization. If None all available cores (as estimated by workers=cpu_count()-1 will be used. Note however that for hyper-threaded CPUs, this estimation returns a too high number – set workers directly to the number of your real cores (not hyperthreads) minus one, for optimal performance.

Note: Use 1/2 of virtual cores - 1: (cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l) * (cat /proc/cpuinfo | grep "cpu cores" | uniq)"""
    )

    chunksize: int = Field(
        250,
        description="""Number of documents to be used in each training chunk. Note: Update size is chunksize * number of workers -> Update every 10,000 documents processed."""
    )

    passes: int = Field(
        5,
        description="""Number of passes through the corpus during training."""
    )

    batch: bool = Field(
        False,
        description=""
    )

    alpha: str = Field(
        "symmetric",
        description="""Can be set to an 1D array of length equal to the number of expected topics that expresses our a-priori belief for the each topics’ probability. Alternatively default prior selecting strategies can be employed by supplying a string:

’asymmetric’: Uses a fixed normalized asymmetric prior of 1.0 / topicno.

Note: The auto value is not supported by LdaMulticore."""
    )

    eta: str = Field(
        None,
        description="""A-priori belief on word probability, this can be:

scalar for a symmetric prior over topic/word probability,

vector of length num_words to denote an asymmetric user defined probability for each word,

matrix of shape (num_topics, num_words) to assign a probability for each word-topic combination,

the string ‘auto’ to learn the asymmetric prior from the data."""
    )

    decay: float = Field(
        0.5,
        description="""A number between (0.5, 1] to weight what percentage of the previous lambda value is forgotten when each new document is examined."""
    )

    offset: float = Field(
        1.0,
        description="""Hyper-parameter that controls how much we will slow down the first steps the first few iterations."""
    )
    eval_every: int = Field(
        5,
        description="""Log perplexity is estimated every that many updates. Setting this to one slows down training by ~2x."""
    )

    iterations: int = Field(
        1000,
        description="""Maximum number of iterations through the corpus when inferring the topic distribution of a corpus."""
    )

    gamma_threshold: float = Field(
        0.001,
        description="""Minimum change in the value of the gamma parameters to continue iterating."""
    )

    random_state: int = Field(
        1029,
        description="""Either a randomState object or a seed to generate one. Useful for reproducibility."""
    )

    minimum_probability: float = Field(
        0.01,
        description="""Topics with a probability lower than this threshold will be filtered out."""
    )

    minimum_phi_value: float = Field(
        0.01,
        description="""if per_word_topics is True, this represents a lower bound on the term probabilities."""
    )

    per_word_topics: bool = Field(
        False,
        description="""If True, the model also computes a list of topics, sorted in descending order of most likely topics for each word, along with their phi values multiplied by the feature length (i.e. word count)."""
    )

    def __init__(self, **data: Any) -> None:
        temp_data = dict(data)

        if 'lda_config_id' in temp_data:
            # Remove `cleaner_config_id` if exists since it will be
            # computed as unique id from other fields.
            temp_data.pop('lda_config_id')

        super().__init__(**temp_data)

        self.lda_config_id = generate_model_hash(json.loads(self.json()))


class MalletConfig(BaseModel):
    '''Definition of parameters for the Gensim LDA model.

    Parameter descriptions are based from the official documentation https://radimrehurek.com/gensim/models/ldamulticore.html.
    '''

    mallet_config_id: str = Field(
        '', description="Configuration id derived from the combination of the parameters.")

    mallet_path: str = Field(
        "models/mallet/mallet-2.0.8/bin/mallet",
        description="""Path to the mallet binary, e.g. /home/username/mallet-2.0.7/bin/mallet."""
    )

    num_topics: int = Field(
        100,
        description="""Number of topics."""
    )

    alpha: int = Field(
        5,
        description="""Alpha parameter of LDA."""
    )

    id2word: dict = Field(
        None,
        description="""Mapping between tokens ids and words from corpus, if not specified - will be inferred from corpus."""
    )

    workers: int = Field(
        7,
        description="""Number of threads that will be used for training."""
    )

    prefix: str = Field(
        "models/mallet/tmp/tmp_",
        description="""Prefix for produced temporary files."""
    )

    optimize_interval: int = Field(
        10,
        description="""Optimize hyperparameters every optimize_interval iterations (sometimes leads to Java exception 0 to switch off hyperparameter optimization)."""
    )

    iterations: int = Field(
        1000,
        description="""Number of training iterations."""
    )

    topic_threshold: float = Field(
        0.0,
        description="""Threshold of the probability above which we consider a topic."""
    )

    random_seed: int = Field(
        1029,
        description="""Random seed to ensure consistent results, if 0 - use system clock."""
    )

    def __init__(self, **data: Any) -> None:
        temp_data = dict(data)

        if 'mallet_config_id' in temp_data:
            # Remove `cleaner_config_id` if exists since it will be
            # computed as unique id from other fields.
            temp_data.pop('mallet_config_id')

        super().__init__(**temp_data)

        self.mallet_config_id = generate_model_hash(json.loads(self.json()))


class DFRConfig(BaseModel):
    tw_file: str = Field(
        "tw.json",
        description=""
    )
    dt_file: str = Field(
        "dt.json",
        description=""
    )
    info_file: str = Field(
        "info.json",
        description=""
    )


class LDAModelConfig(BaseModel):
    model_config_id: str = Field(
        '', description="Configuration id derived from the combination of the parameters.")

    min_tokens: int = Field(
        50,
        description="Minimum number of tokens that a cleaned document must have in order to be included in the training of the model."
    )
    lda_config: LDAConfig
    dictionary_config: DictionaryConfig
    meta: ModelMeta
    dfr_config: DFRConfig

    def __init__(self, **data: Any) -> None:
        temp_data = dict(data)

        if 'model_config_id' in temp_data:
            # Remove `cleaner_config_id` if exists since it will be
            # computed as unique id from other fields.
            temp_data.pop('model_config_id')

        super().__init__(**temp_data)

        self.model_config_id = generate_model_hash(json.loads(self.json()))


class MalletModelConfig(BaseModel):
    model_config_id: str = Field(
        '', description="Configuration id derived from the combination of the parameters.")

    min_tokens: int = Field(
        50,
        description="Minimum number of tokens that a cleaned document must have in order to be included in the training of the model."
    )
    mallet_config: MalletConfig
    dictionary_config: DictionaryConfig
    meta: ModelMeta
    dfr_config: DFRConfig

    def __init__(self, **data: Any) -> None:
        temp_data = dict(data)

        if 'model_config_id' in temp_data:
            # Remove `cleaner_config_id` if exists since it will be
            # computed as unique id from other fields.
            temp_data.pop('model_config_id')

        super().__init__(**temp_data)

        self.model_config_id = generate_model_hash(json.loads(self.json()))


class ModelRunInfo(BaseModel):
    model_run_info_id: str = Field(
        "", description="Unique identifier derived from the combination of the experiment components.")

    model_name: ModelTypes = Field(
        ...,
        description="Name of model."
    )
    model_config_id: str = Field(
        ...,
        description="Configuration of the model used in the experiment."
    )
    processed_corpus_id: str = Field(
        ...,
        description="Some unique identifier of the input data. Example: dictionary_id + hash of the cleaned corpus."
    )

    def __init__(self, **data: Any) -> None:
        temp_data = dict(data)

        if 'model_run_info_id' in temp_data:
            # Remove `cleaner_config_id` if exists since it will be
            # computed as unique id from other fields.
            temp_data.pop('model_run_info_id')

        super().__init__(**temp_data)

        self.model_run_info_id = generate_model_hash(json.loads(self.json()))


# model_config:
#   meta:
#     model_id: null  # To be filled up in the model training
#     library: Gensim
#     model_implementation: LDA Multicore
#     library_version: 3.8.3
#     docs: https://radimrehurek.com/gensim/models/ldamulticore.html#module-gensim.models.ldamulticore
#     references:
#       - https://markroxor.github.io/gensim/static/notebooks/lda_training_tips.html
#   params:
#     min_tokens: 50
#     dictionary:
#       no_below: 10
#       no_above: 0.98
#       keep_n: 200000
#       keep_tokens: null
#     lda:
#       num_topics:
#         # - 50
#         - 75
#         # - 100
#         # - 150
#       id2word: null
#       workers: -41  # -4  # Use 1/2 of virtual cores - 1 (cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l) * (cat /proc/cpuinfo | grep "cpu cores" | uniq)
#       chunksize: 250  # Update size is chunksize * number of workers -> Update every 10,000 documents processed.
#       passes:
#         - 5
#         # - 10
#         # - 10
#         # - 20
#       batch: False
#       alpha:
#         - symmetric
#         # - auto  # The auto value is not supported by LdaMulticore
#       eta:
#         - auto
#         - null
#       decay: 0.5
#       offset: 1.0
#       eval_every: 5
#       iterations:
#         - 1000
#         # - 2000
#       gamma_threshold: 0.001
#       random_state: 1029
#       minimum_probability: 0.01
#       minimum_phi_value: 0.01
#       per_word_topics: False
#   paths:
#     base_dir: /data/wb536061/wb_nlp/data/raw/CORPUS
#     source_dir_name: TXT_LDA
#     corpus_path: /data/wb536061/wb_nlp/data/raw/CORPUS/bow_corpus-TXT_LDA.mm
#     dictionary_path: /data/wb536061/wb_nlp/data/raw/CORPUS/dictionary-TXT_LDA.gensim.dict
#     model_dir: /data/wb536061/wb_nlp/models/lda
#     dfr_files:
#       tw: tw.json
#       dt: dt.json
#       info: info.json
