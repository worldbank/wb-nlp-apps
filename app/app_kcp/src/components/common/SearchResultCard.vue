<template>
  <div>
    <div class="document-row" data-url="#" title="View study">
      <div class="row">
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
              <!-- <router-link :to="document_link" :title="result.title"> -->
              {{ result.title }}</router-link
            >
          </h5>

          <!-- <Authors /> -->
          <Authors :authors="result.author" />

          <div v-if="highlights" class="highlight">
            <read-more
              more-str="read more"
              :text="highlights.body.join('... ').replace(/\s\s+/g, ' ') || ''"
              link="#"
              less-str="read less"
              :max-chars="200"
            ></read-more>
          </div>

          <div class="study-country">
            {{ result.country[0] }}, {{ result.year }}
          </div>

          <div class="study-id d-md-flex mt-2">
            <span class="badge badge-pill badge-secondary"
              >ID: {{ result.id }}</span
            >
            <div class="small ml-md-3 mt-2 mt-md-0">
              Corpus: {{ result.corpus
              }}<span v-if="match && match.rank">, Rank: {{ match.rank }}</span
              ><span v-if="match && match.score"
                >, Score: {{ match.score.toFixed(4) }}</span
              ><span v-if="match && match.topic"
                ><span
                  v-for="topic_id_score in Object.entries(match.topic)"
                  :key="topic_id_score"
                  >, {{ topic_id_score[0].replace("_", " ") }}:
                  {{ topic_id_score[1].toFixed(4) * 100 }}%</span
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
              :title="result.title"
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
              :title="result.title"
              size="lg"
            >
              <DocumentTopic :doc_id="result.id" />
            </b-modal>
          </div>
          <div class="sub-title">
            <div>
              <span class="study-by">{{ result.major_doc_type[0] }}</span>
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
      v-b-toggle
      :href="'#' + result.id"
      v-on:click="activateSubmit()"
      @click.prevent
      >Related documents...</a
    >
    <b-collapse :id="result.id">
      <RelatedDocsPanel :reference_id="result.id" :submit="submit_related" />
    </b-collapse>
    <hr />
  </div>
</template>

<script>
import RelatedDocsPanel from "./RelatedDocsPanel";
import DocumentTopic from "./DocumentTopic";
import DocumentMetadata from "./DocumentMetadata";
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
  },
  components: {
    RelatedDocsPanel,
    DocumentTopic,
    DocumentMetadata,
    Authors,
  },
  data: function () {
    return {
      submit_related: false,
      rrandom_id: null,
    };
  },
  computed: {
    document_cover() {
      return (
        "/nlp/static/" +
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