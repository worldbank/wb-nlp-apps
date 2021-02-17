<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      <p>
        One of our objectives is to share scripts, methods to help NLP students
        by replicating and adapting. The full corpus is too big, and we do not
        own documents. We provide a smaller corpus of documents for practice,
        selected from WB Publications and Research documents. Original text and
        clean text version, metadata.
      </p>

      <p>Content: 25,000 documents</p>
      <p>Metadata file: <a href="#">link here</a></p>
      <p>Already contains augmented metadata.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Metadata",
  props: {
    page_title: String,
  },
  data: function () {
    return {
      date_now: new Date().toDateString(),
      corpus_size: 200000,
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
