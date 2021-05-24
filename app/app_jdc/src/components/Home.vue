<template>
  <div>
    <Banner />
    <div class="container home-container">
      <div class="row justify-content-center mb-5">
        <div class="col-12 col-md-12">
          <h3 class="text-justify">
            Explore our corpus of {{ corpus_size.toLocaleString() }} documents
          </h3>
          <p class="small text-justify">
            Last updated on Wednesday, April 31, 2021
          </p>
          <p class="mt-4 text-justify">
            The Document Explorer puts Natural Language Processing (NLP) at the
            service of knowledge discovery. We compiled and maintain a
            <a href="/#">corpus of research</a>, project and other documents
            from development agencies. Topic and word embeddings models, and
            other methods are applied to provide information discovery solutions
            including <a href="/#">lexical and semantic search</a>, filtering by
            topic composition, and others. A <a href="/#">meta-database</a> is
            created, which provides a detailed description of all documents and
            can be used as input to analysis of knowledge on development. All
            solutions implemented in this project rely on publicly-available
            documents and on <a href="/#">open source tools</a>. Our solutions
            are openly accessible in our <a href="/#">GitHub repository</a>.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Banner from "./Banner";
export default {
  name: "Home",
  components: { Banner },
  data: function () {
    return {
      search_text: "",
      search_type: "keyword",
      uploaded_file: null,
      file_input: null,
      search_text_cache: "",
      corpus_size: "",
    };
  },
  mounted() {
    this.getCorpusSize();
  },
  computed: {
    hasUploadedFile() {
      if (this.uploaded_file !== null) {
        if (this.uploaded_file.name !== undefined) {
          return true;
        }
      }
      return false;
    },
  },
  methods: {
    fileUpload(event) {
      this.uploaded_file = event.target.files[0];
      this.search_text_cache = this.search_text;
      this.search_text = "";
      this.search_type = "semantic";
    },
    clearSearchInput() {
      this.search_text_cache = "";
      this.removeFile();
    },
    removeFile() {
      this.uploaded_file = null;
      this.file_input = null;
      this.search_text = this.search_text_cache;
    },
    sendToSearch() {
      this.$router.push({
        name: "search",
        query: {
          search_type: this.search_type,
          search_text: this.search_text,
        },
        params: {
          uploaded_file: this.uploaded_file,
        },
      });

      return;
    },
    getCorpusSize() {
      this.$http.get("/nlp/corpus/get_corpus_size").then((response) => {
        this.corpus_size = response.data.size;
      });
    },
  },
};
</script>
<style scoped>
.white-bg {
  background-color: white;
}
.fa-times:hover {
  color: red;
}
.container-margin {
  margin-top: 15px;
}

.wbg-header {
  margin: 0px;
}

.home-container {
  padding-top: 30px !important;
}

.input-height-auto {
  height: auto;
}

.jdc-homepage-block {
  margin-top: 50px !important;
}
</style>