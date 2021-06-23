<template>
  <div>
    <header class="blog-header wbg-header">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-12 col-md-8">
            <h1 class="blog-title text-center" dir="auto">Document Explorer</h1>
          </div>
          <div class="col-12 col-md-8">
            <div class="input-group mb-3 mt-3" style="display: flex">
              <!-- <input
                v-model="search_text"
                type="text"
                class="form-control wbg-search-text pl-4"
                placeholder="Enter your keywords..."
                aria-label="Field for search"
                aria-describedby="basic-addon2"
                v-on:keyup.enter="sendToSearch()"
              />
              <div class="input-group-append">
                <button
                  @click="sendToSearch"
                  class="btn btn-primary wbg-search-button pr-4 pl-4"
                  type="button"
                >
                  Search
                </button>
              </div> -->
              <input
                v-model="search_text"
                type="text"
                class="form-control wbg-search-text pl-4"
                :placeholder="uploaded_file ? '' : 'Enter your keywords...'"
                aria-label="Field for search"
                aria-describedby="basic-addon2"
                v-on:keyup.enter="sendToSearch()"
              />
              <div v-if="hasUploadedFile" class="wbg-uploaded-file">
                <div class="truncated-title">
                  {{ this.uploaded_file.name }}
                </div>
                <i
                  class="fas fa-times fa-sm ml-2"
                  @click="removeFile"
                  aria-hidden="true"
                ></i>
              </div>
              <div
                id="submit_file"
                data-toggle="tooltip"
                data-placement="bottom"
                title="Upload a PDF or TXT document to search"
              >
                <div class="file-input">
                  <input
                    @change="fileUpload"
                    type="file"
                    name="file-input"
                    :value="file_input"
                    :disabled="hasUploadedFile"
                    id="file-input"
                    class="file-input__input"
                    data-toggle="tooltip"
                    data-placement="bottom"
                    title="Upload a PDF or TXT document to search"
                    accept=".txt,.doc,.docx,.pdf"
                  />
                  <i
                    title="Delete query"
                    v-show="
                      (search_text && search_text.length > 0) || file_input
                    "
                    @click="clearSearchInput"
                    style="
                      position: relative;
                      margin-left: -50px;
                      margin-right: 10px;
                      padding-right: 10px;
                      padding-left: 20px;
                      z-index: 999;
                    "
                    class="fas fa-times fa-sm"
                  />
                  <label class="file-input__label white-bg" for="file-input"
                    ><i
                      class="fas fa-file-upload fa-lg"
                      :style="hasUploadedFile ? 'color: gray' : ''"
                    ></i
                  ></label>
                </div>
              </div>
              <div class="input-group-append">
                <button
                  @click="sendToSearch()"
                  class="btn btn-primary wbg-search-button pr-4 pl-4"
                  type="button"
                >
                  Search
                </button>
              </div>
            </div>
          </div>
          <div class="col-12 col-md-8 text-center">
            <div class="form-check form-check-inline">
              <input
                v-model="search_type"
                class="form-check-input"
                type="radio"
                name="inlineRadioOptions"
                id="inlineRadio1"
                value="keyword"
                checked=""
              />
              <label class="form-check-label" for="inlineRadio1"
                >Keyword search</label
              >
            </div>
            <div class="form-check form-check-inline">
              <input
                v-model="search_type"
                class="form-check-input"
                type="radio"
                name="inlineRadioOptions"
                id="inlineRadio2"
                value="semantic"
              />
              <label class="form-check-label" for="inlineRadio2"
                >Semantic search</label
              >
            </div>
          </div>
        </div>
      </div>
    </header>
    <div class="container">
      <div class="row justify-content-center mb-5">
        <div class="col-12 col-md-10">
          <h3 class="text-center">
            Explore our corpus of {{ corpus_size.toLocaleString() }} documents
          </h3>
          <div v-if="last_update_date" class="small text-center">
            Last updated on {{ last_update_date.toDateString() }}
          </div>

          <p class="mt-4 text-center">
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

          <p class="mt-4 text-center">
            For the full World Bank documents and open access repositories,
            visit the
            <a
              href="https://documents.worldbank.org/en/publication/documents-reports"
              target="_blank"
              >Documents and Reports</a
            >
            portal and the
            <a href="https://openknowledge.worldbank.org/" target="_blank"
              >Open Knowledge Repository (OKR)</a
            >
            website.
          </p>
        </div>
      </div>
      <div class="row mb-2">
        <div class="col-12 col-md-4">
          <div class="wbg-homepage-block">
            <div class="wbg-homepage-block__fa">
              <i class="fas fa-search fa-lg" aria-hidden="true"></i>
            </div>
            <h3><router-link to="/search">Search</router-link></h3>
            <p>
              Find documents by applying keyword and semantic search and filters
            </p>
          </div>
        </div>
        <div class="col-12 col-md-4">
          <div class="wbg-homepage-block">
            <div class="wbg-homepage-block__fa">
              <i class="fas fa-book-open fa-lg" aria-hidden="true"></i>
            </div>
            <h3><router-link to="/explore">Explore</router-link></h3>
            <p>
              Explore the corpus: geographic coverage, trends, topics,
              embeddings, etc.
            </p>
          </div>
        </div>
        <!-- <div class="col-12 col-md-4">
          <div class="wbg-homepage-block">
            <div class="wbg-homepage-block__fa">
              <i class="fas fa-chart-bar fa-lg" aria-hidden="true"></i>
            </div>
            <h3><a href="/#">Analyze</a></h3>
            <p>Do an analysis in the Corpus of research</p>
          </div>
        </div> -->
        <div class="col-12 col-md-4">
          <div class="wbg-homepage-block">
            <div class="wbg-homepage-block__fa">
              <i class="fas fa-map-marker-alt fa-lg" aria-hidden="true"></i>
            </div>
            <h3>
              <router-link to="/methods">Methods &amp; Tools</router-link>
            </h3>
            <p>
              Learn about the tools, techniques, and models that we used in this
              application
            </p>
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="wbg-homepage-block">
            <div class="wbg-homepage-block__fa">
              <i class="fas fa-link fa-lg" aria-hidden="true"></i>
            </div>
            <h3><router-link to="/content-api">API</router-link></h3>
            <p>Learn about, and access, our API services</p>
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="wbg-homepage-block">
            <div class="wbg-homepage-block__fa">
              <i class="fab fa-github fa-lg" aria-hidden="true"></i>
            </div>
            <h3>
              <a
                href="https://github.com/worldbank/wb-nlp-tools"
                target="_blank"
                >Github</a
              >
            </h3>
            <p>Review the code at our Github repo</p>
          </div>
        </div>
      </div>
      <!-- <div class="row mb-5">
        <div class="col-12">
          <h2 class="text-center mb-4">Highlights</h2>
        </div>
        <div class="col-12 col-md-4 mb-3 mb-md-1">
          <div class="wbg-homepage-highlight">
            <img
              src="/static/files/photo-1532094349884-543bc11b234d"
              height="220"
              alt=""
            />
            <div>
              <h4><a href="/#">JDC Quarterly Digest</a></h4>
              <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-4 mb-3 mb-md-1">
          <div class="wbg-homepage-highlight">
            <img
              src="/static/files/photo-1605962589069-bccdb6e391fe"
              height="220"
              alt=""
            />
            <div>
              <h4>
                <a href="/#"
                  >A Primer: The concsequences of COVID-19 on forced
                  displacement</a
                >
              </h4>
              <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-4 mb-3 mb-md-1">
          <div class="wbg-homepage-highlight">
            <img
              src="/static/files/photo-1533645782036-997947a9d529"
              height="220"
              alt=""
            />
            <div>
              <h4>
                <a href="/#"
                  >Understanding the socioeconomic conditions of refugees in
                  Kenya</a
                >
              </h4>
              <p>Lorem ipsum dolor sit amet, consectetur.</p>
            </div>
          </div>
        </div>
        <div class="col-12 text-center mt-4">
          <a href="/#">View more highlights</a>
        </div>
      </div> -->
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
  data: function () {
    return {
      search_text: "",
      search_type: "keyword",
      uploaded_file: null,
      file_input: null,
      search_text_cache: "",
      corpus_size: "",
      last_update: null,
      last_update_date: null,
    };
  },
  mounted() {
    this.getCorpusSize();
    this.getLastUpdateDate();
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
    getLastUpdateDate() {
      this.$http.get("/nlp/corpus/get_last_update_date").then((response) => {
        this.last_update = response.data;
        if (this.last_update) {
          this.last_update_date = new Date(this.last_update.last_update_date);
        }
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
</style>