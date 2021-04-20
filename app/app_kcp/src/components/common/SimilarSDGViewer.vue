<template>
  <div>
    <div v-if="results.length === 0">
      <b-skeleton-img height="300px"></b-skeleton-img>
    </div>

    <vue-horizontal v-if="results.length > 0 && render_style === 'horizontal'">
      <div
        class="sdg-related-section"
        v-for="result in results"
        :key="'sdg_' + result.id"
      >
        <SDGCard :result="result" />
      </div>
    </vue-horizontal>

    <div v-if="results.length > 0 && render_style === 'vertical'">
      <div
        class="sdg-related-section"
        v-for="result in results"
        :key="'sdg_' + result.id"
      >
        <SDGCard :result="result" />
      </div>
    </div>
  </div>
</template>
<script>
import VueHorizontal from "vue-horizontal";
import SDGCard from "./SDGCard";
export default {
  components: {
    SDGCard,
    VueHorizontal,
  },
  name: "SimilarSDGViewer",
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
    this.getSimilarSDG();
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
      // viewEvent: {
      //   type: "",
      //   percentInView: 0,
      //   percentTop: 0,
      //   percentCenter: 0,
      // },
    };
  },
  methods: {
    // viewHandler(e) {
    //   if (e.type === "exit") return;
    //   Object.assign(this.viewEvent, e);
    // },
    getIndicatorName(result) {
      if (result.url_wb) {
        var name = result.url_wb.split("/");
        this.indicator_name = name[name.length - 1];
        return this.indicator_name;
      }
    },
    getSimilarSDG() {
      this.loading = true;
      this.$http
        .get(this.$config.extra_url.sdg + "/get_similar_indicators_by_doc_id", {
          params: this.searchParams,
        })
        .then((response) => {
          this.results = response.data;
        });
    },
  },
  watch: {
    doc_id: function () {
      this.getSimilarSDG();
    },
  },
};
</script>
<style scoped>
.sdg-group {
  margin-top: 20px !important;
  margin-bottom: 75px !important;
}
.sdg-frame {
  box-sizing: content-box;
}

.vue-horizontal {
  /* border: 3px solid #dbdbdb; */
  border: 0px;
  padding: 5px;
}
.sdg-related-section {
  /* width: 40vh; */
  width: 100%;
  padding: 0px 20px;
  margin: 3px;
  height: 500px;
  background: #ffffff;
  /* background: #f3f3f3; */
  border: 2px solid #ebebeb;
  border-radius: 4px;
  margin-bottom: 20px;
}
</style>