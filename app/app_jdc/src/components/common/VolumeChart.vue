<template>
  <div>
    <div>
      <h4>Documents by {{ field_name }}</h4>
      <b-form-radio-group
        v-model="docs_value"
        value-field="item"
        text-field="name"
        :options="group_value_options"
      />
      <br />

      <b-row>
        <b-col>
          <v-chart
            class="chart"
            ref="graphChartDocs"
            :option="defaultOptions"
            :autoresize="true"
            :loading="loading"
          />
        </b-col>
      </b-row>

      <br />
      <br />
    </div>

    <div>
      <h4>Tokens by {{ field_name }}</h4>
      <b-form-radio-group
        v-model="tokens_value"
        value-field="item"
        text-field="name"
        :options="group_value_options"
      />
      <br />

      <b-row>
        <b-col>
          <v-chart
            class="chart"
            ref="graphChartTokens"
            :option="defaultOptions"
            :autoresize="true"
            :loading="loading"
          />
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import { use } from "echarts/core";
import VChart from "vue-echarts";

import {
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  DataZoomInsideComponent,
  DataZoomSliderComponent,
  ToolboxComponent,
} from "echarts/components";
import { GraphChart, LinesChart, LineChart, BarChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";

use([
  TooltipComponent,
  LegendComponent,
  GraphChart,
  CanvasRenderer,
  LinesChart,
  LineChart,
  BarChart,
  GridComponent,
  DataZoomComponent,
  DataZoomInsideComponent,
  DataZoomSliderComponent,
  ToolboxComponent,
]);

export default {
  name: "VolumeChart",
  components: {
    VChart,
  },
  props: {
    grid_top: {
      type: Number,
      default: null,
    },
    field: String,
    field_name: String,
    data: {
      type: Object,
      default: function () {
        return null;
      },
    },
  },
  mounted() {
    // this.docs_data = this.data.docs;
    // this.tokens_data = this.data.tokens;
    window.vvm = this;
    this.updateCharts();
  },
  computed: {
    defaultOptions() {
      var opts = {
        // title: {
        //   text: this.field_name + " volume",
        // },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#6a7985",
            },
          },
        },
        legend: {
          data: [],
        },
        toolbox: {
          feature: {
            // dataZoom: {
            //   yAxisIndex: "none",
            // },
            // restore: {},
            saveAsImage: {},
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "10%",
          containLabel: true,
        },
        xAxis: [
          {
            type: "category",
            boundaryGap: false,
            data: [],
          },
        ],
        yAxis: [
          {
            type: "value",
            axisLabel: {
              formatter: "{value}",
            },
          },
        ],
        dataZoom: [
          {
            type: "inside",
            start: 20,
            end: 100,
          },
          {
            start: 20,
            end: 100,
            handleIcon:
              "M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z",
            handleSize: "50%",
            handleStyle: {
              color: "#fff",
              shadowBlur: 3,
              shadowColor: "rgba(0, 0, 0, 0.6)",
              shadowOffsetX: 2,
              shadowOffsetY: 2,
            },
          },
        ],
        series: [],
      };

      if (this.grid_top) {
        opts.grid.top = this.grid_top;
      }
      return opts;
    },
  },
  data: function () {
    return {
      loading: false,
      docs_data: null,
      tokens_data: null,

      docs_value: "volume",
      tokens_value: "volume",

      group_value_options: [
        { item: "volume", name: "By volume" },
        { item: "share", name: "By share" },
      ],
    };
  },
  methods: {
    updateOption(data, value, label) {
      console.log(label);
      return {
        // title: {
        //   text: "Data" + "(" + label + ")",
        // },
        legend: {
          data: data[value].legend,
        },
        xAxis: [
          {
            type: "category",
            boundaryGap: false,
            data: data[value].year,
          },
        ],
        yAxis: [
          {
            type: "value",
            axisLabel: {
              formatter: value === "share" ? "{value} %" : "{value}",
            },
          },
        ],
        series: data[value].series,
      };
    },
    updateCharts() {
      this.docs_data = this.data.docs;
      this.tokens_data = this.data.tokens;

      this.$refs.graphChartDocs.setOption(
        this.updateOption(this.docs_data, this.docs_value, "Documents")
      );

      this.$refs.graphChartTokens.setOption(
        this.updateOption(this.tokens_data, this.tokens_value, "Tokens")
      );
    },
  },
  watch: {
    data() {
      this.updateCharts();
    },
    docs_value() {
      this.$refs.graphChartDocs.setOption(
        this.updateOption(this.docs_data, this.docs_value, "Documents")
      );
    },
    tokens_value() {
      this.$refs.graphChartTokens.setOption(
        this.updateOption(this.tokens_data, this.tokens_value, "Tokens")
      );
    },
    loading() {
      if (this.loading === false) {
        this.updateCharts();
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.chart {
  height: 420px;
}
</style>
