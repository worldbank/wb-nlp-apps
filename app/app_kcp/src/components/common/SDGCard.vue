<template>
  <!-- https://sdg-tracker.org/ -->
  <div>
    <div class="row justify-content-center sdg-group">
      <div class="col-12">
        <p class="lead">
          <a :href="result.url_data" target="_blank">{{ result.name }}</a>
        </p>
      </div>

      <div class="col-md-auto align-self-center">
        <img width="175px" :src="result.img_uri" />
      </div>
      <div class="col-9 align-self-center">
        <p>
          <span class="sdg-title">Goal {{ result.goal }}</span
          >: {{ result.goal_title }}
        </p>
        <!-- <br /> -->
        <p>
          <span class="sdg-title">Target {{ result.target }}</span
          >: {{ result.target_title }}
        </p>
        <!-- <br /> -->
        <p>
          <span class="sdg-title">Indicator {{ result.indicator }}</span
          >: {{ result.indicator_description }}
        </p>
      </div>

      <!-- <div class="col-5 offset-md-3">
        <div v-if="indicator_meta">
          <div class="wdi-definition">
            <p>
              {{
                indicator_meta.Shortdefinition || indicator_meta.Longdefinition
              }}
            </p>
          </div>
        </div>
        <hr />
      </div> -->
    </div>
  </div>
</template>
<script>
export default {
  name: "SDGCard",
  props: {
    result: Object,
  },
  mounted() {
    window.sdg_card = this;
    // this.getIndicatorMetadata(this.result);
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
    // searchParams() {
    //   const params = new URLSearchParams();
    //   params.append("url_meta", this.result.url_meta);
    //   return params;
    // },
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
    // getIndicatorMetadata() {
    //   this.$http
    //     .get(this.$config.extra_url.sdg + "/get_wdi_metadata", {
    //       params: this.searchParams,
    //     })
    //     .then((response) => {
    //       this.indicator_meta = response.data;
    //     });
    // },
  },
  watch: {},
};
</script>
<style scoped>
.sdg-group {
  margin-top: 20px !important;
  margin-bottom: 75px !important;
}
.sdg-title {
  font-weight: bold;
}
</style>