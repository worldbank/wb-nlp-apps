<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <p>Conversion to text</p>
      <p>Stop words (include CSV file)</p>
      <p>Phrase detection</p>
      <p>Spell check</p>
      <p>Acronyms</p>
      <p>n-grams (phrases)</p>
      <p>NER</p>
      <p>Country counts (include CSV file)</p>
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
