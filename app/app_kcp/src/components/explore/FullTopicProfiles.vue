<template>
  <div>
    <h3>{{ page_title }}</h3>
    <br />

    <p>
      Topics are not covered evenly over time, across regions, by document type,
      and by organization represented in our corpus. Select a corpus, a topic
      and a (LDA) model, and two or more partitions to compare the evolution of
      the topic coverage over time. The resulting chart can be embedded, its
      code downloaded, and the underlying data are available in our document
      meta-database.
    </p>

    <hr />

    <b-container fluid>
      <h5>Select model</h5>
      <MLModelSelect
        @modelSelected="onModelSelect"
        :model_name="model_name"
        placeholder="Select model"
      />

      <br />

      <b-row v-show="model_run_info_id !== null">
        <b-col :md="show_topic_words ? 9 : 12">
          <b-row
            v-if="
              lda_model_id != '' &&
              topic_share_active &&
              current_lda_model_topics_options
            "
          >
            <b-col>
              <b-form-group>
                <div class="model-select-wrapper">
                  <model-select
                    :options="current_lda_model_topics_options"
                    v-model="topic_id"
                    placeholder="Select topic"
                    class="wbg-model-select"
                  >
                  </model-select>
                </div>
              </b-form-group>
            </b-col>
          </b-row>
          <br />

          <div v-if="major_doc_type_data">
            <h4>Topic profile by document type</h4>
            <b-form-radio-group
              v-model="major_doc_type_value"
              value-field="item"
              text-field="name"
              :options="[
                { item: 'volume', name: 'By volume' },
                { item: 'share', name: 'By share' },
              ]"
            />
            <br />

            <b-row>
              <b-col>
                <v-chart
                  class="chart"
                  refs="graphChart"
                  :option="
                    graphOptions(
                      major_doc_type_data,
                      major_doc_type_value,
                      'Document type'
                    )
                  "
                  :autoresize="true"
                  :loading="loading"
                />
              </b-col>
            </b-row>

            <br />
            <br />
          </div>

          <div v-if="adm_region_data">
            <h4>Topic profile by admin regions</h4>
            <b-form-radio-group
              v-model="adm_region_value"
              value-field="item"
              text-field="name"
              :options="[
                { item: 'volume', name: 'By volume' },
                { item: 'share', name: 'By share' },
              ]"
            />
            <br />

            <b-row>
              <b-col>
                <v-chart
                  v-if="adm_region_data"
                  class="chart"
                  refs="graphChart"
                  :option="
                    graphOptions(
                      adm_region_data,
                      adm_region_value,
                      'Admin regions'
                    )
                  "
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
// import "echarts";

import { use } from "echarts/core";
import VChart from "vue-echarts";
// import { Plotly } from "vue-plotly";
import $ from "jquery";
import MLModelSelect from "../common/MLModelSelect";
import { ModelSelect } from "vue-search-select";

// import * as echarts from 'echarts/core';
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
  name: "TopicProfiles",
  components: {
    // Plotly,
    MLModelSelect,
    ModelSelect,
    VChart,
  },
  props: {
    page_title: String,
    show_topic_words: Boolean,
  },
  data: function () {
    return {
      api_url: "/api",
      nlp_api_url: null,
      model_topics: [],
      related_words: [],
      current_lda_model_topics: [],
      current_lda_model_topics_options: [],
      raw_text: "poverty",
      loading: true,
      model_name: "lda",
      model_run_info_id: null,

      corpus_id: "WB",
      lda_model_id: "ALL_50",

      topic_share_active: true,
      full_profile_ready: false,
      major_doc_type_value: "volume",
      adm_region_value: "volume",
      adm_region_data: null,
      major_doc_type_data: null,

      prev_topic_id: -1,
      topic_id: null,
      selected_topic: 0,
      topic_share_selected_adm_regions: [],
      topic_share_selected_doc_types: [],
      topic_share_selected_lending_instruments: [],
      topic_share_plot_ready: false,
      topic_share_searching: false,

      topic_shares: null,
      topic_words: null,
    };
  },
  computed: {
    // topic_id() {
    //   return this.selected_topic.topic_id;
    // },

    searchParams() {
      const params = new URLSearchParams();
      params.append("model_id", this.model_run_info_id);
      params.append("topn_words", 10);
      return params;
    },
    readyForSubmit: function () {
      return (
        this.topic_share_selected_adm_regions.length +
          this.topic_share_selected_doc_types.length +
          this.topic_share_selected_lending_instruments.length >
        0
      );
    },
    topicChanged: function () {
      // return this.prev_topic_id != this.selected_topic.topic_id;
      return this.prev_topic_id != this.topic_id;
    },
    blurContent: function () {
      return this.topicChanged || !this.topic_share_plot_ready;
    },
  },
  mounted() {
    window.vm = this;
    this.setModel();
    this.getFullTopicProfiles();
  },
  methods: {
    onModelSelect: function (result) {
      this.model_run_info_id = result.model_run_info_id;
      this.nlp_api_url = result.url;
      this.getModelTopics();
    },
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
      return {
        title: {
          text: "Topic profiles" + "(" + label + ")",
        },
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
            dataZoom: {
              yAxisIndex: "none",
            },
            restore: {},
            saveAsImage: {},
          },
        },

        grid: {
          left: "3%",
          right: "4%",
          bottom: "15%",
          top: "10%",
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
    getModelTopics: function () {
      this.topic_id = null;
      this.$http
        .get(this.nlp_api_url + "/get_model_topic_words", {
          params: this.searchParams,
        })
        .then((response) => {
          // this.model_topics = response.data;
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
        })
        .finally(() => (this.loading = false));
    },
    setModel: function (_model_id, model_name) {
      _model_id = "ALL_50";
      model_name = "lda";
      let vm = this;
      if (model_name == "word2vec") {
        vm.word2vec_model_id = _model_id;
      } else if (model_name == "lda") {
        // Assume that
        vm.lda_model_id = _model_id;

        // let options = {
        //   corpus_id: this.corpus_id,
        //   model_id: this.lda_model_id,
        //   topn_words: 10,
        // };

        let options = {
          // model_id: "6694f3a38bc16dee91be5ccf4a64b6d8",
          model_id: this.model_run_info_id,
          topn_words: 10,
        };

        this.$http
          // .get(this.api_url + "/get_lda_model_topics" + "?" + $.param(options))
          .get(
            this.nlp_api_url + "/get_model_topic_words" + "?" + $.param(options)
          )
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
          })
          .finally(() => (this.loading = false));
      } else {
        return;
      }
    },
    getFullTopicProfiles: function () {
      this.loading = true;
      this.full_profile_ready = false;
      this.prev_topic_id = this.topic_id;
      this.topic_share_searching = true;
      this.topic_share_plot_ready = false;

      const params = new URLSearchParams();
      params.append("model_id", this.model_run_info_id);
      params.append("topic_id", this.topic_id);
      params.append("year_start", 1960);
      params.append("type", "line");

      // let options = {
      //   // corpus_id: this.corpus_id,
      //   // model_id: "6694f3a38bc16dee91be5ccf4a64b6d8",
      //   model_id: this.model_run_info_id,
      //   // model_id: "3e82ec784f125709c8bac46d7dd8a67f",
      //   topic_id: this.topic_id,
      //   year_start: 1960,
      //   type: "line",
      // };

      this.$http
        .get(this.nlp_api_url + "/get_full_topic_profiles", { params: params })
        .then((response) => {
          let data = response.data;

          this.adm_region_data = data.adm_region;
          this.major_doc_type_data = data.major_doc_type;

          if ("topic_words" in data) {
            this.topic_words = data.topic_words;
          }
          this.full_profile_ready = true;
          this.loading = false;
        })

        .finally(() => {
          this.topic_share_searching = false;
          this.plotStack(this.topic_shares);
        });
    },
    plotVolumeTopicProfiles() {},
  },
  watch: {
    topic_id() {
      this.getFullTopicProfiles();
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
  height: 450px;
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
