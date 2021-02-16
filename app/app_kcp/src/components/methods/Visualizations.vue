<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      Explain purpose and main components of the “EXPLORE” section of the site.
      <br />
      <br />
      <ul>
        <li>
          Corpus describes the collection of documents (sources, scope,
          coverage, updates)
        </li>
        <li>
          Topic composition based on LDA model; describes the distribution of
          topics in the corpus or sub-corpus for different LDA models
        </li>
        <li>
          Topic profiles; select one topic, and see how it has evolved over
          time, by region, source, type, etc.
        </li>
        <li>Classification model: taxonomy tagging</li>
        <li>Word embeddings: semantic closeness using word2vec</li>
        <li>
          Similarity: select or load a document, find closest based on different
          measures of similarity
        </li>
      </ul>

      All code (except scrapers) in GitHub. See Methods and Tools.
    </div>
  </div>
</template>

<script>
export default {
  name: "Visualizations",
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
a {
  color: #42b983;
}
</style>
