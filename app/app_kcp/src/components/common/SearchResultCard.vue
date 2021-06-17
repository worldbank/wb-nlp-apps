<template>
  <div>
    <div class="document-row" data-url="#">
      <SearchResultLoading v-if="loading" :loading="loading" :size="1" />
      <div class="row" v-show="!loading">
        <div class="col-3 col-lg-3">
          <img
            :src="document_cover"
            onerror="if (this.src != '/static/files/doc_thumb.png') this.src = '/static/files/doc_thumb.png';"
            title="document thumbnail"
            alt="document thumbnail"
          />
        </div>
        <div class="col-9 col-lg-9">
          <!-- <span class="badge badge-primary wbg-badge">DOCUMENT</span> -->
          <h5 class="title">
            <router-link
              :to="{
                name: 'document',
                params: { doc_id: result.id, metadata: result },
              }"
            >
              <!-- <router-link
              :to="{
                path: '/document/' + result.id,
                params: { doc_id: result.id, metadata: result },
              }"
            > -->
              <!-- <router-link :to="document_link" :title="normalizeTitle(result.title)"> -->
              {{ normalizeTitle(result.title) }}</router-link
            >
          </h5>

          <!-- <Authors /> -->
          <Authors :authors="result.author" authors_class="authors-small" />

          <div v-if="highlights" class="highlight">
            <read-more
              v-if="highlights.body"
              more-str="read more"
              :text="highlights.body.join('... ').replace(/\s\s+/g, ' ') || ''"
              link="#"
              less-str="read less"
              :max-chars="200"
            ></read-more>
          </div>

          <div v-if="result.country" class="study-country">
            {{ result.country[0] }}, {{ result.year }}
          </div>

          <div class="study-id d-md-flex mt-2">
            <!-- <span class="badge badge-pill badge-secondary"
              >ID: {{ result.id }}</span
            >
            <div class="small ml-md-3 mt-2 mt-md-0"> -->

            <div class="small mt-2 mt-md-0">
              Source: {{ result.corpus
              }}<span v-if="match && match.rank">, Rank: {{ match.rank }}</span>
              <!-- <span v-if="match && match.score"
                >, Score: {{ truncate(match.score, 4) }}</span
              > -->
              <span v-if="match && match.topic"
                ><span
                  v-for="topic_id_score in Object.entries(match.topic)"
                  :key="topic_id_score"
                  >, {{ topic_id_score[0].replace("_", " ") }}:
                  {{ truncate(topic_id_score[1], 4) }}%</span
                ></span
              >
            </div>
          </div>

          <div class="study-meta d-flex">
            <div
              class="small mt-2 mb-2 mr-3"
              @click="
                $bvModal.show(
                  'modal-scoped-meta-' + random_id() + '-' + result.id
                )
              "
            >
              <a href="javascript:void(0);"
                ><i class="fas fa-database mr-1" aria-hidden="true"></i
                >Metadata</a
              >
            </div>
            <b-modal
              :id="'modal-scoped-meta-' + random_id() + '-' + result.id"
              :title="normalizeTitle(result.title)"
              size="lg"
            >
              <DocumentMetadata :metadata="result" />
            </b-modal>
            <div
              class="small mt-2 mb-2"
              @click="
                $bvModal.show('modal-scoped-' + random_id() + '-' + result.id)
              "
            >
              <a href="javascript:void(0);"
                ><i class="fas fa-chart-bar fa-lg mr-1" aria-hidden="true"></i
                >Topics</a
              >
            </div>
            <b-modal
              :id="'modal-scoped-' + random_id() + '-' + result.id"
              :title="normalizeTitle(result.title)"
              size="lg"
            >
              <DocumentTopic :doc_id="result.id" />
            </b-modal>
          </div>
          <div class="sub-title">
            <div>
              <span class="study-by">{{
                result.major_doc_type[0].replace(
                  "Publications and Research",
                  "Publications and Reports"
                )
              }}</span>
            </div>
          </div>
          <div class="survey-stats">
            <span>Created on: {{ getDate(result.date_published) }} </span>
            <span>Last modified: {{ getDate(result.last_update_date) }} </span>
            <span>Views: {{ result.views }}</span>
          </div>
        </div>
      </div>
    </div>
    <a
      style="text-decoration: none"
      v-if="show_related && !loading"
      v-b-toggle
      :href="'#' + result.id"
      v-on:click="activateSubmit()"
      @click.prevent
      >Related documents
      <span>
        <i
          class="fa"
          :class="related_docs_visible ? 'fa-chevron-up' : 'fa-chevron-down'"
        ></i>
      </span>
    </a>
    <b-collapse
      v-show="related_docs_visible && !loading"
      v-model="related_docs_visible"
      :id="result.id"
    >
      <RelatedDocsPanel
        :reference_id="result.id"
        :submit="submit_related"
        :first_entry="match && match.rank === 1"
        @errorStatus="relatedDocsError()"
        @firstEntryReady="openRelatedDocs()"
      />
    </b-collapse>
    <hr />
  </div>
</template>

<script>
import RelatedDocsPanel from "./RelatedDocsPanel";
import DocumentTopic from "./DocumentTopic";
import DocumentMetadata from "./DocumentMetadata";
import SearchResultLoading from "./SearchResultLoading";

import Authors from "./Authors";
import ReadMore from "vue-read-more";
import Vue from "vue";

Vue.use(ReadMore);
export default {
  name: "SearchResultCard",
  props: {
    result: Object,
    match: Object,
    highlights: Object,
    loading: { type: Boolean, default: false },
  },
  components: {
    RelatedDocsPanel,
    DocumentTopic,
    DocumentMetadata,
    Authors,
    SearchResultLoading,
  },
  mounted() {
    this.resetStateParams();
  },
  data: function () {
    return {
      submit_related: false,
      rrandom_id: null,
      related_docs_visible: false,
      show_related: true,
    };
  },
  computed: {
    document_cover() {
      return (
        "/nlp/static/corpus/" +
        this.result.corpus +
        "/COVER/" +
        this.result.id +
        ".png"
      );
    },
    document_link() {
      return "/document/" + this.result.id;
    },
  },
  methods: {
    normalizeTitle(title) {
      if (title.endsWith(".pdf")) {
        title = title.slice(0, title.length - 4);
      }
      return title;
    },
    truncate(value, size) {
      return (value.toFixed(size) * 100 + "").slice(0, size + 1);
    },
    random_id() {
      if (this.rrandom_id === null) {
        this.rrandom_id = Math.random();
      }
      return this.rrandom_id;
    },
    getDate: function (date) {
      date = new Date(date).toDateString();
      date = date.split(" ");

      return date[1] + " " + date[2] + ", " + date[3];
    },
    activateSubmit: function () {
      if (this.submit_related === false) {
        this.submit_related = true;
      }
    },
    relatedDocsError(error) {
      if (error === true) {
        this.show_related = false;
      }
    },
    openRelatedDocs() {
      this.related_docs_visible = true;
      this.submit_related = true;
    },
    resetStateParams() {
      this.related_docs_visible = false;
      this.submit_related = false;
      if (this.match && this.match.rank === 1) {
        this.activateSubmit();
      }
    },
  },
  watch: {
    result() {
      this.resetStateParams();
    },
  },
};
</script>
<style>
.document-row .study-country {
  font-size: small;
}
.highlight {
  font-size: small;
}
.highlight em {
  font-weight: bold;
  font-style: normal;
}
.highlight p {
  margin-bottom: 0.1rem;
}
</style>