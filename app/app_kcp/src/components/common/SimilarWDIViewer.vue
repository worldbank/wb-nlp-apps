<template>
  <div>
    <div v-if="results.length === 0">
      <b-skeleton-img height="300px"></b-skeleton-img>
    </div>
    <vue-horizontal v-if="results.length > 0">
      <div
        class="related-section"
        :style="'height: ' + panel_section_height + 'px;'"
        v-for="result in results"
        :key="'wdi_' + result.id"
      >
        <WDICard :result="result" />
        <!-- <div class="row wdi-group">
          <div class="col-12">
            <p class="lead">
              <a :href="result.url_wb" target="_blank">{{ result.name }}</a>
            </p>
          </div>
          <div class="col-4" v-view="viewHandler">
            {{ viewEvent }}
            <iframe
              class="wdi-frame"
              v-if="result.url_wb && viewEvent.percentInView > 0.9"
              loading="lazy"
              :src="
                'https://data.worldbank.org/share/widget?indicators=' +
                getIndicatorName(result) +
                '&view=map'
              "
              width="450"
              height="300"
              frameBorder="0"
              scrolling="no"
            ></iframe>
          </div>

          <div class="col-4 offset-md-4">
            <a :href="result.url_data" target="_blank">Link to data</a>
            <br />
            <a :href="result.url_meta" target="_blank">Link to metadata</a>
          </div>
        </div> -->
      </div>
    </vue-horizontal>
    <!--
  <div v-if="results.length > 0">
    <div class="row wdi-group" v-for="result in results" :key="result.id">
      <div class="col-12">
        <p class="lead">
          <a :href="result.url_wb" target="_blank">{{ result.name }}</a>
        </p>
      </div>

      <div class="col-6 mx-auto">
        <iframe
          class="wdi-frame"
          v-if="result.url_wb"
          loading="lazy"
          :src="
            'https://data.worldbank.org/share/widget?indicators=' +
            getIndicatorName(result) +
            '&view=map'
          "
          width="450"
          height="300"
          frameBorder="0"
          scrolling="no"
        ></iframe>
      </div>

      <div class="col-6">
        <a :href="result.url_data" target="_blank">Link to data</a>
        <br />
        <a :href="result.url_meta" target="_blank">Link to metadata</a>
      </div>
    </div> -->
  </div>
</template>
<script>
import VueHorizontal from "vue-horizontal";
import WDICard from "./WDICard";
export default {
  components: { WDICard, VueHorizontal },
  name: "SimilarWDIViewer",
  props: {
    doc_id: String,
    topn: {
      type: Number,
      default: 10,
    },
  },
  mounted() {
    window._satellite = {
      track: function (v) {
        console.log(v);
      },
    };
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
  margin-bottom: 75px !important;
}
.wdi-frame {
  box-sizing: content-box;
}

.vue-horizontal {
  /* border: 3px solid #dbdbdb; */
  border: 0px;
  padding: 5px;
}
.related-section {
  /* width: 40vh; */
  width: 100%;
  padding: 0px 20px;
  margin: 3px;
  height: 400px;
  background: #ffffff;
  /* background: #f3f3f3; */
  border: 2px solid #ebebeb;
  border-radius: 4px;
}
</style>