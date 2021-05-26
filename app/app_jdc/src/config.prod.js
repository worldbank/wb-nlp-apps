export default {
    jdc_models: {
        embedding_model: {
            model_name: "word2vec",
            model_id: "2617e5cf327e60cc8955189110e7f21d", // "0d63e5ae71e4f78fc427ddbec2fefc73",
        },
        topic_model: {
            model_name: "mallet",
            model_id: "6fd8b418cbe4af7a1b3d24debfafa1ee"
        },
        topic_model_api_url: "/nlp/models/mallet",
        default_topic_id: 39 // Topic on refugee
    },
    default_model: {
        embedding_model: {
            model_name: "word2vec",
            model_id: "2617e5cf327e60cc8955189110e7f21d", // "0d63e5ae71e4f78fc427ddbec2fefc73",
        },
        topic_model: {
            model_name: "mallet", // "lda",
            model_id: "6fd8b418cbe4af7a1b3d24debfafa1ee", // "6694f3a38bc16dee91be5ccf4a64b6d8"
        },
        word2vec: {
            model_id: "2617e5cf327e60cc8955189110e7f21d",  // "854ae5f9cdda093265212c435d1ddfd4",  // "777a9cf47411f6c4932e8941f177f90a",
        },
        lda: {
            model_id: "6fd8b418cbe4af7a1b3d24debfafa1ee",  // "749573cedb4b06aedcba2ec89bc46b46",  // "6694f3a38bc16dee91be5ccf4a64b6d8"
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
        },
        mallet: {
            file: "/nlp/search/mallet/file",
            url: "/nlp/search/mallet/url",
        }
    },
    analyze_document_url: {
        lda: {
            analyze_file: "/nlp/models/lda/analyze_file",
            analyze_url: "/nlp/models/lda/analyze_url"
        },
        mallet: {
            analyze_file: "/nlp/models/mallet/analyze_file",
            analyze_url: "/nlp/models/mallet/analyze_url"
        }

    },
    corpus_url: "/nlp/corpus",
    extra_url: {
        wdi: "/nlp/extra/indicators/wdi",
        sdg: "/nlp/extra/indicators/sdg",
        microdata: "/nlp/extra/indicators/microdata",
        all: "/nlp/extra/indicators/all"
    },
    pagination: {
        page_sizes: [10, 25, 50, 100],
        page_window: 2,
        size: 10,
    },
    sample_metadata: {
        "hex_id": "7b1575229ffccf9",
        "url_txt": "http://documents.worldbank.org/curated/en/369571538245763939/text/569840NEWS0Ban10121051970BOX354963B.txt",
        "country": [
            "World"
        ],
        "url_pdf": "http://documents.worldbank.org/curated/en/369571538245763939/pdf/569840NEWS0Ban10121051970BOX354963B.pdf",
        "year": 1997,
        "der_language_detected": "en",
        "corpus": "WB",
        "doc_type": [
            "Newsletter"
        ],
        "title": "Bank's World",
        "adm_region": [
            "The World Region"
        ],
        "date_published": "1997-12-05T00:00:00",
        "int_id": 554320239546846460,
        "path_original": "data/corpus/WB/wb_12853118.txt",
        "tokens": 17160,
        "id": "wb_12853118",
        "views": 0,
        "last_update_date": "2021-02-16T06:14:46.624679",
        "topics_src": [
            "Energy",
            "Environment",
            "Health; Nutrition and Population",
            "Science and Technology Development",
            "Social Protections and Labor",
            "Water Resources"
        ],
        "der_clean_token_count": 6744,
        "digital_identifier": "090224b0828b321d",
        "der_language_score": 0.999995416533436,
        "filename_original": "569840NEWS0Ban10121051970BOX354963B.txt",
        "wb_subtopic_src": [
            "Climate Change and Environment",
            "Climate Change and Health",
            "Energy Demand",
            "Energy and Environment",
            "Energy and Mining",
            "Global Environment",
            "Hydrology",
            "Labor Markets",
            "Science of Climate Change"
        ],
        "collection": "Bank's World (Bank notes)",
        "language_src": "English",
        "major_doc_type": [
            "Publications and Research"
        ],
        "der_countries": {
            "YEM": 2,
            "MEX": 1,
            "AFG": 1,
            "SAU": 1,
            "CHN": 10,
            "JPN": 3,
            "THA": 1,
            "IDN": 2,
            "VNM": 1,
            "SDN": 3,
            "BGD": 1,
            "SWE": 1,
            "ESP": 1,
            "PSE": 1,
            "MYS": 1,
            "YUG": 3,
            "POL": 1,
            "SUN": 1,
            "SYR": 1,
            "KOR": 1,
            "BRA": 1,
            "RUS": 1,
            "DEU": 3,
            "KEN": 1,
            "EGY": 1,
            "PAN": 3,
            "IND": 2
        }
    }
}