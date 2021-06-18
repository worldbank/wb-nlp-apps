<template>
  <div>
    <MicrodataCard
      v-for="result in results"
      :key="'microdata-' + result.id"
      :result="result"
      :metadata="metadata"
    />
    <div v-show="loading" class="text-center"><b-spinner></b-spinner></div>
  </div>
</template>
<script>
import MicrodataCard from "./MicrodataCard";

export default {
  components: { MicrodataCard },
  name: "SimilarMicrodataViewer",
  props: {
    doc_id: String,
    topn: {
      type: Number,
      default: 10,
    },
  },
  mounted() {
    this.loadKCPMetadata();
  },
  computed: {
    searchParams() {
      const params = new URLSearchParams();
      params.append("model_id", this.$config.default_model.word2vec.model_id);
      params.append("doc_id", this.doc_id);
      params.append("topn", this.topn);
      return params;
    },
  },
  data() {
    return {
      results: [],
      loading: false,
      indicator_name: null,
      metadata: null,
    };
  },
  methods: {
    loadKCPMetadata() {
      if (!this.metadata) {
        this.loading = true;
        this.$http
          .get("/static/data/kcp_microdata_metadata_minified.json")
          .then((response) => {
            this.metadata = response.data;
            this.getSimilarMicrodata();
            this.loading = false;
          });
      }
    },
    getSimilarMicrodata() {
      this.loading = true;
      this.$http
        .get(
          this.$config.extra_url.microdata +
            "/get_similar_indicators_by_doc_id",
          {
            params: this.searchParams,
          }
        )
        .then((response) => {
          this.results = response.data;
        });
    },
  },
  watch: {
    doc_id: function () {
      this.getSimilarMicrodata();
    },
  },
};
</script>
<style scoped>
.vue-horizontal {
  /* border: 3px solid #dbdbdb; */
  border: 0px;
  padding: 5px;
}
.microdata-related-section {
  /* width: 40vh; */
  width: 100%;
  padding: 0px 20px;
  margin: 3px;
  height: 400px;
  background: #ffffff;
  /* background: #f3f3f3; */
  border: 2px solid #ebebeb;
  border-radius: 4px;
  margin-bottom: 20px;
}

.microdata-info {
  border: 0px;
}
</style>