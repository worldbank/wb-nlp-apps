<template>
  <div>
    <!-- <Header /> -->
    <div class="container">
      <br />
      <div class="row">
        <div class="col-3 col-lg-3">
          <img
            src="/static/files/doc_thumb.png"
            title="document thumbnail"
            alt="document thumbnail"
          />
        </div>
        <div class="col-9 col-lg-9">
          <h3 class="title">
            <a :href="metadata.url_pdf" :title="metadata.title" target="_blank">
              {{ metadata.title }}</a
            >
          </h3>
          <div class="study-country">
            {{ metadata.country[0] }}, {{ metadata.year }}
          </div>
          <div class="sub-title">
            <div>
              <span class="study-by">Ministry of Public Health</span>
            </div>
            <div class="owner-collection">
              Corpus:
              <router-link to="/search/">{{ metadata.corpus }}</router-link>
            </div>
          </div>
          <div class="survey-stats">
            <span>Created on: {{ getDate(metadata.date_published) }} </span>
            <span
              >Last modified: {{ getDate(metadata.last_update_date) }}
            </span>
            <span>Views: {{ metadata.views }}</span>
          </div>
          <span class="mr-3 link-col float-left">
            <medium>
              Metadata
              <i class="fa fa-download" aria-hidden="true"> </i></medium
            >:
            <a :href="metadata_download_link" target="_blank" title="JSON">
              <span class="badge badge-info">JSON</span>
            </a>
          </span>
        </div>
      </div>
      <br />
      <div class="row">
        <div class="col-12 doc-tabs">
          <b-tabs
            v-model="tabIndex"
            active-nav-item-class="doc-tab-item"
            active-tab-class="doc-active-tab"
            content-class="mt-12"
            style="height: 800px"
          >
            <b-tab
              title="Metadata"
              :title-item-class="itemClass(0)"
              :title-link-class="linkClass(0)"
              active
            >
              <!-- <template #title>
                <div>
                  <strong>Metadata</strong>
                </div>
              </template> -->
              <div><br /><MetadataViewer :metadata="metadata" /></div
            ></b-tab>
            <b-tab
              title="View document"
              :title-item-class="itemClass(1)"
              :title-link-class="linkClass(1)"
            >
              <!-- <template #title>
                <div style="color: blue">
                  <strong>View document</strong>
                </div>
              </template> -->
              <div>
                <iframe
                  width="100%"
                  height="600px"
                  :src="metadata.url_pdf"
                /></div
            ></b-tab>
            <b-tab
              :title-item-class="itemClass(2)"
              :title-link-class="linkClass(2)"
              v-on:click="activateSubmit()"
              @click.prevent
              title="Related documents"
            >
              <div>
                <br />
                <h3>LDA model</h3>
                <RelatedDocsPanel
                  :section_height="150"
                  :reference_id="metadata.id"
                  :submit="submit_related"
                />
                <br />
                <h3>Word2vec model</h3>
                <RelatedDocsPanel
                  :section_height="150"
                  :reference_id="metadata.id"
                  model_name="word2vec"
                  :submit="submit_related"
                /></div
            ></b-tab>
          </b-tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import Header from "../Header.vue";
import RelatedDocsPanel from "./RelatedDocsPanel";
import MetadataViewer from "./MetadataViewer";

export default {
  name: "DocumentPage",
  props: {
    // metadata: Object,
  },
  mounted() {
    window.vm = this;
    this.getMetadata();
  },
  computed: {
    metadata() {
      return this.result;
    },
    metadata_download_link() {
      return "/nlp/corpus/get_metadata_by_id?id=" + this.metadata.id;
    },
  },
  components: { RelatedDocsPanel, MetadataViewer },

  data: function () {
    return {
      result: localStorage[this.$route.params.doc_id],
      submit_related: false,
      tabIndex: 0,
    };
  },
  methods: {
    getMetadata() {
      //   this.$http
      //     .get("/nlp/corpus/get_metadata_by_id", {
      //       params: { id: this.$route.params.doc_id },
      //     })
      //     .then((response) => {
      //       this.metadata = response.data;
      //     });
      this.result = this.$route.params.metadata;
      localStorage[this.$route.params.doc_id] = this.result;
      console.log(this.metadata);
    },
    activateSubmit: function () {
      if (this.submit_related === false) {
        this.submit_related = true;
      }
    },
    getDate: function (date) {
      date = new Date(date).toDateString();
      date = date.split(" ");

      return date[1] + " " + date[2] + ", " + date[3];
    },
    linkClass(idx) {
      if (this.tabIndex === idx) {
        // return ["bg-primary", "text-light", "tab-link-format", "active"];
        return ["text-primary", "tab-link-format", "active"];
      } else {
        return ["bg-light", "text-dark", "tab-link-format"];
      }
    },
    itemClass(idx) {
      if (this.tabIndex === idx) {
        return ["tab-item-format"];
      } else {
        return ["tab-item-format"];
      }
    },
  },
};
// <style scoped src="bootstrap/dist/css/bootstrap.css"></style>
</script>

<style>
/* .doc-tab-item {
  color: green;
} */
.tab-link-format {
  margin: 10px;
  /* background: transparent !important; */
  background-color: transparent !important;
  padding-top: 5px !important;
  border: 0px !important;
  /* margin: 5px; */
  /* margin-bottom: 1px; */
}

.tab-item-format {
  margin: 10px;
  /* background: transparent !important; */
  background-color: transparent !important;
  padding: 5px;
  /* margin-bottom: 1px; */
}
.doc-active-tab {
  max-height: 680px;
  overflow: scroll;
}
</style>