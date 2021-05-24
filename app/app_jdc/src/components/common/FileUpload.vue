<template>
  <div>
    <div data-v-3e4a7f3e="" class="file-upload">
      <!---->
      <div class="input-wrapper" style="opacity: 0.7">
        <input
          id="file-upload-input"
          type="file"
          name="file"
          accept=".txt, .pdf"
          disabled="disabled"
        /><label for="file-upload-input" class="file-upload-label"
          ><span class="file-upload-icon file-upload-icon-pulse">⇪</span>
          <div>Uploading file</div></label
        >
        <div
          class="file-upload-progress"
          style="width: 100%; display: block"
        ></div>
      </div>
    </div>

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
  </div>
</template>

<script>
import FileUpload from "v-file-upload";
import $ from "jquery";

export default {
  name: "FileUploadPanel",
  components: {
    FileUpload,
  },
  props: {
    page_title: String,
  },
  data: function () {
    // http://10.0.0.25:8880/api/related_words?raw_text=poverty&model_id=ALL_50
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
      // fileUploaded: null,
      is_searching: false,
      documents: [],
    };
  },
  mounted() {
    this.getRelatedWords();
  },
  computed: {
    uploading() {
      return this.progress > 0;
    },
    progressStyle() {
      return {
        width: `${this.progress}%`,
        display: this.uploading ? "block" : "none",
      };
    },
    inputWrapperStyle() {
      return { opacity: this.uploading ? "0.7" : "1" };
    },
    fileUploadInputName() {
      return "file-upload-input" + this.uniqueId;
    },
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
<style scoped >
h3 {
  margin: 40px 0 0;
}
.file-upload .input-wrapper {
  text-align: center;
  position: relative;
  background-color: #307dbf;
  height: 80px;
}
.file-upload .input-wrapper:hover {
  background-color: #2c70ac;
}
.file-upload .input-wrapper .file-upload-input {
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
}
.file-upload .input-wrapper .file-upload-label {
  width: 100%;
  font-size: 1.25em;
  color: #fff;
  display: inline-block;
  padding: 10px;
  position: absolute;
  left: 0;
  right: 0;
  z-index: 2;
  line-height: 1.4em;
}
.file-upload .input-wrapper .file-upload-label:hover {
  cursor: pointer;
}
.file-upload .input-wrapper .file-upload-label .file-upload-icon {
  display: inline-block;
  text-align: center;
  font-weight: bold;
  font-size: 40px;
}
.file-upload
  .input-wrapper
  .file-upload-label
  .file-upload-icon.file-upload-icon-pulse {
  animation: fade 1.5s infinite 0.5s;
}
.file-upload .input-wrapper .file-upload-progress {
  position: absolute;
  background-color: #47b04b;
  height: 100%;
  max-width: 100%;
  z-index: 1;
  transition: width 0.6s ease;
}
.file-upload .thumb-preview {
  display: flex;
  flex-flow: row wrap;
}
.file-upload .thumb-preview .thumb-preview-item {
  border-radius: 5px;
  margin: 5px;
  background-color: #ccc;
  height: 150px;
  width: 150px;
  padding: 0;
  position: relative;
}
.file-upload .thumb-preview .thumb-preview-item img {
  border-radius: 5px;
}
@-moz-keyframes fade {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
@-webkit-keyframes fade {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
@-o-keyframes fade {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
@keyframes fade {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
@-moz-keyframes fade {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
@-webkit-keyframes fade {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
@-o-keyframes fade {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
@keyframes fade {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
</style>
