<template>
  <div>
    <Banner />
    <div class="container home-container">
      <div class="row justify-content-center mb-5">
        <div class="col-12 col-md-12">
          <h2 class="text-center">
            A catalog of {{ corpus_size.toLocaleString() }} documents related to
            forced displacement
          </h2>
          <p class="text-center jdc-update-class">
            Last updated on Wednesday, April 31, 2021
          </p>

          <p class="mt-4 text-justify">
            The JDC Document Explorer exploits natural language processing (NLP)
            techniques to improve the discoverability of documents related to
            forced displacement, and to assess the scope and coverage of these
            documents. We applied topic models, word embedding models, and other
            information extraction methods to a large corpus of publications and
            project documents made publicly available by the UNHCR and
            multilateral development banks. This resulted in a document catalog
            with
            <router-link to="/search"
              >lexical and semantic searchability</router-link
            >, and in an <router-link to="/explore">exploration</router-link> of
            the composition and evolution over time of this knowledge base on
            forced displacement, by source, topic, geographic coverage, and type
            of document.
          </p>
          <p class="mt-4 text-justify">
            The Joint Data Center on Forced Displacement (JDC) was established
            to enhance the ability of stakeholders to make timely and
            evidence-informed decisions that can improve the wellbeing of
            forcibly displaced populations. Among these stakeholders are the
            multilateral development banks (MDBs): the World Bank, the African
            Development Bank (AfDB), the Asian Development Bank (ADB), the
            European Bank for Reconstruction and Development (EBRD), and the
            Inter-American Development Bank (IDB), who play a critical role in
            financing and implementing their shareholders policies and programs.
            In 2016, the MDBs had issued a joint statement expressing their
            commitment to working together, and within their respective
            institutional mandates, to respond to the global forced displacement
            crisis.
          </p>
          <p class="mt-4 text-justify">
            The objective of the Document Explorer project was to support the
            monitoring of the scope and coverage of MDB's projects and programs
            related to forced displacement, identify gaps in research and
            analytical work, and provide tools to researchers and project
            managers to easily discover useful information in this vast
            knowledge repository. MDBs make much of their respective research
            output and project documents publicly available. We built a
            largely-automated system to extract and organize information
            contained in these documents, and to describe how MDBs, over time
            and across countries, address forced displacement and related
            issues.
          </p>
          <p class="mt-4 text-justify">
            The JDC Document Explorer is built on a more generic
            <router-link to="/">Document Explorer</router-link> developed and
            maintained by the World Bank Development Data Group, with support of
            the Joint Data Center (project P174148) and of the Knowledge for
            Change Program (KCP, project P173741). The NLP methods (text
            preparation and modeling) used in this application are openly
            accessible.
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
      this.$http
        .get("/nlp/corpus/get_corpus_size?app_tag_jdc=true")
        .then((response) => {
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

.jdc-update-class {
  color: #999;
  font-weight: 600;
  margin-top: 10px;
  padding-bottom: 0px !important;
}
</style>