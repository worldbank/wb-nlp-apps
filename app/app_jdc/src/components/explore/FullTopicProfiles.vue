<template>
  <div>
    <header>
      <h1 class="blog-post-title mb-3" dir="auto">
        {{ page_title }}
      </h1>
    </header>
    <div>
      <p class="mt-3 text-justify">
        Topics are not covered evenly over time, across regions, by document
        type, and by organization represented in our corpus. Select a corpus, a
        topic and a (LDA) model, and two or more partitions to compare the
        evolution of the topic coverage over time.
      </p>
    </div>

    <hr />

    <b-container fluid>
      <!-- <h5>Select model</h5>
      <MLModelSelect
        @modelSelected="onModelSelect"
        :model_name="model_name"
        placeholder="Select model"
      />

      <br /> -->

      <h5>Select topic</h5>

      <b-row v-show="model_run_info_id !== null">
        <b-col :md="show_topic_words ? 9 : 12">
          <b-row v-if="current_lda_model_topics_options.length > 0">
            <b-col>
              <b-form-group>
                <div class="model-select-wrapper">
                  <ModelSelect
                    :options="current_lda_model_topics_options"
                    v-model="topic_id"
                    placeholder="Select topic"
                    class="wbg-model-select"
                  >
                  </ModelSelect>
                </div>
              </b-form-group>
            </b-col>
          </b-row>
          <br />

          <div>
            <h4>Topic profile by document type</h4>
            <b-form-radio-group
              v-model="major_doc_type_value"
              value-field="item"
              text-field="name"
              :options="group_value_options"
            />
            <br />

            <b-row>
              <b-col>
                <v-chart
                  class="chart"
                  ref="graphChartMajorDocType"
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
            <h4>Topic profile by source</h4>
            <b-form-radio-group
              v-model="corpus_value"
              value-field="item"
              text-field="name"
              :options="group_value_options"
            />
            <br />

            <b-row>
              <b-col>
                <v-chart
                  class="chart"
                  ref="graphChartCorpusRegion"
                  :option="defaultOptions"
                  :autoresize="true"
                  :loading="loading"
                />
              </b-col>
            </b-row>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { use } from "echarts/core";
import VChart from "vue-echarts";

// import MLModelSelect from "../common/MLModelSelect";
import { ModelSelect } from "vue-search-select";

import {
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  DataZoomInsideComponent,
  DataZoomSliderComponent,
  ToolboxComponent,
  // TitleComponent,
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
  // TitleComponent,
]);

export default {
  name: "TopicProfiles",
  components: {
    // MLModelSelect,
    ModelSelect,
    VChart,
  },
  props: {
    page_title: String,
    show_topic_words: Boolean,
  },
  data: function () {
    return {
      nlp_api_url: this.$config.jdc_models.topic_model_api_url,
      current_lda_model_topics: [],
      current_lda_model_topics_options: [],
      loading: true,

      model_name: this.$config.jdc_models.topic_model.model_name,
      model_run_info_id: this.$config.jdc_models.topic_model.model_id,

      full_profile_ready: false,

      major_doc_type_value: "volume",
      corpus_value: "volume",

      group_value_options: [
        { item: "volume", name: "By volume" },
        { item: "share", name: "By share" },
      ],

      corpus_data: null,
      major_doc_type_data: null,

      prev_topic_id: -1,
      topic_id: this.$config.jdc_models.default_topic_id,

      topic_words: null,
    };
  },
  computed: {
    searchParams() {
      const params = new URLSearchParams();
      params.append("model_id", this.model_run_info_id);
      params.append("topn_words", 10);
      return params;
    },

    topicChanged: function () {
      return this.prev_topic_id != this.topic_id;
    },
    defaultOptions() {
      return {
        // title: {
        //   text: "Topic profiles",
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
          bottom: "15%",
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
    },
  },
  mounted() {
    window.vm = this;
    this.getModelTopics();
  },
  methods: {
    formatTopicText: function (topic) {
      return (
        "Topic " +
        topic.topic_id +
        ": " +
        topic.topic_words
          .slice(0, 8)
          .map(function (x) {
            return x.word;
          })
          .join(", ")
      );
    },
    graphOptions(data, value, label) {
      console.log(label);
      return {
        // title: {
        //   text: "Topic profiles" + " (" + label + ")",
        //   subtext: "Default layout",
        //   top: "bottom",
        //   left: "right",
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
          data: data[value].legend,
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
          bottom: "15%",
          containLabel: true,
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
        dataZoom: [
          {
            type: "inside",
            start: 50,
            end: 100,
          },
          {
            start: 50,
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
        series: data[value].series,
      };
    },
    updateOption(data, value, label) {
      console.log(label);
      return {
        // title: {
        //   text: "Topic profiles" + " (" + label + ")",
        //   subtext: "Default layout",
        //   top: "bottom",
        //   left: "right",
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
    getModelTopics: function () {
      // this.topic_id = 0;
      this.$http
        .get(this.nlp_api_url + "/get_model_topic_words", {
          params: this.searchParams,
        })
        .then((response) => {
          this.current_lda_model_topics = response.data;
          this.current_lda_model_topics_options = this.lodash.map(
            this.current_lda_model_topics,
            (topic) => {
              return {
                text: this.formatTopicText(topic),
                value: topic.topic_id,
              };
            }
          );
          this.topic_words = this.current_lda_model_topics[this.topic_id];

          this.getFullTopicProfiles();
        })
        .finally(() => (this.loading = false));
    },
    getFullTopicProfiles: function () {
      this.loading = true;
      this.full_profile_ready = false;
      this.prev_topic_id = this.topic_id;

      const params = new URLSearchParams();
      params.append("model_id", this.model_run_info_id);
      params.append("topic_id", this.topic_id);
      params.append("year_start", 1960);
      params.append("app_tag_jdc", true);
      params.append("type", "line");

      this.$http
        .get(this.nlp_api_url + "/get_full_topic_profiles", { params: params })
        .then((response) => {
          let data = response.data;

          this.corpus_data = data.corpus;
          this.major_doc_type_data = data.major_doc_type;

          if ("topic_words" in data) {
            this.topic_words = data.topic_words;
          }
          this.updateCharts();

          this.full_profile_ready = true;
          this.loading = false;
        })

        .finally(() => {});
    },
    plotVolumeTopicProfiles() {},
    updateCharts() {
      this.$refs.graphChartMajorDocType.setOption(
        this.updateOption(
          this.major_doc_type_data,
          this.major_doc_type_value,
          "Document type"
        )
      );

      this.$refs.graphChartCorpusRegion.setOption(
        this.updateOption(this.corpus_data, this.corpus_value, "Source")
      );
    },
  },
  watch: {
    topic_id() {
      this.getFullTopicProfiles();
    },
    corpus_value() {
      this.$refs.graphChartCorpusRegion.setOption(
        this.updateOption(this.corpus_data, this.corpus_value, "Source")
      );
    },
    major_doc_type_value() {
      this.$refs.graphChartMajorDocType.setOption(
        this.updateOption(
          this.major_doc_type_data,
          this.major_doc_type_value,
          "Document type"
        )
      );
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#topic-selected {
  width: 42vw;
  text-overflow: ellipsis;
  overflow: hidden;
  display: block;
  white-space: nowrap;
}
/* #topic-selected > div {
  position: absolute;
} */

/* .vs--single .vs__selected {
  text-overflow: ellipsis;
  color: #394066;
} */
.blur {
  filter: blur(1px);
  opacity: 0.4;
}

.checkbox /deep/ .b-dropdown-form {
  max-height: 400px;
  font-size: 75%;
  overflow-y: auto;
}

.chart {
  height: 400px;
}

.model-select-wrapper {
  margin: 5px;
}
.wbg-model-select {
  border-color: var(--action-color) !important;
  color: var(--action-color) !important;
  border-radius: var(--border-radius-sm) !important;
  /* padding: 0.375rem 0.75rem !important; */
  font-weight: 400 !important;
  font-size: 1rem !important;
}

/* .wbg-model-select .text.default { */
div.default.text {
  color: var(--action-color-hover) !important;
}
</style>
