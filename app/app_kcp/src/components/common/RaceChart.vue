<template>
  <div v-if="flags && data">
    <div style="overflow: hidden; margin-right: 50px">
      <b-button
        style="float: right"
        @click="startRace('reset')"
        :variant="resetButtonVariant"
        :disabled="disableReset"
        >Reset</b-button
      >

      <b-button
        style="float: right; margin: 0 10px 0 10px"
        @click="setPauseEvent()"
        :variant="pauseButtonVariant"
        :disabled="disablePause"
        >{{ paused ? "Resume" : "Pause" }}</b-button
      >
    </div>
    <br />
    <v-chart class="chart" :option="option" ref="myChart" :autoresize="true" />
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
  GraphicComponent,
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
  GraphicComponent,
]);

export default {
  name: "RaceAChart",
  components: { VChart },
  mounted() {
    window.rvm = this;
    this.fetchData();
    if (this.input_data.length > 0) {
      this.loadInputData();
    }
  },
  props: {
    input_data: {
      type: Array,
      default: function () {
        return [];
      },
    },
    iso3map: Object,
  },
  watch: {
    isReady() {
      if (this.isReady) {
        this.dynamicOption = this.option;
        this.startRace();
        this.$emit("ready", this.isReady);
      }
    },
    input_data() {
      if (this.input_data.length > 0) {
        this.loadInputData();
      }
    },
    // paused() {
    //   console.log("Pause changed...");
    //   if (this.paused) {
    //     this.clearQueue();
    //   } else {
    //     this.startIndex = this.years.indexOf(this.current_year);
    //     this.startRace();
    //   }
    // },
  },
  computed: {
    disableReset() {
      return !this.stopped && !this.paused;
    },
    disablePause() {
      return this.current_year === this.years[this.years.length - 1];
    },
    resetButtonVariant() {
      var variant = "outline-secondary";

      if (this.stopped || this.paused) {
        variant = "primary";
      }
      return variant;
    },
    pauseButtonVariant() {
      var variant = "primary";

      if (this.paused) {
        variant = "success";
      }
      if (this.current_year === this.years[this.years.length - 1]) {
        variant = "outline-secondary";
      }
      return variant;
    },
    startYear() {
      return this.years[this.startIndex];
    },
    isReady() {
      return this.data_loaded && this.flags;
    },
    option() {
      let vm = this;
      return {
        grid: {
          top: 10,
          bottom: 30,
          left: 150,
          right: 80,
        },
        xAxis: {
          max: "dataMax",
          label: {
            formatter: function (n) {
              return Math.round(n);
            },
          },
        },
        dataset: {
          source: vm.data.filter(function (d) {
            return d[2] === vm.startYear;
          }),
        },
        yAxis: {
          type: "category",
          inverse: true,
          max: 15,
          axisLabel: {
            show: true,
            textStyle: {
              fontSize: 14,
            },
            formatter: function (value) {
              return (
                vm.getCountryCodeDetails(value).name +
                "{flag|" +
                vm.getFlag(value) +
                "}"
              );
            },
            rich: {
              flag: {
                fontSize: 25,
                padding: 5,
              },
            },
          },
          animationDuration: 600,
          animationDurationUpdate: 600,
        },
        series: [
          {
            realtimeSort: true,
            seriesLayoutBy: "column",
            type: "bar",
            itemStyle: {
              color: function (param) {
                return (
                  vm.countryColors[param.value[3]] || "hsl(204.1, 58.7%, 59.2%)"
                );
              },
            },
            encode: {
              x: vm.dimension,
              y: 3,
            },
            label: {
              show: true,
              precision: 1,
              position: "right",
              valueAnimation: true,
              fontFamily: "monospace",
            },
          },
        ],
        // Disable init animation.
        animationDuration: 0,
        animationDurationUpdate: vm.updateFrequency,
        animationEasing: "linear",
        animationEasingUpdate: "linear",
        graphic: {
          elements: [
            {
              type: "text",
              right: 160,
              bottom: 60,
              style: {
                text: vm.years[vm.startIndex].split("-")[0],
                font: "bolder 80px monospace",
                fill: "rgba(100, 100, 100, 0.25)",
              },
              z: 100,
            },
          ],
        },
      };
    },
  },
  data() {
    return {
      dynamicOption: null,
      updateFrequency: 2000,
      dimension: 0,
      countryColors: {
        Australia: "#00008b",
        Canada: "#f00",
        China: "#ffde00",
        Cuba: "#002a8f",
        Finland: "#003580",
        France: "#ed2939",
        Germany: "#000",
        Iceland: "#003897",
        India: "#f93",
        Japan: "#bc002d",
        "North Korea": "#024fa2",
        "South Korea": "#000",
        "New Zealand": "#00247d",
        Norway: "#ef2b2d",
        Poland: "#dc143c",
        Russia: "#d52b1e",
        Turkey: "#e30a17",
        "United Kingdom": "#00247d",
        "United States": "#b22234",
      },
      data: null,
      flags: null,
      years: null,
      startIndex: 0,
      stopped: true,
      data_loaded: false,

      paused: false,
      current_year: null,

      queue: [],
    };
  },

  methods: {
    setPauseEvent() {
      this.paused = !this.paused;

      if (this.paused) {
        this.clearQueue();
      } else {
        const p = this.years.indexOf(this.current_year);
        if (p) {
          this.startIndex = p;
        }

        this.startRace("pause");
      }
    },
    getFlag(countryName) {
      const detail = this.iso3map[countryName];
      if (!countryName || !detail) {
        console.log(countryName);
        return "";
      }

      const alpha_2 = detail["alpha-2"];
      return (
        this.flags.find(function (item) {
          return item.code === alpha_2;
        }) || {}
      ).emoji;
    },
    updateYear(year) {
      var source = this.data.filter(function (d) {
        return d[2] === year;
      });
      this.dynamicOption.series[0].data = source;
      this.dynamicOption.graphic.elements[0].style.text = year.split("-")[0];

      this.$refs.myChart.setOption(this.dynamicOption);

      this.current_year = year;
      console.log(this.current_year);

      if (year === this.years[this.years.length - 1]) {
        this.stopped = true;
      }
    },
    startRace(from = "start") {
      if (from === "reset") {
        this.startIndex = 0;
      }
      let vm = this;
      vm.stopped = false;
      vm.paused = false;
      var i = 0;
      vm.clearQueue();
      //   vm.startIndex = vm.years.indexOf(vm.current_year);

      for (i = vm.startIndex; i < vm.years.length - 1; ++i) {
        (function (i) {
          vm.queue.push(
            setTimeout(function () {
              vm.updateYear(vm.years[i + 1]);
            }, (i - vm.startIndex) * vm.updateFrequency)
          );
        })(i);
      }
    },
    getCountryCodeDetails(code) {
      return this.iso3map[code] || {};
    },
    loadInputData() {
      var start_year = "1960-01-01";
      this.data_loaded = false;
      this.years = this.input_data
        .map((record) => record.year)
        .filter((x, i, a) => a.indexOf(x) === i)
        .sort()
        .filter((v) => v >= start_year);
      this.country_codes = this.input_data
        .map((record) => record.key)
        .filter((x, i, a) => a.indexOf(x) === i)
        .sort();

      //   var data = [];
      this.data = [];

      var countryLastValue = {};
      var year = null;
      var sub = null;
      var code = null;
      var now = null;
      var val = null;

      console.log("Start loop");

      for (var i = 0; i < this.years.length; i++) {
        year = this.years[i];
        sub = this.input_data.filter((record) => record.year === year);

        for (var j = 0; j < this.country_codes.length; j++) {
          code = this.country_codes[j];
          now = sub.filter((record) => record.key == code);

          if (now.length == 0) {
            val = countryLastValue[code] || 0;
          } else {
            countryLastValue[code] = now[0].cumulative_value;
            val = countryLastValue[code];
          }

          this.data.push([
            val,
            this.getCountryCodeDetails(code).name,
            year,
            code,
          ]);
          //   console.log(this.data[this.data.length - 1]);
        }
      }

      this.data = this.data.filter((record) => record[1]);
      this.data_loaded = true;

      //   this.data = this.input_data
      //     .map((record) => [
      //       //   record.value,
      //       record.cumulative_value,
      //       record.doc_count,
      //       record.year_doc_count,
      //       this.getCountryCodeDetails(record.key).name,

      //       record.year,
      //       record.key,
      //     ])
      //     .filter((record) => record[3]);

      //   this.keys = []

      //   for (var i = 0; i < this.data.length; ++i) {
      //     if (
      //       this.years.length === 0 ||
      //       this.years[this.years.length - 1] !== this.data[i][4]
      //     ) {
      //       this.years.push(this.data[i][4]);
      //     }
      //     if (
      //       this.years.length === 0 ||
      //       this.years[this.years.length - 1] !== this.data[i][4]
      //     ) {
      //       this.years.push(this.data[i][4]);
      //     }
      //     }
    },
    fetchData() {
      this.$http.get("/static/data/emoji-flags.json").then((response) => {
        this.flags = response.data;
      });
    },
    clearQueue() {
      this.queue.forEach((panel) => clearTimeout(panel));

      this.queue = [];
    },
  },
  destroyed() {
    this.clearQueue();
  },
};
</script>

<style>
.chart {
  height: 550px;
}
</style>