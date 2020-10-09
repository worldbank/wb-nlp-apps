<template>
  <div class="hello">
    <h1>{{ page_title }}</h1>
    <br />

    <b-container fluid>
      <b-row>
        <b-col cols="9" class="border-right">
          Word2vec is a simple embedding model.
        </b-col>
        <b-col cols="3">
          <h2>Try the API!</h2>
          <b-form-input
            width="100%"
            v-model="raw_text"
            placeholder="Enter word(s)"
            v-on:keyup.enter="getRelatedWords"
          />
          <br />
          <h4 v-show="raw_text">Input text</h4>
          {{ raw_text }}
          <br />
          <br />
          <h4>Similar words</h4>

          <b-skeleton
            v-show="loading"
            animation="wave"
            width="85%"
          ></b-skeleton>
          <b-list-group v-show="!loading" flush>
            <b-list-group-item
              v-for="related_word in related_words"
              :key="related_word.word"
            >
              {{ related_word.word }}
            </b-list-group-item>
          </b-list-group></b-col
        >
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "Similarity",
  props: {
    page_title: String,
  },
  data: function () {
    // http://10.0.0.25:8880/api/related_words?raw_text=poverty&model_id=ALL_50
    return {
      api_url: "http://10.0.0.25:8880/api/related_words",
      related_words: [],
      raw_text: "",
      loading: true,
    };
  },
  mounted() {
    this.getRelatedWords();
  },
  methods: {
    getRelatedWords: function () {
      this.loading = true;
      this.$http
        .get(this.api_url + "?model_id=ALL_50&raw_text=" + this.raw_text)
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
