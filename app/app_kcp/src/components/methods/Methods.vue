<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <p>
        Our project benefited considerably from methods and tools developed by
        the open source community. We are equally committed to contribute to the
        public good, by making our processes as transparent and reproducible as
        possible.
      </p>
      <p>
        Apart from the web scrapers developed for
        <router-link to="/methods/text-acquisition"
          >acquiring documents</router-link
        >
        from various sources (which we do not share to avoid risks of abusive
        use that may impact the websites we scraped), all our scripts are
        available in our Github repository. These scripts cover the following
        components of the project:
      </p>
      <ul>
        <li>
          <router-link to="/methods/text-preparation"
            >Text processing/preparation</router-link
          >
          We obtained most of the documents that are part of our corpus in PDF
          format. These documents had to be converted to text format. For many
          documents, OCR had been implemented by the originating document
          repository (all World Bank documents are made available both in PDF
          and in TXT format). The OCR resulted in many errors. Beyond file
          format conversion, a pipeline of text processing had to be
          implemented. This pipeline included language detection, spell
          checking, acronyms extraction, stop-words exclusion, exclusion of
          non-English words, phrase detection, counting frequency of country
          names in documents, and more. This pipeline resulted in a “clean”
          version of each document in text format, which served as input to the
          NLP models. As the quality of the models depends heavily on the
          quality of this text preparation phase, we plan to further develop and
          improve this processing and cleaning pipeline. Future improvements
          will be published in our GitHub repository. This may include
          application of named entity recognition, approaches to deal with text
          hyphenation, and others.
        </li>
        <li>
          Implementation of
          <router-link to="/methods/lda">topic models</router-link>. Latent
          Dirichlet Allocation (LDA) models were implemented (using Gensim and
          Mallet).
        </li>
        <li>
          Implementation of
          <router-link to="/methods/word-embeddings"
            >word embedding models</router-link
          >
          Many of the documents in our corpus are such that sentence
          tokenization is often not doable. We therefore limited our embedding
          models to word2vec models which only require word tokenization.
        </li>
        <li>
          <router-link to="/methods/cataloguing">Cataloguing</router-link> we
          catalogued the documents metadata in a MongoDB database.
        </li>
        <li>
          <router-link to="/methods/search-engine">Search engine</router-link>
          our search engine is built on ElasticSearch (for the keyword search)
          and on Milvus for the semantic search.
        </li>
        <li>
          <router-link to="/methods/visualizations">Visualizations</router-link>
          We adapted the dfrBrowser application by A. Goldstone to display the
          output of our LDA topic model and used the eCharts library for other
          visualizations.
        </li>
      </ul>

      We also provide a set of
      <router-link to="/methods/training-materials"
        >training materials</router-link
      >
      that data scientists may find useful to learn and practice NLP approaches
      by replicating and adapting our scripts, using a manageable corpus.
    </div>
  </div>
</template>

<script>
export default {
  name: "Methods",
  props: {
    page_title: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
</style>
