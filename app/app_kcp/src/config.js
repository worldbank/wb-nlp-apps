export default {
    default_model: {
        word2vec: {
            model_id: "777a9cf47411f6c4932e8941f177f90a",
        },
        lda: {
            model_id: "6694f3a38bc16dee91be5ccf4a64b6d8"
        }
    },
    nlp_api_url: {
        word2vec: "/nlp/models/word2vec",
        lda: "/nlp/models/lda",
        mallet: "/nlp/models/mallet",
    },
    search_url: {
        keyword: "/nlp/search/keyword",
        semantic: "/nlp/search/word2vec/semantic",
        file: "/nlp/search/word2vec/file",
        word2vec: {
            file: "/nlp/search/word2vec/file",
            url: "/nlp/search/word2vec/url",
        },
        lda: {
            file: "/nlp/search/lda/file",
            url: "/nlp/search/lda/url",
        }
    },
    corpus_url: "/nlp/corpus",
    extra_url: {
        wdi: "/nlp/extra/wdi"
    },
    pagination: {
        page_sizes: [10, 25, 50, 100],
        page_window: 2,
        size: 10,
    }
}