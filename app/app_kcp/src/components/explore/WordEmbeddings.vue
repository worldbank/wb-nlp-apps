<template>
  <div>
    <h1>{{ page_title }}</h1>
    <br />

    <b-container fluid>
      <b-row>
        <b-col md="9" class="border-right">
          <!-- Word2vec is a simple embedding model. -->
          <EmbeddingViz @selected="getRelatedWords"></EmbeddingViz>
        </b-col>
        <b-col md="3">
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

          <div v-show="loading">
            <b-skeleton-table
              v-show="loading"
              animation="wave"
              :rows="10"
              :columns="1"
              :table-props="{ bordered: true, striped: true }"
            ></b-skeleton-table>
          </div>

          <h4 v-show="related_words.length > 0">Similar words</h4>

          <b-list-group v-show="!loading" flush>
            <b-list-group-item
              v-for="related_word in related_words"
              :key="related_word.word"
            >
              {{ related_word.word }}
            </b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import EmbeddingViz from "./EmbeddingViz.vue";

export default {
  name: "WordEmbeddings",
  components: {
    EmbeddingViz,
  },
  props: {
    page_title: String,
  },
  data: function () {
    return {
      nlp_api_url: "/nlp/models/word2vec/get_similar_words",
      related_words: [],
      raw_text: "",
      loading: true,
    };
  },
  mounted() {
    this.getRelatedWords();
  },
  methods: {
    getRelatedWords: function (text = null) {
      if (typeof text !== "string") {
        text = this.raw_text;
      } else {
        this.raw_text = text;
      }
      this.loading = true;
      this.related_words = [];
      const body = {
        model_id: "777a9cf47411f6c4932e8941f177f90a",
        raw_text: text,
        topn_words: 10,
        metric: "cosine_similarity",
      };

      this.$http
        .post(this.nlp_api_url, body)
        .then((response) => {
          this.related_words = response.data;
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
          this.loading = false;
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
