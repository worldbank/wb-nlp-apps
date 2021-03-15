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
        </div>
      </div>
      <br />
      <div class="row">
        <div class="col-12 doc-tabs">
          <b-tabs
            active-nav-item-class="active doc-tab-item "
            active-tab-class=""
            content-class="mt-12"
            style="height: 800px"
          >
            <b-tab title="Metadata" active>
              <div><p>I'm the first tab</p></div></b-tab
            >
            <b-tab title="View document">
              <div>
                <iframe
                  width="100%"
                  height="600px"
                  :src="metadata.url_pdf"
                /></div
            ></b-tab>
            <b-tab
              v-on:click="activateSubmit()"
              @click.prevent
              title="Related documents"
            >
              <div>
                <br />
                <h3>LDA model</h3>
                <RelatedDocsPanel
                  :section_height="200"
                  :reference_id="metadata.id"
                  :submit="submit_related"
                />
                <br />
                <h3>Word2vec model</h3>
                <RelatedDocsPanel
                  :section_height="200"
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
  },
  components: { RelatedDocsPanel },

  data: function () {
    return {
      result: localStorage[this.$route.params.doc_id],
      submit_related: false,
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
  },
};
// <style scoped src="bootstrap/dist/css/bootstrap.css"></style>
</script>

<style>
/* .doc-tab-item {
  color: green;
} */
</style>