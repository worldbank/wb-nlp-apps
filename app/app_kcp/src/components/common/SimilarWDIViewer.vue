<template>
  <div v-if="results.length > 0">
    <div class="row wdi-group" v-for="result in results" :key="result.id">
      <div class="col-12">
        <p class="lead">{{ result.name }}</p>
      </div>

      <div class="col-4">
        <a :href="result.url_data" target="_blank">Link to data</a>
      </div>
      <div class="col-4">
        <a :href="result.url_meta" target="_blank">Link to metadata</a>
      </div>

      <div class="col-4">
        <a :href="result.url_wb" target="_blank">Link to World Bank page</a>
      </div>

      <!-- <div class="col-1"></div>
      <div class="col-11">{{ result.url_data }}</div>
      <div class="col-1"></div>
      <div class="col-11">{{ result.url_meta }}</div>
      <div class="col-1"></div>
      <div class="col-11">{{ result.url_wb }}</div> -->
    </div>
    <!--
    <ul v-if="results.length > 0">
      <li v-for="result in results" :key="result.id">{{ result.name }}</li>
    </ul> -->
  </div>
</template>
<script>
export default {
  name: "SimilarWDIViewer",
  props: {
    doc_id: String,
    topn: {
      type: Number,
      default: 10,
    },
  },
  mounted() {
    this.getSimilarWDI();
  },
  computed: {
    searchParams() {
      const params = new URLSearchParams();
      params.append("model_id", "777a9cf47411f6c4932e8941f177f90a");
      params.append("doc_id", this.doc_id);
      params.append("topn", this.topn);
      return params;
    },
  },
  data() {
    return {
      results: [],
      loading: false,
    };
  },
  methods: {
    getSimilarWDI() {
      this.loading = true;
      this.$http
        .get("/nlp/extra/wdi/get_similar_wdi_by_doc_id", {
          params: this.searchParams,
        })
        .then((response) => {
          this.results = response.data;
        });
    },
  },
  watch: {
    doc_id: function () {
      this.getSimilarWDI();
    },
  },
};
</script>
<style scoped>
.wdi-group {
  margin-top: 20px !important;
  margin-bottom: 50px !important;
}
</style>