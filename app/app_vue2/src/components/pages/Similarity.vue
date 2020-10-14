<template>
  <div>
    <h1>{{ page_title }}</h1>
    <br />

    <b-container fluid>
      <b-row>
        <b-col cols="9" class="border-right">
          Word2vec is a simple embedding model.
          <FileUpload
            :url="url"
            :thumb-url="thumbUrl"
            :headers="headers"
            accept=".txt, .pdf"
            @change="onFileChange"
          ></FileUpload>

          <div class="input-group mb-3">
            <div class="custom-file">
              <form
                class="form-file-upload"
                method="post"
                enctype="multipart/form-data"
                action="/api/related_docs"
              >
                <input
                  type="file"
                  ref="file"
                  name="file"
                  class="xcustom-file-input"
                  id="xinputGroupFile01"
                />
                <!--<label class="custom-file-label" for="inputGroupFile01">Choose file</label>-->
                <input
                  type="submit"
                  v-on:click="uploadFile"
                  :disabled="isReady() === false"
                />
              </form>
            </div>
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
import FileUpload from "v-file-upload";
import $ from "jquery";

export default {
  name: "Similarity",
  components: {
    FileUpload,
  },
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

      // Model params
      corpus_id: "WB",
      word2vec_model_id: "ALL_50",
      lda_model_id: "ALL_50",
      // Uploaded file data
      // fileUploaded: null,
      is_searching: false,
      documents: [],
    };
  },
  mounted() {
    this.getRelatedWords();
  },
  methods: {
    onFileChange: function (file) {
      // this.fileUploaded = file;
      window.fup = file;
      this.postUploadedFile(file);
    },
    isReady: function () {
      return true;
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
        // data: data,
      };

      this.$http
        .post(
          // "/api/related_docs?corpus_id=WB&model_id=ALL_50&topn=10&clean_doc=true",
          "/api/related_docs?" + $.param(options),
          data,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
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
        })
        .finally(() => {
          this.is_searching = false;
        });

      if (this.lda_model_id != "") {
        options = {
          corpus_id: this.corpus_id,
          model_id: this.lda_model_id,
          topn_topics: 10,
          total_topic_score: 0.8,
          clean_doc: true,
        };

        this.$http
          .post("/api/lda_doc_topics?" + $.param(options), data, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
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
          })
          .finally(() => {
            this.is_searching = false;
          });
      }
    },
    uploadFile: function (e) {
      if (!this.isReady()) {
        return;
      }

      window.x = this.$refs;
      var file = this.$refs.file.files[0];

      this.is_file_uploaded = true;

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
        // data: data,
      };

      this.$http
        .post(
          // "/api/related_docs?corpus_id=WB&model_id=ALL_50&topn=10&clean_doc=true",
          "/api/related_docs?" + $.param(options),
          data,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
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
        })
        .finally(() => {
          this.is_searching = false;
        });

      if (this.lda_model_id != "") {
        options = {
          corpus_id: this.corpus_id,
          model_id: this.lda_model_id,
          topn_topics: 10,
          total_topic_score: 0.8,
          clean_doc: true,
        };

        this.$http
          .post("/api/lda_doc_topics?" + $.param(options), data, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
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
          })
          .finally(() => {
            this.is_searching = false;
          });
      }

      e.preventDefault();
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
