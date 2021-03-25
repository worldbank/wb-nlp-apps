<template>
  <div>
    <div v-if="metadata" class="container">
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
              <span class="study-by">{{ metadata.major_doc_type[0] }}</span>
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
            Metadata
            <i class="fa fa-download" aria-hidden="true"> </i>
            :
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
          >
            <b-tab
              title="Metadata"
              :title-item-class="itemClass(0)"
              :title-link-class="linkClass(0)"
              active
            >
              <div>
                <MetadataViewer
                  :metadata="metadata"
                  :show_raw_metadata="true"
                /></div
            ></b-tab>
            <b-tab
              title="View document"
              :title-item-class="itemClass(1)"
              :title-link-class="linkClass(1)"
            >
              <br />
              <div>
                <iframe
                  ref="iframe"
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
                <h4>Related documents from topic model</h4>
                <RelatedDocsPanel
                  :section_height="150"
                  :reference_id="metadata.id"
                  :submit="submit_related"
                />
                <br /><br />
                <h4>Related documents from word embedding model</h4>
                <RelatedDocsPanel
                  :section_height="150"
                  :reference_id="metadata.id"
                  model_name="word2vec"
                  :submit="submit_related"
                /></div
            ></b-tab>
            <b-tab
              :title-item-class="itemClass(3)"
              :title-link-class="linkClass(3)"
              v-on:click="activateSubmit()"
              @click.prevent
              title="Related WDI indicators"
            >
              <div>
                <SimilarWDIViewer :doc_id="metadata.id" /></div
            ></b-tab>
          </b-tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RelatedDocsPanel from "./RelatedDocsPanel";
import MetadataViewer from "./MetadataViewer";
import SimilarWDIViewer from "./SimilarWDIViewer";

export default {
  name: "DocumentPage",
  props: {},
  mounted() {
    window.vm = this;
    this.getMetadata();
  },
  computed: {
    metadata() {
      if (
        this.result !== undefined &&
        this.$route.params.doc_id !== this.result.id &&
        !this.loading
      ) {
        if (sessionStorage[this.$route.params.doc_id] === undefined) {
          this.getMetadata();
        } else {
          this.loadStorage();
        }
      }
      return this.result;
    },
    metadata_download_link() {
      return "/nlp/corpus/get_metadata_by_id?id=" + this.metadata.id;
    },
  },
  components: { RelatedDocsPanel, MetadataViewer, SimilarWDIViewer },

  data: function () {
    return {
      result: this.metadata,
      submit_related: false,
      tabIndex: 0,
      loading: false,
    };
  },
  methods: {
    loadStorage() {
      this.result = JSON.parse(
        sessionStorage.getItem(this.$route.params.doc_id)
      );
    },
    getMetadata() {
      if (this.$route.params.metadata !== undefined) {
        this.result = this.$route.params.metadata;
        sessionStorage.setItem(
          this.$route.params.doc_id,
          JSON.stringify(this.result)
        );
      } else {
        this.loading = true;
        this.$http
          .get("/nlp/corpus/get_metadata_by_id", {
            params: { id: this.$route.params.doc_id },
          })
          .then((response) => {
            this.result = response.data;
            sessionStorage.setItem(
              this.$route.params.doc_id,
              JSON.stringify(this.result)
            );
          })
          .finally(() => {
            this.loading = false;
          });
      }
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
    setIFrame() {
      var iframe = this.$refs.iframe;
      if (iframe !== undefined && this.metadata !== undefined) {
        var container = iframe.parentElement;
        iframe.remove();
        iframe.src = this.metadata.url_pdf;
        container.append(iframe);
      }
    },
  },
  watch: {
    metadata: function () {
      this.setIFrame();
      this.tabIndex = 0;
    },
  },
};
</script>

<style>
.tab-link-format {
  margin: 10px;
  background-color: transparent !important;
  padding-top: 5px !important;
  border: 0px !important;
}

.tab-item-format {
  margin: 10px;
  background-color: transparent !important;
  padding: 5px;
}
.doc-active-tab {
  margin-bottom: 50px;
  padding-right: 30px;
  padding-left: 30px;
}
</style>