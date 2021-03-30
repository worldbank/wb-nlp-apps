<template>
  <div>
    <div class="row wdi-group">
      <div class="col-12">
        <p class="lead">
          <a :href="result.url_wb" target="_blank">{{ result.name }}</a>
        </p>
      </div>
      <div class="col-4">
        <!-- <div class="col-4" v-view="viewHandler"> -->
        <!-- v-if="result.url_wb && viewEvent.percentInView > 0.9" -->
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

      <div class="col-4 offset-md-4">
        <a :href="result.url_data" target="_blank">Link to data</a>
        <br />
        <a :href="result.url_meta" target="_blank">Link to metadata</a>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "WDICard",
  props: {
    result: Object,
  },
  mounted() {
    this.getSimilarWDI();
  },
  data() {
    return {
      indicator_name: null,
      //   viewEvent: {
      //     type: "",
      //     percentInView: 0,
      //     percentTop: 0,
      //     percentCenter: 0,
      //   },
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
  },
  watch: {},
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
</style>