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
        <br />
        <br />

        <a :href="result.url_data" target="_blank">Link to data</a>
        <br />
        <a :href="result.url_meta" target="_blank">Link to metadata</a>
      </div>

      <div class="col-5 offset-md-3">
        <div v-if="indicator_meta">
          <p class="lead">Definition</p>
          <div class="wdi-definition">
            <p>
              {{
                indicator_meta.Shortdefinition || indicator_meta.Longdefinition
              }}
            </p>
          </div>
        </div>
        <hr />
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
    window.wdi_card = this;
    this.getIndicatorMetadata(this.result);
  },
  data() {
    return {
      indicator_name: null,
      indicator_meta: null,
      //   viewEvent: {
      //     type: "",
      //     percentInView: 0,
      //     percentTop: 0,
      //     percentCenter: 0,
      //   },
    };
  },
  computed: {
    searchParams() {
      const params = new URLSearchParams();
      params.append("url_meta", this.result.url_meta);
      return params;
    },
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
    getIndicatorMetadata() {
      this.$http
        .get("/nlp/extra/wdi/get_wdi_metadata", { params: this.searchParams })
        .then((response) => {
          this.indicator_meta = response.data;
        });
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
.wdi-definition {
  max-height: 350px;
  overflow-y: scroll;
}
</style>