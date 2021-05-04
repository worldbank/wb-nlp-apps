<template>
  <div v-if="flags && data">
    <b-button
      @click="startRace()"
      :variant="stopped ? 'primary' : 'outline-secondary'"
      :disabled="!stopped"
      >Reset</b-button
    >
    <v-chart class="chart" :option="option" ref="myChart" :autoresize="true" />
  </div>
</template>


<script>
import $ from "jquery";

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
    // this.plotRace();
  },
  watch: {
    isReady() {
      if (this.isReady) {
        this.dynamicOption = this.option;
        this.startRace();
      }
    },
  },
  computed: {
    isReady() {
      return this.data && this.flags;
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
          source: vm.data.slice(1).filter(function (d) {
            return d[4] === vm.startYear;
          }),
        },
        yAxis: {
          type: "category",
          inverse: true,
          max: 10,
          axisLabel: {
            show: true,
            textStyle: {
              fontSize: 14,
            },
            formatter: function (value) {
              return value + "{flag|" + vm.getFlag(value) + "}";
            },
            rich: {
              flag: {
                fontSize: 25,
                padding: 5,
              },
            },
          },
          animationDuration: 300,
          animationDurationUpdate: 300,
        },
        series: [
          {
            realtimeSort: true,
            seriesLayoutBy: "column",
            type: "bar",
            itemStyle: {
              color: function (param) {
                return vm.countryColors[param.value[3]] || "#5470c6";
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
                text: vm.years[vm.startIndex],
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
      updateFrequency: 1000,
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
      startIndex: 70,
      stopped: true,
    };
  },

  methods: {
    getFlag(countryName) {
      if (!countryName) {
        return "";
      }
      return (
        this.flags.find(function (item) {
          return item.name === countryName;
        }) || {}
      ).emoji;
    },
    updateYear(year) {
      var source = this.data.slice(1).filter(function (d) {
        return d[4] === year;
      });
      this.dynamicOption.series[0].data = source;
      this.dynamicOption.graphic.elements[0].style.text = year;
      this.$refs.myChart.setOption(this.dynamicOption);

      if (year === this.years[this.years.length - 1]) {
        this.stopped = true;
      }
    },
    startRace() {
      let vm = this;
      vm.stopped = false;
      var i = 0;

      for (i = vm.startIndex; i < vm.years.length - 1; ++i) {
        (function (i) {
          setTimeout(function () {
            vm.updateYear(vm.years[i + 1]);
          }, (i - vm.startIndex) * vm.updateFrequency);
        })(i);
      }
    },
    fetchData() {
      this.$http
        .get("https://cdn.jsdelivr.net/npm/emoji-flags@1.3.0/data.json")
        .then((response) => {
          this.flags = response.data;
        });

      this.$http
        .get("/static/data/life-expectancy-table.json")
        .then((response) => {
          this.years = [];
          this.data = response.data;

          for (var i = 0; i < this.data.length; ++i) {
            if (
              this.years.length === 0 ||
              this.years[this.years.length - 1] !== this.data[i][4]
            ) {
              this.years.push(this.data[i][4]);
            }
          }
        });
    },
    plotRace() {
      var updateFrequency = 1000;
      var dimension = 0;

      var countryColors = {
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
      };

      $.when(
        $.getJSON("https://cdn.jsdelivr.net/npm/emoji-flags@1.3.0/data.json"),
        $.getJSON("/static/data/life-expectancy-table.json")
      ).done(function (res0, res1) {
        var flags = res0[0];
        var data = res1[0];
        var years = [];
        var i = 0;
        for (i = 0; i < data.length; ++i) {
          if (years.length === 0 || years[years.length - 1] !== data[i][4]) {
            years.push(data[i][4]);
          }
        }

        function getFlag(countryName) {
          if (!countryName) {
            return "";
          }
          return (
            flags.find(function (item) {
              return item.name === countryName;
            }) || {}
          ).emoji;
        }
        var startIndex = 10;
        var startYear = years[startIndex];

        var option = {
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
            source: data.slice(1).filter(function (d) {
              return d[4] === startYear;
            }),
          },
          yAxis: {
            type: "category",
            inverse: true,
            max: 10,
            axisLabel: {
              show: true,
              textStyle: {
                fontSize: 14,
              },
              formatter: function (value) {
                return value + "{flag|" + getFlag(value) + "}";
              },
              rich: {
                flag: {
                  fontSize: 25,
                  padding: 5,
                },
              },
            },
            animationDuration: 300,
            animationDurationUpdate: 300,
          },
          series: [
            {
              realtimeSort: true,
              seriesLayoutBy: "column",
              type: "bar",
              itemStyle: {
                color: function (param) {
                  return countryColors[param.value[3]] || "#5470c6";
                },
              },
              encode: {
                x: dimension,
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
          animationDurationUpdate: updateFrequency,
          animationEasing: "linear",
          animationEasingUpdate: "linear",
          graphic: {
            elements: [
              {
                type: "text",
                right: 160,
                bottom: 60,
                style: {
                  text: startYear,
                  font: "bolder 80px monospace",
                  fill: "rgba(100, 100, 100, 0.25)",
                },
                z: 100,
              },
            ],
          },
        };

        // console.log(option);
        this.$refs.myChart.setOption(option);

        for (i = startIndex; i < years.length - 1; ++i) {
          (function (i) {
            setTimeout(function () {
              updateYear(years[i + 1]);
            }, (i - startIndex) * updateFrequency);
          })(i);
        }

        function updateYear(year) {
          var source = data.slice(1).filter(function (d) {
            return d[4] === year;
          });
          option.series[0].data = source;
          option.graphic.elements[0].style.text = year;
          this.$refs.myChart.setOption(option);
        }
      });
    },
  },
};
</script>

<style>
.chart {
  height: 420px;
}
</style>