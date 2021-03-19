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
              <input
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
          <h3 class="text-center">Explore our corpus of 300,000 documents</h3>
          <div class="small text-center">
            Last updated on Wednesday, January 6, 2021
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
              Explore the corpus: topic composition, trends, geographic
              coverage, word embeddings, etc.
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
              <a href="https://github.com/avsolatorio/wb_nlp" target="_blank"
                >Github</a
              >
            </h3>
            <p>Review the code at our Github repo</p>
          </div>
        </div>
      </div>
      <div class="row mb-5">
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
      </div>
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
    };
  },
  methods: {
    sendToSearch() {
      this.$router.push({
        path: "search",
        query: { search_type: this.search_type, search_text: this.search_text },
      });

      return;
    },
  },
};
</script>
