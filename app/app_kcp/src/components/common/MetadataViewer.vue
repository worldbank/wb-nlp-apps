<template>
  <div>
    <div v-if="metadata.title">
      <div class="xsl-caption field-caption">Title</div>
      <p>{{ metadata.title }}</p>
    </div>

    <div v-if="metadata.date_published">
      <div class="xsl-caption field-caption">Date published</div>
      <p>{{ metadata.date_published }}</p>
    </div>

    <div v-if="metadata.topics_src.concat(metadata.wb_subtopic_src).length > 0">
      <div class="xsl-caption field-caption">Topics</div>
      <ul>
        <li
          v-for="topic_name in metadata.topics_src.concat(
            metadata.wb_subtopic_src
          )"
          :key="topic_name"
        >
          {{ topic_name }}
        </li>
      </ul>
    </div>

    <div v-if="metadata.country.length > 0">
      <div class="xsl-caption field-caption">Tagged country or region</div>
      <ul>
        <li v-for="country in metadata.country" :key="country">
          {{ country }}
        </li>
      </ul>
    </div>

    <div v-if="metadata.doc_type.length > 0">
      <div class="xsl-caption field-caption">Document type</div>
      <ul>
        <li v-for="doc_type in metadata.doc_type" :key="doc_type">
          {{ doc_type }}
        </li>
      </ul>
    </div>

    <div v-if="privateCountryData">
      <div class="xsl-caption field-caption">Country popularity</div>
      <p>
        The number of times a country is mentioned in the document is shown in
        the map below. This metric may indicate that the document is relevant
        for countries that highly cited.
      </p>
      <WBMapChart
        :countryData="privateCountryData"
        highColor="#0000ff"
        lowColor="#eeeeff"
        countryStrokeColor="#909090"
        defaultCountryFillColor="#fefefe"
      />
    </div>

    <div v-if="privateFilteredDocTopics">
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

    <div v-if="show_raw_metadata">
      <div class="xsl-caption field-caption">Full metadata</div>
      <div v-if="metadata" style="word-wrap: break-word">
        <vue-json-pretty :data="metadata" :highlightMouseoverNode="true">
        </vue-json-pretty>
      </div>
    </div>
  </div>
</template>
<script>
// import MapChart from "@avsolatorio/vue-map-chart";
import VueJsonPretty from "vue-json-pretty";
import "vue-json-pretty/lib/styles.css";

import WBMapChart from "./MapChartWB";

export default {
  props: {
    metadata: Object,
    show_raw_metadata: Boolean,
  },
  components: { WBMapChart, VueJsonPretty },
  mounted() {
    window.viewer = this;
    this.privateFilteredDocTopics = null;
    this.privateCountryData = null;
    this.doc_topics = [];

    this.getISOInfo();
    this.getDocumentTopics();
  },
  data() {
    return {
      iso3map: null,
      privateCountryData: null,
      privateFilteredDocTopics: null,
      doc_topics: [],
    };
  },
  computed: {
    topicsParams() {
      var search_params = new URLSearchParams();
      search_params.append("model_id", "6694f3a38bc16dee91be5ccf4a64b6d8");
      search_params.append("doc_id", this.metadata.id);
      search_params.append("sort", true);

      return search_params;
    },
  },
  methods: {
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
      this.privateCountryData = null;
      if (this.iso3map === null) {
        this.getISOInfo();
      } else {
        this.setCountryData();
      }

      return this.privateCountryData;
    },
    setCountryData() {
      this.privateCountryData = {};
      for (const [key, value] of Object.entries(this.metadata.der_countries)) {
        console.log(key, value);

        if (this.iso3map[key] !== undefined) {
          this.privateCountryData[this.iso3map[key]["alpha-2"]] = value;
        }
      }
    },
    getISOInfo() {
      this.$http
        .get("/static/data/iso3166-3-country-info.json")
        .then((response) => {
          this.iso3map = response.data;

          if (this.privateCountryData === null) {
            this.setCountryData();
          }
        });
    },
    getDocumentTopics() {
      this.$http
        .get("/nlp/models/lda/get_topics_by_doc_id", {
          params: this.topicsParams,
        })
        .then((response) => {
          this.doc_topics = response.data;
          this.filteredDocTopics();
        });
    },
  },
  watch: {
    metadata: function () {
      this.countryData();
      this.getDocumentTopics();
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