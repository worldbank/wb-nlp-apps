<template>
  <div class="meta-wrapper">
    <div v-if="metadata" style="word-wrap: break-word">
      <vue-json-pretty :data="metadata" :highlightMouseoverNode="true">
      </vue-json-pretty>
    </div>
  </div>
</template>
<script>
// import MapChart from "@avsolatorio/vue-map-chart";
import VueJsonPretty from "vue-json-pretty";
import "vue-json-pretty/lib/styles.css";

export default {
  props: {
    metadata: Object,
    show_raw_metadata: Boolean,
  },
  components: { VueJsonPretty },
  mounted() {},
  data() {
    return {};
  },
  computed: {},
  methods: {},
  watch: {},
};
</script>
<style scoped>
.meta-wrapper {
  max-height: 70vh;
  overflow-y: scroll;
}
</style>