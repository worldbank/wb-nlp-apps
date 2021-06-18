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
    corpus_details: [{ "name": "ASIAN DEVELOPMENT BANK", "corpus_id": "ADB", "url": "https://www.adb.org/publications", "selection": "All types of documents except for the Official Records are of interest. This includes: Books; Reports; Papers and briefs; Serials; Conference Proceedings; Guides; Policies, Strategies, and Plans; Brochures and Flyers; Country Planning Documents; Country Sector and Thematic Assessments; Economic and Political Updates; Project Documents; Evaluation Documents." }, { "name": "AFRICAN DEVELOPMENT BANK", "corpus_id": "AFDB", "url": "https://www.afdb.org/en/documents/", "selection": "Documents of the following type are of interest: Environmental and Social Assessments; Evaluation Reports; Knowledge; Policy Documents; Strategy Documents; Projects Operations; Publications" }, { "name": "UNITED NATIONS ECONOMIC COMMISSION FOR LATIN AMERICA AND THE CARIBBEAN", "corpus_id": "ECLAC", "url": "https://www.cepal.org/en/publications/list/language/en", "selection": "All types of Documents are of interest, including: Regular Publications, Reviews, and Bulletins; Project Documents, Studies, and Research Papers; ECLAC Series; Books and Monographs; Flagships; Conferences and Meetings Documents; Position Papers of the Sessions of the Commission" }, { "name": "EDUCATION POLICY AND DATA CENTER", "corpus_id": "EPDC", "url": "https://www.epdc.org/taxonomy/term/156.html", "selection": "Documents of the following type are of interest: Research Papers" }, { "name": "UNITED NATIONS ECONOMIC AND SOCIAL COMMISSION FOR ASIA AND THE PACIFIC", "corpus_id": "ESCAP", "url": "https://www.unescap.org/publications", "selection": "All types of documents are of interest, including: Journal; Flagship; Working Paper; Book; Report; Review report" }, { "name": "FISHERIES, AQUACULTURE AND MARINE ECOSYSTEMS", "corpus_id": "FAME", "url": "https://fame.spc.int/en/publications/digital-library", "selection": "Documents of the following type are of interest: Book; Brochure/leaflet; Bulletin/newsletter (full issue); Conference/Journal Paper; Conference proceedings; Manual; Policy Brief; Report; Thesis" }, { "name": "FOOD AND AGRICULTURE ORGANIZATION", "corpus_id": "FAO", "url": "http://www.fao.org/publications/flagships/en/", "selection": "All flagship reports are of interest including: SOFA, SOFIA, SOFO, SOFI, SOFA, and SOCO." }, { "name": "INTERAMERICAN DEVELOPMENT BANK", "corpus_id": "IDB", "url": "https://publications.iadb.org/en/publications?", "selection": "Documents of the following type are of interest: Technical Notes; Discussion Papers; Working Papers; Catalogs and Brochures; Magazines, Journals, & Newsletters; Monographs; Books; Annual Reports; Policy Briefs; Learning Materials; Co-publications." }, { "name": "INTERNATIONAL INSTITUTE FOR EDUCATIONAL PLANNING", "corpus_id": "IIEP", "url": "http://www.iiep.unesco.org/en/publications", "selection": "Documents that fall under the following themes are of interest: Economics of Education; Educational Planning; Equality of Education for Targeted Groups; Levels, Content, and Modalities in Education; Management and Administration of Education Systems; Skills, Employment, and Social Development." }, { "name": "INTERNATIONAL LABOR ORGANIZATION", "corpus_id": "ILO", "url": "https://www.ilo.org/Search5/search.do?sitelang=en&locale=en_EN&consumercode=ILOHQ_STELLENT_PUBLIC&searchWhat=Search+ilo.org&searchLanguage=en", "selection": "All major publications in the English language are included." }, { "name": "OECD", "corpus_id": "OECD", "url": "https://www.oecd-ilibrary.org/papers#search-paper", "selection": "Documents of interest include: Working Papers and Periodicals" }, { "name": "UNITED NATIONS ECONOMIC COMMISSION FOR AFRICA", "corpus_id": "UNECA", "url": "https://www.uneca.org/publication-list", "selection": "All documents of the following type are of interest: Policy Reports; Policy Briefs; Flagship Reports; Other Reports" }, { "name": "UNITED NATIONS ECONOMIC COMMISSION FOR EUROPE", "corpus_id": "UNECE", "url": "https://www.unece.org/publications/oes/welcome.html", "selection": "All documents of \u201ctype\u201d Publications returned by the POST request to http://www.unece.org/index.php are included." }, { "name": "UNITED NATIONS ECONOMIC COMMISSION FOR WESTERN ASIA", "corpus_id": "UNESCWA", "url": "https://www.unescwa.org/publications/publications-list", "selection": "Documents of the following types are of interest: Reports and Studies; Data and Statistics; Training and Guidelines; Information Material; Working Papers; Brief Papers" }, { "name": "UNITED NATIONS HIGH COMMISSION FOR REFUGEES", "corpus_id": "UNHCR", "url": "https://www.unhcr.org/search", "selection": "All Documents that fall under the following categories are of interest: Reports; Publications; Statistics; Asylum Trends." }, { "name": "UNITED NATIONS INDUSTRIAL DEVELOPMENT ORGANIZATION", "corpus_id": "UNIDO", "url": "https://www.unido.org/resources/publications/publications-type", "selection": "All documents that fall under the following category are of interest: Working Papers." }, { "name": "UNITED NATIONS OFFICE OF DRUGS AND CRIME", "corpus_id": "UNODC", "url": "https://www.unodc.org/unodc/en/publications.html?ref=menutop", "selection": "All documents of the following types are of interest: World Drug Report; Crime and Drug Survey; Bulletin on Narcotics; Magazines; Annual Report; All Publications (by date)." }, { "name": "UNITED NATIONS POPULATION DIVISION", "corpus_id": "UNPD", "url": "http://www.un.org/en/development/desa/population/publications/index.shtml", "selection": "Documents of the following type are of interest: Publications; Manuals; Expert Paper Series; Technical Paper Series;" }, { "name": "WORLD BANK", "corpus_id": "WB", "url": "https://search.worldbank.org/api/v2/wds", "selection": "All types of documents ranging from Publications and Research, Project Documents, etc." }, { "name": "WORLD FOOD PROGRAM", "corpus_id": "WFP", "url": "https://www.wfp.org/publications?text=", "selection": "Documents of the following type are of interest: Brochures and Factsheets; Strategies and Policies; Annual reports; Country reports; Reports; Project reports; Analyses assessments and case studies; Books and papers; Evaluations; Impact Evaluations; Humanitarian Emergency Response Evaluations; Country Portfolio and Country Strategic Plan Evaluations; Operation and Activity Evaluations; Policy Evaluations; Strategic Evaluations; Syntheses Evaluations; Thematic and Transfer Modality Evaluations; Bulletins and Newsletter." }, { "name": "WORLD HEALTH ORGANIZATION", "corpus_id": "WHO", "url": "http://www.who.int/publications/en/", "selection": "The following document type is of interest: Bulletin of the World Health Organization (full list of all volumes available at: https://www.ncbi.nlm.nih.gov/pmc/journals/522/)" }],
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
