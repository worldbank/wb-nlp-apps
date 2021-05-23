<template>
  <div>
    <br />
    <h4>Related World Development Indicators</h4>

    <div v-if="wdi_results.length === 0">
      <b-skeleton-img height="300px"></b-skeleton-img>
    </div>

    <vue-horizontal
      v-if="wdi_results.length > 0 && render_style === 'horizontal'"
    >
      <div
        class="wdi-related-section"
        v-for="wresult in wdi_results"
        :key="'wdi_' + wresult.id"
      >
        <WDICard :result="wresult" />
      </div>
    </vue-horizontal>
    <br />
    <br />
    <h4>Related SDG Indicators</h4>

    <div v-if="sdg_results.length === 0">
      <b-skeleton-img height="300px"></b-skeleton-img>
    </div>

    <vue-horizontal
      v-if="sdg_results.length > 0 && render_style === 'horizontal'"
    >
      <div
        class="sdg-related-section"
        v-for="sresult in sdg_results"
        :key="'sdg_' + sresult.id"
      >
        <SDGCard :result="sresult" />
      </div>
    </vue-horizontal>
    <br />
    <br />
    <h4>Related microdata</h4>

    <div v-if="microdata_results.length > 0">
      <div v-for="result in microdata_results" :key="'microdata-' + result.id">
        <p class="lead">
          <a :href="metadataLink(result)" target="_blank">{{ result.name }}</a>
        </p>
        <p>{{ result.id }}</p>
        <br />
        <br />
      </div>
    </div>
  </div>
</template>

<script>
import VueHorizontal from "vue-horizontal";
import SDGCard from "./SDGCard";
import WDICard from "./WDICard";

export default {
  props: {
    indicators_data: Object,
    render_style: {
      default: "horizontal",
      type: String,
    },
  },
  components: { SDGCard, WDICard, VueHorizontal },
  mounted() {
    // window.viewer = this;
    window.document_indicators = this;
    this.updateData();
  },
  data() {
    return {
      loading: false,
      wdi_results: [],
      sdg_results: [],
      microdata_results: [],
    };
  },
  computed: {},
  methods: {
    updateData() {
      this.loading = true;
      this.wdi_results = [];
      this.sdg_results = [];
      this.microdata_results = [];

      this.wdi_results = this.indicators_data.wdi;
      this.sdg_results = this.indicators_data.sdg;
      this.microdata_results = this.indicators_data.microdata;

      this.loading = false;
    },
    metadataLink(result) {
      return (
        "https://microdatalib.worldbank.org/index.php/catalog/study/" +
        result.id
      );
    },
  },
  watch: {
    indicators_data: {
      deep: true,
      handler() {
        this.updateData();
      },
    },
    loading() {
      this.$emit("onLoadingStatusChanged", this.loading);
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
.wdi-related-section {
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
.sdg-related-section {
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