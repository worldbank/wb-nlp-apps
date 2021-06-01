<template>
  <!-- https://sdg-tracker.org/ -->
  <div>
    <div class="row justify-content-center sdg-group">
      <div class="col-12 sdg-name">
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
        <p>
          <span class="sdg-title">Target {{ result.target }}</span
          >: {{ result.target_title }}
        </p>
        <p>
          <span class="sdg-title">Indicator {{ result.indicator }}</span
          >: {{ result.indicator_description }}
        </p>
      </div>
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
    // window.sdg_card = this;
  },
  data() {
    return {};
  },
  computed: {},
  methods: {},
  watch: {},
};
</script>
<style scoped>
.sdg-name {
  margin-bottom: 15px;
}
.sdg-group {
  margin-top: 20px !important;
  /* margin-bottom: 75px !important; */
}
.sdg-title {
  font-weight: bold;
}
</style>