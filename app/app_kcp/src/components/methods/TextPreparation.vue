<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      This page discusses the details regarding the primary components of our
      text processing pipeline. The following sections include technical
      information about our selection of tools, techniques adopted and
      developed, as well as some insights on our learnings while iterating on
      the development of the pipeline.
      <hr />
      <h5>PDF processing</h5>
      <p>Conversion to text</p>
      <h5>Metadata normalization</h5>
      <p>This is the process of metadata normalization</p>
      <h5>Stop words</h5>
      <p>Stop words (include CSV file)</p>
      <h5>Phrase detection</h5>
      <p>Phrase detection</p>
      <h5>Spell checking and vocabulary</h5>
      <p>Spell check</p>
      <h5>Acronym extraction</h5>
      <p>Acronyms</p>
      <h5>Named Entity Extraction</h5>
      <p>NER</p>
      <h5>Extraction of country counts</h5>
      <p>Country counts (include CSV file)</p>
      <h5>Language detection</h5>
      <p>Tokenization</p>
      <p>
        Simple interactive application showing before and after text cleaning of
        input text.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "TextPreparation",
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
