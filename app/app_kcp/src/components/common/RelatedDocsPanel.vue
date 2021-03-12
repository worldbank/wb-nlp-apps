<template>
  <div>
    <vue-horizontal v-show="results.length === 0">
      <div
        class="related-section"
        v-for="i in Array(5).keys()"
        :key="'rel_sk_' + i"
      >
        <div style="padding-top: 5px">
          <b-skeleton-img height="85px"></b-skeleton-img>
        </div>
      </div>
    </vue-horizontal>
    <vue-horizontal v-show="results.length > 0">
      <div
        class="related-section"
        v-for="result in results"
        :key="'rel_' + result.rank"
      >
        <div
          class="related-document-row"
          data-url="#"
          title="View related study"
        >
          <div class="row">
            <div class="col-12 scrollable">
              <span class="title">
                <a
                  :href="result.metadata.url_pdf"
                  :title="result.metadata.title"
                  >{{ result.metadata.title }}</a
                >
              </span>
              <div class="study-country">
                {{ result.metadata.country[0] }}, {{ result.metadata.year }}
              </div>
              <div class="survey-stats">
                <span
                  >Created on:
                  {{ getDate(result.metadata.date_published) }} </span
                ><br />
                <span>Views: {{ result.metadata.views }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </vue-horizontal>
  </div>
</template>

<script>
import VueHorizontal from "vue-horizontal";

export default {
  components: { VueHorizontal },
  props: {
    reference_id: String,
    submit: Boolean,
  },
  computed: {
    similarityBody() {
      return {
        model_id: "6694f3a38bc16dee91be5ccf4a64b6d8",
        doc_id: this.reference_id,
        topn_docs: 10,
        metric: "cosine_similarity",
        show_duplicates: false,
        duplicate_threshold: 0.98,
        metric_type: "IP",
      };
    },
  },
  data() {
    return {
      similar_docs_by_id_url: "/nlp/models/lda/get_similar_docs_by_doc_id",
      results: [],
      loading: false,
      errored: false,
    };
  },
  methods: {
    getDate: function (date) {
      date = new Date(date).toDateString();
      date = date.split(" ");

      return date[1] + " " + date[2] + ", " + date[3];
    },
    sendSemanticSearch: function () {
      this.loading = true;

      this.$http
        .post(
          this.similar_docs_by_id_url + "?return_metadata=true",
          this.similarityBody
        )
        .then((response) => {
          this.results = response.data;
          console.log(this.results);
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
          this.loading = false;
        })
        .finally(() => (this.loading = false));
    },
  },
  watch: {
    submit: function () {
      this.sendSemanticSearch();
    },
  },
};
</script>

<style scoped>
/* <!-- Peeking Style --> */
/* .horizontal >>> .v-hl-container {
  scroll-padding-left: 16px;
  scroll-padding-right: 16px;
} */

.scrollable {
  overflow-y: auto;
  max-height: 90px;
}

.related-document-row {
  margin-top: 0;
}

.related-document-row .title {
  font-size: 0.85rem;
}

.related-document-row .survey-stats {
  font-size: 0.65rem;
  opacity: 0.7;
  margin: 8px auto;
}

.related-document-row .study-country {
  font-size: 0.75rem;
}

.vue-horizontal {
  border: 3px solid #dbdbdb;
  padding: 5px;
}
.related-section {
  width: 40vh;
  padding: 0px 20px;
  margin: 3px;
  height: 100px;
  background: #ffffff;
  /* background: #f3f3f3; */
  border: 2px solid #ebebeb;
  border-radius: 4px;
}
</style>

