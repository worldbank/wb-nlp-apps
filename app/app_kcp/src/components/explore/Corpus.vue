<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <p class="mt-4">
        Our corpus is composed of documents made publicly accessible by various
        agencies (listed
        <router-link to="/explore/subcategories/sources/"> here</router-link>)
        involved in international development. These agencies were selected to
        cover a diversity of themes related to socio-economic development. We
        will keep enriching this corpus in the future.
      </p>
      <p>
        The corpus was built over several months by querying APIs when
        available, or by scraping websites. The web scraping policy of some
        organizations prevented us from collecting materials we consider as
        relevant for our word embedding models (including the World Health
        Organization and the International Labour Organization). We will seek to
        include documents from these sources in future versions of our models.
        The corpus will be maintained on a periodic basis (quarterly or
        bi-annually).
      </p>
      <p>
        Two versions of the corpus are used in the project. One is used to train
        our <router-link to="/methods/lda">LDA topic</router-link> and
        <router-link to="/methods/word-embeddings">word embedding</router-link>
        models. Another one is used in our
        <router-link to="/methods/word-embeddings">
          document catalog</router-link
        >. The corpus used for the catalog is a subset of documents from the
        training corpus (documents are filtered based on their origin and type),
        to which we add “new” documents (acquired after the models were trained)
        for which topics and word embeddings have been extracted by inference.
      </p>
      <p>
        Core metadata on each document (title, author, URL, type of document,
        abstract, etc. based on availability) are collected at the document
        acquisition stage. Information extraction procedures and NLP models are
        then applied to generate additional metadata (including number of
        tokens, country counts, topic composition, acronyms, extraction of named
        entities, and others). These approaches are described in the
        <router-link to="/methods">Methods & Tools</router-link> section. The
        <router-link to="/explore/subcategories/metadata/"
          >Metadata</router-link
        >
        section provides a description of the information collected on each
        document, or generated for each document.
      </p>

      <p>
        <b style="color: red">
          Our catalog provides links to documents; we do not directly distribute
          the documents.</b
        >
      </p>

      <h4>Scope</h4>
      <p>
        The corpus is built to cover all sectors of socio-economic development.
        It focuses on project documents and research/knowledge products. As our
        objective is also to make word embeddings relevant to statistical data
        discoverability, we also included a set of documents related to official
        statistics, statistical software, and the metadata of Sustainable
        Development Goals. Although no document is excluded based on its
        geographic coverage, the focus on development issues means that the
        majority of documents on low and middle-income countries. The
        <router-link to="/explore/subcategories/geographic-coverage/"
          >Geographic coverage</router-link
        >
        section provides information on the country and regional coverage of the
        corpus.
      </p>
      <h4>Volume</h4>
      <p>
        As of {{ date_now }}, our training corpus contains
        {{ corpus_size.toLocaleString() }} documents, representing a total of
        {{ total_tokens.toLocaleString() }} useful words (‘tokens’). Useful
        words are the words that are left in a document after it goes through
        our text cleaning pipeline, which excludes stop words, words not found
        in the English dictionary or Wikipedia (after spell checking and
        automatic correction is applied). Many documents in our corpus,
        especially older documents, are scanned documents converted to text
        using OCR. OCR errors generated a significant number of unknown words
        which could not be automatically corrected and created noise that had to
        be excluded. The distribution of documents and tokens by year and by
        source is presented
        <router-link to="/explore/subcategories/volume/">here</router-link>.
      </p>
      <h4>Languages</h4>
      <p>
        Our corpus is limited to documents written in English. Some of the
        scraped documents may be multi-lingual, and others may be in other
        languages. Automatic language detection was applied to retain English
        documents only. As our corpus is largely composed of documents from
        international agencies or regional agencies from the United Nations
        system, the selection of English documents is not considered as a major
        issue for most of the purposes we pursue.
      </p>
      <h4>Exclusions</h4>
      <p>
        We have excluded documents that were found to have too little relevant
        content. This includes documents that, after processing, contained less
        than 250 tokens. We also excluded documents like procurement plans,
        reports from administrative tribunals, budgets, and other administrative
        documents. This exclusion is based on some heuristics and cannot be
        guaranteed without errors of inclusion or exclusion.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Corpus",
  props: {
    page_title: String,
  },
  data: function () {
    return {
      date_now: new Date().toDateString(),
      corpus_size: 368563,
      org_count: 14,
      total_tokens: 1029000000,
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* h3 {
  margin: 40px 0 0;
} */
/* a {
  color: #42b983;
} */
</style>
