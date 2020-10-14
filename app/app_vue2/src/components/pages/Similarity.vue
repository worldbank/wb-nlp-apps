<template>
  <div>
    <h1>{{ page_title }}</h1>
    <br />

    <b-container fluid>
      <b-row>
        <b-col cols="9" class="border-right">
          <!-- Word2vec is a simple embedding model. -->

          <FileUpload
            :url="'/api/empty'"
            accept=".txt,.pdf"
            :post_file="false"
            :progress="progress"
            @change="onFileChange"
          ></FileUpload>

          <!-- <div class="file-upload">
            <div class="input-wrapper"> -->
          <!-- <vueDropzone
            :include-styling="true"
            :options="dropzoneOptions"
            :useCustomSlot="true"
            @vdropzone-files-added="onFileChange"
          >
            <div class="dropzone-custom-content">
              <h3 class="dropzone-custom-title">
                Drag and drop to upload a document
              </h3>
              <div class="subtitle">
                ...or click to select a file from your computer
              </div>
            </div>
          </vueDropzone> -->
          <!-- </div>
          </div> -->
          <!--
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
                <input
                  type="submit"
                  v-on:click="uploadFile"
                  :disabled="isReady() === false"
                />
              </form>
            </div>
          </div> -->
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
import FileUpload from "@avsolatorio/v-file-upload";
// import vue2Dropzone from "vue2-dropzone";
// import "vue2-dropzone/dist/vue2Dropzone.min.css";

import $ from "jquery";

export default {
  name: "Similarity",
  components: {
    FileUpload,
    // vueDropzone: vue2Dropzone,
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
      progress: 0,
      // fileUploaded: null,
      is_searching: false,
      documents: [],
      dropzoneOptions: {
        url: "https://httpbin.org/post",
        thumbnailWidth: 200,
        addRemoveLinks: true,
      },
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

      // this.$http
      //   .post(
      //     // "/api/related_docs?corpus_id=WB&model_id=ALL_50&topn=10&clean_doc=true",
      return "/api/related_docs?" + $.param(options);
    },
  },
  methods: {
    isSuccess: function (e) {
      window.esuccess = e;
    },
    onFileChange: function (file) {
      this.progress = 0.1;
      // this.fileUploaded = file;
      window.anexo = file;
      file = file["file"];
      window.uploaded_file = file;
      window.fup = file;

      // var data = new FormData();
      // data.append("file", file);

      // this.$http
      //   .post(
      //     // "/api/related_docs?corpus_id=WB&model_id=ALL_50&topn=10&clean_doc=true",
      //     "/api/upload_file",
      //     data,
      //     {
      //       headers: {
      //         "Content-Type": "multipart/form-data",
      //       },
      //     }
      //   )
      //   .then((response) => {
      //     let data = response.data;
      //     window.uploaded_file = data;
      //   })
      //   .catch((error) => {
      //     console.log(error);
      //     this.errors.push(error);
      //     this.errored = true;
      //     this.is_searching = false;
      //   })
      //   .finally(() => {
      //     this.is_searching = false;
      //   });

      this.postUploadedFile(file);
    },
    isReady: function () {
      return true;
    },

    onProgress(e) {
      this.progress = parseInt((e.loaded * 100) / e.total);
      console.log(this.progress);
      // this.$emit("progress", this.progress);
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

      var config = {
        onUploadProgress: this.onProgress,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };

      this.$http
        .post(
          // "/api/related_docs?corpus_id=WB&model_id=ALL_50&topn=10&clean_doc=true",
          "/api/related_docs?" + $.param(options),
          data,
          config
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
/*
.file-upload .input-wrapper {
  text-align: center;
  position: relative;
  background-color: #307dbf;
  height: 80px;
}
.file-upload .input-wrapper:hover {
  background-color: #2c70ac;
}

.dropzone-custom-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.dropzone-custom-title {
  margin-top: 0;
  color: #00b782;
}

.subtitle {
  color: #314b5f;
} */
</style>
