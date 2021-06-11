<template>
  <div>
    <vue-horizontal v-if="!errored && !results">
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
    <div v-if="errored || (results && results.length === 0)">
      No related documents found
    </div>
    <vue-horizontal v-if="results && results.length > 0">
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
                'px; overflow-y:auto; margin-top:5px;'
              "
            >
              <span class="title">
                <router-link
                  :to="{
                    name: 'document',
                    params: {
                      doc_id: result.metadata.id,
                      metadata: result.metadata,
                    },
                  }"
                >
                  <div class="truncated-title">
                    {{ result.metadata.title }}
                  </div></router-link
                >

                <!--
                <a
                  :href="result.metadata.url_pdf"
                  :title="result.metadata.title"
                  target="_blank"
                >
                  <div class="truncated-title">
                    {{ result.metadata.title }}
                  </div>
                </a> -->
              </span>
              <div class="study-country">
                <span v-if="result.metadata.country"
                  >{{ result.metadata.country[0] }}, </span
                ><span v-if="result.metadata.year">{{
                  result.metadata.year
                }}</span>
              </div>
              <div class="survey-stats">
                <span v-if="result.metadata.date_published"
                  >Created on:
                  {{ getDate(result.metadata.date_published) }} </span
                ><br />
                <span v-if="result.metadata.views"
                  >Views: {{ result.metadata.views }}</span
                >
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
    reference_id: { type: String, default: "" },
    submit: Boolean,
    model_name: String,
    section_height: Number,
    first_entry: Boolean,
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
        duplicate_threshold: 0.999,
        metric_type: "IP",
      };
    },
    model_id() {
      if (this.model_name === "word2vec") {
        return this.$config.default_model.embedding_model.model_id;
      } else {
        // Default to lda model if model_name is not specified
        return this.$config.default_model.topic_model.model_id;
      }
    },
    similar_docs_by_id_url() {
      if (this.model_name === "word2vec") {
        return (
          this.$config.nlp_api_url[
            this.$config.default_model.embedding_model.model_name
          ] + "/get_similar_docs_by_doc_id"
        );
      } else {
        // Default to lda model if model_name is not specified
        return (
          this.$config.nlp_api_url[
            this.$config.default_model.topic_model.model_name
          ] + "/get_similar_docs_by_doc_id"
        );
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
      results: null,
      loading: false,
      errored: false,
      id_changed: false,
      first_load: true,
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
      this.results = null;
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
      if (this.submit && (this.first_load || this.id_changed)) {
        this.sendSemanticSearch();
        this.id_changed = false;
        this.first_load = false;
      }
    },
    reference_id: function () {
      this.id_changed = true;
      // this.sendSemanticSearch();
    },
    first_entry() {
      if (this.first_entry) {
        this.sendSemanticSearch();
      }
    },
    errored: function () {
      this.$emit("errorStatus", this.errored);
    },
    results: function () {
      if (this.results) {
        if (this.results.length === 0) {
          this.$emit("errorStatus", true);
        } else if (this.first_entry && this.results.length > 0) {
          this.$emit("firstEntryReady", true);
        }
      }
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
