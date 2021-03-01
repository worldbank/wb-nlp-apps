<template>
  <div>
    <h1>{{ page_title }}</h1>
    <br />

    <b-container fluid>
      <b-row>
        <b-col cols="9" class="border-right">
          <FileUpload
            :url="'/api/empty'"
            accept=".txt,.pdf"
            :post_file="false"
            :progress="progress"
            @change="onFileChange"
          ></FileUpload>

          <br />
          <br />
          <div v-if="documents.length" style="word-wrap: break-word">
            <vue-json-pretty :data="documents" :highlightMouseoverNode="true">
            </vue-json-pretty>
          </div>
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
import $ from "jquery";
import FileUpload from "@avsolatorio/v-file-upload";

import VueJsonPretty from "vue-json-pretty";
import "vue-json-pretty/lib/styles.css";

export default {
  name: "Similarity",
  components: {
    FileUpload,
    VueJsonPretty,
  },
  props: {
    page_title: String,
  },
  data: function () {
    return {
      api_url: "http://10.0.0.3:8880/api/related_words",
      related_words: [],
      raw_text: "",
      loading: true,

      // Model params
      corpus_id: "WB",
      word2vec_model_id: "ALL_50",
      lda_model_id: "ALL_50",
      // Uploaded file data
      progress: 0,
      is_searching: false,
      documents: [],
    };
  },
  mounted() {
    this.getRelatedWords();
  },
  computed: {
    related_docs_url: function () {
      var options = {
        corpus_id: this.corpus_id,
        model_id: this.word2vec_model_id,
        topn: 10,
        clean_doc: true,
      };

      return "/api/related_docs?" + $.param(options);
    },
  },
  methods: {
    isSuccess: function (e) {
      window.esuccess = e;
    },
    onFileChange: function (file) {
      this.progress = 0.1;
      window.anexo = file;
      file = file["file"];
      window.uploaded_file = file;
      window.fup = file;

      this.postUploadedFile(file);
    },
    isReady: function () {
      // This is useful when having different models to choose from.
      return true;
    },
    onProgress(e) {
      this.progress = parseInt((e.loaded * 100) / e.total);
      console.log(this.progress);
    },
    postUploadedFile: function (file) {
      var data = new FormData();
      data.append("file", file);
      window.fd = data;
      console.log(data);

      this.errors = [];
      this.uploaded_doc_topics = null;
      this.is_searching = true;

      var options = {
        corpus_id: this.corpus_id,
        model_id: this.word2vec_model_id,
        topn: 10,
        clean_doc: true,
      };

      var config = {
        onUploadProgress: this.onProgress,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };

      this.$http
        .post("/api/related_docs?" + $.param(options), data, config)
        .then((response) => {
          let data = response.data;
          if ("docs" in data) {
            this.documents = data.docs;
          }
        })
        .catch((error) => {
          console.log(error);
          this.errors.push(error);
          this.errored = true;
          this.is_searching = false;
          this.progress = 0;
        })
        .finally(() => {
          this.is_searching = false;
          this.progress = 0;
        });

      if (this.lda_model_id != "") {
        options = {
          corpus_id: this.corpus_id,
          model_id: this.lda_model_id,
          topn_topics: 10,
          total_topic_score: 0.8,
          clean_doc: true,
        };

        this.progress = 0.1;
        this.$http
          .post("/api/lda_doc_topics?" + $.param(options), data, config)
          .then((response) => {
            let data = response.data;
            if ("topics" in data) {
              this.uploaded_doc_topics = data.topics;
            }
          })
          .catch((error) => {
            console.log(error);
            this.errors.push(error);
            this.errored = true;
            this.is_searching = false;
            this.progress = 0;
          })
          .finally(() => {
            this.is_searching = false;
            this.progress = 0;
          });
      }
    },
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
