<template>
  <div>
    <div v-if="metadata" class="container">
      <div class="mt-2">
        <router-link to="/search/">Back to search</router-link>
      </div>
      <div class="mt-4 row">
        <div class="col-sm-12 col-md-3">
          <img
            width="100%"
            :src="document_cover"
            onerror="if (this.src != '/static/files/doc_thumb.png') this.src = '/static/files/doc_thumb.png';"
            title="document thumbnail"
            alt="document thumbnail"
          />
        </div>
        <div class="col-sm-12 col-md-9">
          <h3 class="title">
            {{ metadata.title }}
          </h3>

          <!-- <Authors /> -->
          <Authors :authors="metadata.author" authors_class="authors-large" />

          <div class="abstract">
            <read-more
              more-str="read more"
              :text="metadata.abstract || ''"
              link="#"
              less-str="read less"
              :max-chars="500"
            ></read-more>
          </div>

          <div
            v-if="metadata.country && metadata.country.length > 0"
            class="study-country"
          >
            {{ metadata.country[0] }}, {{ metadata.year }}
          </div>
          <div class="sub-title">
            <div>
              Category:
              <span class="study-by">{{
                metadata.major_doc_type[0].replace(
                  "Publications and Research",
                  "Publications and Reports"
                )
              }}</span>
            </div>
            <div class="owner-collection">
              Corpus:
              <router-link to="/search/">{{ metadata.corpus }}</router-link>
            </div>
            <div v-if="metadata.corpus === 'WB' && metadata.url_pdf">
              Open in:
              <a
                :href="document_wbdocs_link"
                :title="metadata.title"
                target="_blank"
                >World Bank Documents and Reports</a
              >
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
                  height="800px"
                  type="application/pdf"
                  :src="
                    'https://docs.google.com/gview?url=' +
                    metadata.url_pdf +
                    '&embedded=true'
                  "
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
                <h4>
                  {{ lda_show_related ? "R" : "No r" }}elated documents from
                  topic model
                </h4>
                <RelatedDocsPanel
                  :section_height="150"
                  :reference_id="metadata.id"
                  :submit="submit_related"
                  @errorStatus="
                    (error) => {
                      if (error === true) {
                        lda_show_related = false;
                      }
                    }
                  "
                />
                <br /><br />
                <h4>
                  {{ word2vec_show_related ? "R" : "No r" }}elated documents
                  from word embedding model
                </h4>
                <RelatedDocsPanel
                  :section_height="150"
                  :reference_id="metadata.id"
                  model_name="word2vec"
                  :submit="submit_related"
                  @errorStatus="
                    (error) => {
                      if (error === true) {
                        word2vec_show_related = false;
                      }
                    }
                  "
                /></div
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
import Authors from "./Authors";
import ReadMore from "vue-read-more";
import Vue from "vue";

Vue.use(ReadMore);
export default {
  name: "DocumentPage",
  props: {},
  mounted() {
    // window.vm = this;
    this.getMetadata();
  },
  computed: {
    document_wbdocs_link() {
      return this.result.url_pdf
        .replace(
          "/curated/en/",
          "/en/publication/documents-reports/documentdetail/"
        )
        .replace("/pdf/", "/")
        .replace(".pdf", "");
      // http://documents1.worldbank.org/curated/en/699851600091617671/pdf/The-African-Context-on-COVID-19.pdf
      // https://documents.worldbank.org/en/publication/documents-reports/documentdetail/699851600091617671/the-african-context-on-covid-19
    },
    document_cover() {
      return (
        "/nlp/static/corpus/" +
        this.result.corpus +
        "/COVER/" +
        this.result.id +
        ".png"
      );
    },
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
      return (
        this.$config.corpus_url + "/get_metadata_by_id?id=" + this.metadata.id
      );
    },
  },
  components: {
    RelatedDocsPanel,
    MetadataViewer,
    Authors,
  },

  data: function () {
    return {
      result: this.metadata,
      submit_related: false,
      tabIndex: 0,
      loading: false,
      lda_show_related: true,
      word2vec_show_related: true,
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
          .get(this.$config.corpus_url + "/get_metadata_by_id", {
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
/* p {
  margin-bottom: 1px;
}
span > a {
  float: right;
} */
.tab-link-format {
  margin: 10px;
  background-color: transparent !important;
  padding-top: 5px !important;
  border: 0px !important;
}
.study-country {
  margin-top: 10px;
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
.abstract p {
  margin-bottom: 0.1rem;
}
</style>