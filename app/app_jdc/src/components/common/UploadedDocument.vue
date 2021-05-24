<template>
  <div>
    <!-- <div v-if="loading" class="text-center">
      <b-spinner></b-spinner>
    </div> -->
    <div v-if="privateFilteredDocTopics && !loading">
      <div class="xsl-caption field-caption">LDA topics</div>
      <div class="field-value">
        <div class="row border-bottom">
          <div class="col-md-2 font-weight-bold">Topic</div>
          <div class="col-md-2 font-weight-bold">Score (%)</div>
          <div class="col-md-8 font-weight-bold">Top words</div>
        </div>

        <div
          v-for="dt in privateFilteredDocTopics"
          :key="dt.topic_id"
          class="border-bottom"
        >
          <div class="row">
            <div class="col-md-2 topic-name">Topic {{ dt.topic_id }}</div>
            <div class="col-md-2">
              <div class="progress mt-1">
                <div
                  class="progress-bar"
                  :style="'width: ' + topicPercent(dt.value) + '%'"
                  role="progressbar"
                  :aria-valuenow="topicPercent(dt.value)"
                  aria-valuemin="0"
                  aria-valuemax="100"
                  :title="topicPercent(dt.value) + '%'"
                ></div>
              </div>
              <div class="topic-score">{{ topicPercent(dt.value) }}%</div>
            </div>
            <div class="col-md-8 topic-words">
              <span class="topic-word"> {{ dt.topic_words }} </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <br />
    <br />
    <div v-if="privateCountryData && !loading">
      <div class="xsl-caption field-caption">Extracted countries</div>

      <WBMapChart
        :countryData="privateCountryData"
        highColor="#0000ff"
        lowColor="#efefff"
        countryStrokeColor="#909090"
        defaultCountryFillColor="#fff"
      />
    </div>
    <br />
    <br />

    <div v-if="metadata && !loading">
      <div class="xsl-caption field-caption">Extracted country details</div>
      <div style="word-wrap: break-word">
        <vue-json-pretty :data="metadata" :highlightMouseoverNode="true">
        </vue-json-pretty>
      </div>
    </div>
  </div>
</template>
<script>
import VueJsonPretty from "vue-json-pretty";
import "vue-json-pretty/lib/styles.css";

import WBMapChart from "./MapChartWB";

export default {
  props: {
    result: Object,
  },
  components: { WBMapChart, VueJsonPretty },
  mounted() {
    // window.viewer = this;
    window.document_analyzed = this;
    this.getISOInfo();
  },
  data() {
    return {
      loading: false,
      doc_topics: [],
      iso3map: null,
      privateCountryData: null,
      privateFilteredDocTopics: null,
      metadata: {},
    };
  },
  computed: {},
  methods: {
    updateData() {
      this.loading = true;
      this.privateFilteredDocTopics = null;
      this.metadata = {};
      this.privateCountryData = {};

      this.doc_topics = [];
      this.doc_topics = this.result.doc_topic_words;
      // this.privateCountryData = this.result.country_counts;

      this.metadata["country_counts"] = this.result.country_counts;
      this.metadata["country_groups"] = this.result.country_groups;
      this.metadata["country_details"] = this.result.country_details;

      // Doc topics
      this.privateFilteredDocTopics = this.doc_topics.filter((obj) => {
        return obj.value > 0;
      });

      // Map country data

      for (const [key, value] of Object.entries(this.result.country_counts)) {
        console.log(key, value);

        if (this.iso3map[key] !== undefined) {
          this.privateCountryData[this.iso3map[key]["alpha-2"]] = value;
        }
      }
      this.loading = false;

      // this.filteredDocTopics();
      // this.countryData();
    },
    topicPercent(value) {
      return Math.round(100 * value);
    },
    filteredDocTopics() {
      this.privateFilteredDocTopics = null;
      this.privateFilteredDocTopics = this.doc_topics.filter((obj) => {
        return obj.value > 0;
      });
      return this.privateFilteredDocTopics;
    },
    countryData() {
      this.setCountryData();

      return this.privateCountryData;
    },
    setCountryData() {
      this.privateCountryData = null;

      let privateCountryData = {};
      for (const [key, value] of Object.entries(this.result.country_counts)) {
        console.log(key, value);

        if (this.iso3map[key] !== undefined) {
          privateCountryData[this.iso3map[key]["alpha-2"]] = value;
        }
      }
      this.privateCountryData = privateCountryData;
      return this.privateCountryData;
    },
    getISOInfo() {
      if (this.iso3map === null) {
        this.$http
          .get("/static/data/iso3166-3-country-info.json")
          .then((response) => {
            this.iso3map = response.data;
            this.updateData();
          });
      } else {
        this.updateData();
      }
    },
  },
  watch: {
    result: {
      deep: true,
      handler() {
        this.updateData();
      },
    },
    loading() {
      this.$emit("onLoadingStatusChanged", this.loading);
    },
  },
};
</script>
<style scoped>
.field-caption {
  font-weight: bold;
  margin-bottom: 25px;
  margin-bottom: 10px;
}
.xsl-caption {
  font-family: "Open Sans", sans-serif;
  /* font-weight: bold; */
  /* color: #707070; */
  text-transform: uppercase;
  margin-top: 25px;
}
.topic-name {
  font-size: 0.9rem;
  font-family: "Roboto", "Open Sans", sans-serif;
}
.topic-score {
  font-size: 10px;
}
.topic-word {
  color: #495057;
  font-family: "Roboto", "Open Sans", sans-serif;
  font-size: 0.9rem;
}
.progress {
  /* display: -ms-flexbox; */
  display: flex;
  height: 1rem;
  overflow: hidden;
  font-size: 0.75rem;
  background-color: #e9ecef;
  border-radius: 0rem;
}
.progress-bar {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-direction: column;
  flex-direction: column;
  -ms-flex-pack: center;
  justify-content: center;
  color: #fff;
  text-align: center;
  white-space: nowrap;
  background-color: #007bff;
  transition: width 0.6s ease;
}
.border-bottom {
  border-bottom: 1px solid #dee2e6 !important;
}
.font-weight-bold {
  font-weight: 700 !important;
}
</style>