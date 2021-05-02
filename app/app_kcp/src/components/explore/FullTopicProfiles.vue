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

          <h4>Topic profile by document type</h4>

          <b-row>
            <b-col>
              <v-chart
                v-if="major_doc_type_volume"
                class="chart"
                refs="graphChart"
                :option="graphOptions(major_doc_type_volume, 'Document type')"
                :autoresize="true"
                :loading="loading"
              />
            </b-col>
          </b-row>

          <br />
          <br />

          <h4>Topic profile by admin regions</h4>

          <b-row>
            <b-col>
              <v-chart
                v-if="adm_region_volume"
                class="chart"
                refs="graphChart"
                :option="graphOptions(adm_region_volume, 'Admin regions')"
                :autoresize="true"
                :loading="loading"
              />
            </b-col>
          </b-row>
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
      errors: [],
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

      // Doc types specific to WB document. Must be changed when updating the metadata.
      adm_regions: [
        "Africa",
        "East Asia and Pacific",
        "Europe and Central Asia",
        "Latin America & Caribbean",
        "Middle East and North Africa",
        "Rest Of The World",
        "South Asia",
        "The world Region",
      ],
      doc_types: [
        "Board Documents",
        "Country Focus",
        "Economic & Sector Work",
        "Project Documents",
        "Publications & Research",
      ],
      lending_instruments: ["Development Policy Lending"],

      // Plotly data and layout
      plot_data: [
        {
          x: [1, 2, 3, 4],
          y: [10, 15, 13, 17],
          type: "scatter",
        },
      ],
      plot_layout: {
        title: "My graph",
      },
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
    graphOptions(data, label) {
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
          data: data.legend,
        },
        toolbox: {
          feature: {
            saveAsImage: {},
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: [
          {
            type: "category",
            boundaryGap: false,
            data: data.year,
          },
        ],
        yAxis: [
          {
            type: "value",
            axisLabel: {
              formatter: "{value} %",
            },
          },
        ],
        series: data.series,
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
        .catch((error) => {
          console.log(error);
          this.errored = true;
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
          .catch((error) => {
            console.log(error);
            this.errored = true;
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

      let options = {
        corpus_id: this.corpus_id,
        // model_id: "6694f3a38bc16dee91be5ccf4a64b6d8",
        model_id: this.model_run_info_id,
        // model_id: "3e82ec784f125709c8bac46d7dd8a67f",
        topic_id: this.topic_id,
        year_start: 1960,
        type: "bar",
      };

      this.$http
        .post(this.nlp_api_url + "/get_full_topic_profiles", options)
        .then((response) => {
          let data = response.data;

          this.adm_region_volume = data.adm_region.volume;
          this.adm_region_share = data.adm_region.share;

          this.major_doc_type_volume = data.major_doc_type.volume;
          this.major_doc_type_share = data.major_doc_type.share;

          if ("topic_words" in data) {
            this.topic_words = data.topic_words;
          }
          console.log(data);
          this.full_profile_ready = true;
          this.loading = false;
        })
        .catch((error) => {
          console.log(error);
          this.errors.push(error);
          this.errored = true;
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
