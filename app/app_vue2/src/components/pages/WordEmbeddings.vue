<template>
  <div class="hello">
    <h1>{{ page_title }}</h1>
    <br />

    <ul>
      <li v-for="related_word in related_words" :key="related_word.word">
        {{ related_word.word }}
      </li>
    </ul>

    <b-container fluid>
      <!-- <vue-friendly-iframe
        src="https://agoldst.github.io/dfr-browser/demo/"
        @load="onLoad"
      ></vue-friendly-iframe> -->
      <iframe
        src="https://agoldst.github.io/dfr-browser/demo/"
        frameborder="0"
        height="800px"
        width="100%"
      ></iframe>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "WordEmbeddings",
  props: {
    page_title: String,
  },
  data: function () {
    // http://10.0.0.25:8880/api/related_words?raw_text=poverty&model_id=ALL_50
    return {
      related_words: [],
      loading: true,
    };
  },
  mounted() {
    this.getRelatedWords();
  },
  methods: {
    getRelatedWords: function () {
      this.$http
        .get(
          "http://10.0.0.25:8880/api/related_words?raw_text=poverty&model_id=ALL_50"
        )
        .then((response) => {
          this.related_words = response.data.words;
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
        })
        .finally(() => (this.loading = false));
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
