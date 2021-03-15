<template>
  <div>
    <vue-horizontal v-show="results.length === 0">
      <div
        class="related-section"
        :style="'height: ' + panel_section_height + 'px;'"
        v-for="i in Array(5).keys()"
        :key="'rel_sk_' + i"
      >
        <div style="padding-top: 5px">
          <b-skeleton-img
            :height="panel_section_height - 15 + 'px'"
          ></b-skeleton-img>
        </div>
      </div>
    </vue-horizontal>
    <vue-horizontal v-show="results.length > 0">
      <div
        class="related-section"
        :style="'height: ' + panel_section_height + 'px;'"
        v-for="result in results"
        :key="'rel_' + result.rank"
      >
        <div
          class="related-document-row"
          data-url="#"
          title="View related study"
        >
          <div class="row">
            <div
              class="col-12"
              :style="
                'max-height: ' +
                (panel_section_height - 10) +
                'px; overflow-y:auto;'
              "
            >
              <span class="title">
                <a
                  :href="result.metadata.url_pdf"
                  :title="result.metadata.title"
                  target="_blank"
                >
                  <div class="truncated-title">
                    {{ result.metadata.title }}
                  </div>
                </a>
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
    model_name: String,
    section_height: Number,
  },
  mounted() {},
  computed: {
    similarityBody() {
      return {
        model_id: this.model_id,
        doc_id: this.reference_id,
        topn_docs: 10,
        metric: "cosine_similarity",
        show_duplicates: false,
        duplicate_threshold: 0.98,
        metric_type: "IP",
      };
    },
    model_id() {
      if (this.model_name === "word2vec") {
        return "777a9cf47411f6c4932e8941f177f90a";
      } else {
        // Default to lda model if model_name is not specified
        return "6694f3a38bc16dee91be5ccf4a64b6d8";
      }
    },
    similar_docs_by_id_url() {
      if (this.model_name === "word2vec") {
        return "/nlp/models/word2vec/get_similar_docs_by_doc_id";
      } else {
        // Default to lda model if model_name is not specified
        return "/nlp/models/lda/get_similar_docs_by_doc_id";
      }
    },
    panel_section_height() {
      if (this.section_height !== undefined) {
        return this.section_height;
      } else {
        return 100;
      }
    },
  },
  data() {
    return {
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
      const body = this.similarityBody;
      console.log(this.similar_docs_by_id_url);

      this.$http
        .post(this.similar_docs_by_id_url + "?return_metadata=true", body)
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

/* .scrollable {
  overflow-y: auto;
  max-height: 90px;
} */

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
.truncated-title {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3; /* number of lines to show */
  -webkit-box-orient: vertical;
}
</style>
