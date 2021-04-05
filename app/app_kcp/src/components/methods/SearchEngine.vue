<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <p>
        Keyword search is a common tool for users to find relevant information.
        While the focus of this project is to explore, develop, and apply NLP
        models to improve the discoverability of text data, we also recognize
        the immense power of a well tuned keyword search engine. This motivated
        us to integrate a full-text search engine on the platform.
      </p>
      <p>
        We are using
        <a href="https://www.elastic.co/" target="_blank">Elasticsearch</a> as
        our full-text search engine.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchEngine",
  props: {
    page_title: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* h3 {
  margin: 40px 0 0;
}
a {
  color: #42b983;
} */
</style>
