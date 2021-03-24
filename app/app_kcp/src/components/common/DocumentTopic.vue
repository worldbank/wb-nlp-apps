<template>
  <div>
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
  </div>
</template>
<script>
export default {
  props: {
    doc_id: String,
  },
  components: {},
  mounted() {
    // window.viewer = this;
    this.privateFilteredDocTopics = null;
    this.doc_topics = [];

    if (this.doc_id) {
      this.private_doc_id = this.doc_id;
    }

    console.log(this.doc_id);

    // this.getDocumentTopics();
  },
  data() {
    return {
      doc_topics: [],
      private_doc_id: null,
      privateFilteredDocTopics: null,
    };
  },
  computed: {
    topicsParams() {
      var search_params = new URLSearchParams();
      search_params.append("model_id", "6694f3a38bc16dee91be5ccf4a64b6d8");
      search_params.append("doc_id", this.private_doc_id);
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
    private_doc_id: function () {
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