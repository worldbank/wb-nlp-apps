<template>
  <div class="vue-world-map">
    <WBMap
      @hoverCountry="onHoverCountry"
      @hoverLeaveCountry="onHoverLeaveCountry"
    />
    <div
      v-if="legend.name"
      class="vue-map-legend"
      :style="'left:' + position.left + 'px; top: ' + position.top + 'px'"
    >
      <div class="vue-map-legend-header">
        <span>{{ legend.name }}</span>
      </div>
      <div class="vue-map-legend-content">
        <span>{{ processedCountryData[legend.code] || 0 }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import chroma from "chroma-js";
import WBMap from "../wb/WBMap";
import {
  getDynamicMapCss,
  getBaseCss,
  getCombinedCssString,
} from "../../js/dynamic-map-css";
let legend = {
  data: null,
  code: null,
  name: null,
};
let position = {
  left: 0,
  top: 0,
};
export default {
  name: "WBMapChart",
  components: { WBMap },
  watch: {
    countryData() {
      this.renderMapCSS();
    },
  },
  props: {
    nodeId: {
      type: String,
      default: "mapChartStyleNode",
    },
    lowColor: {
      type: String,
      default: "#fde2e2",
    },
    highColor: {
      type: String,
      default: "#d83737",
    },
    chromaScaleOn: {
      type: Boolean,
      default: true,
    },
    countryData: {
      type: Object,
      required: true,
    },
    defaultCountryFillColor: {
      type: String,
      default: "#dadada",
    },
    countryStrokeColor: {
      type: String,
      default: "#909090",
    },
    countryStrokeWidth: {
      type: String,
      default: "0.5px",
    },
    xxxMaskStrokeWidth: {
      type: String,
      default: "0.75px",
    },
    xxxStrokeDashArray: {
      type: String,
      default: "1 1",
    },
    legendHeaderBackgroundColor: {
      type: String,
      default: "white",
    },
    legendContentBackgroundColor: {
      type: String,
      default: "#dadbda8f",
    },
    legendFontColorHeader: {
      type: String,
      default: "black",
    },
    legendFontColorContent: {
      type: String,
      default: "black",
    },
    legendBorderColor: {
      type: String,
      default: "gray",
    },
    legendBorderRadius: {
      type: Number,
      default: 5,
    },
    legendBoxShadow: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      processedCountryData: null,
      legend: legend,
      position: position,
      node: this.getOrCreateNode(),
      chromaScale: chroma.scale([this.$props.lowColor, this.$props.highColor]),
    };
  },
  methods: {
    processCountryData() {
      var totalCount = Object.values(this.countryData).reduce((a, b) => a + b);

      var processedCountryData = this.countryData;
      Object.keys(this.countryData).forEach(
        (k) => (processedCountryData[k] = processedCountryData[k] / totalCount)
      );

      var cnVal = this.countryData.CN || 0;
      var inVal = this.countryData.IN || 0;
      var sdudVal = this.countryData.SD || 0;
      var ssudVal = this.countryData.SS || 0;

      // Set values for disputed areas
      if (cnVal + inVal > 0) {
        processedCountryData.XXX_arunachal_pradesh = (cnVal + inVal) / 2;
        processedCountryData.XXX_demchok = (cnVal + inVal) / 2;
        processedCountryData.XXX_aksai_chin = (cnVal + inVal) / 2;
      }

      if (sdudVal + ssudVal > 0) {
        processedCountryData.XXX_abyei = (sdudVal + ssudVal) / 2;
      }

      processedCountryData.XXX_western_sahara = "No data";

      this.processedCountryData = processedCountryData;
    },
    getOrCreateNode() {
      var node = document.getElementById(this.nodeId);
      if (!node) {
        node = document.createElement("style");
        node.id = this.nodeId;
      }
      return node;
    },
    onHoverCountry(country) {
      if (
        country.code.startsWith("XXX_") &&
        country.name !== "Western Sahara"
      ) {
        return;
      }
      this.legend = country;
      this.position = country.position;
      this.$emit("hoverCountry", country);
    },
    onHoverLeaveCountry(country) {
      this.legend = {
        data: null,
        code: null,
        name: null,
      };
      this.$emit("hoverLeaveCountry", country);
    },
    renderMapCSS() {
      this.processCountryData();
      const baseCss = getBaseCss(this.$props);
      const dynamicMapCss = getDynamicMapCss(
        // this.$props.countryData,
        this.$data.processedCountryData,
        this.chromaScale,
        this.$props.highColor,
        this.$props.chromaScaleOn
      );
      this.$data.node.innerHTML = getCombinedCssString(baseCss, dynamicMapCss);
    },
  },
  mounted() {
    document.body.appendChild(this.$data.node);

    this.renderMapCSS();
  },
};
</script>

<style scoped>
.vue-world-map,
#map-svg {
  height: 100%;
}
.vue-world-map {
  position: relative;
}
.vue-map-legend {
  width: 185px;
  background: #fff;
  overflow: auto;
  border: 1px solid;
  position: absolute;
}
.vue-map-legend-header {
  padding: 10px 15px;
}
.vue-map-legend-content {
  padding: 10px 15px;
  background: #dadbda8f;
  border-top: 1px solid #acacad;
}
</style>