<template>
  <div>
    <div v-for="result in results" :key="'microdata-' + result.id">
      <p class="lead">
        <a :href="metadataLink(result)" target="_blank">{{ result.name }}</a>
      </p>
      <p>{{ result.id }}</p>
      <br />
      <br />
    </div>
  </div>
</template>
<script>
export default {
  components: {},
  name: "SimilarMicrodataViewer",
  props: {
    render_style: {
      default: "horizontal",
      type: String,
    },
    doc_id: String,
    topn: {
      type: Number,
      default: 10,
    },
  },
  mounted() {
    this.getSimilarMicrodata();
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
    };
  },
  methods: {
    metadataLink(result) {
      return (
        "https://microdata.worldbank.org/index.php/api/catalog/" + result.id
      );
    },
    getIndicatorName(result) {
      if (result.url_wb) {
        var name = result.url_wb.split("/");
        this.indicator_name = name[name.length - 1];
        return this.indicator_name;
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
</style>