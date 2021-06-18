<template>
  <div>
    <div v-if="metadata[result.id]">
      <hr />
      <p class="lead">
        <a :href="metadataLink(result)" target="_blank">{{
          metadata[result.id].title
        }}</a>
      </p>
      <div class="microdata-info-wrapper">
        <div class="microdata-info">
          <span class="xsl-caption field-caption">Year:</span>
          {{ year }}
        </div>
        <div class="microdata-info">
          <span class="xsl-caption field-caption">ID:</span> {{ result.id }}
        </div>
        <div class="microdata-info">
          <span class="xsl-caption field-caption">Country / countries:</span>
          {{ metadata[result.id].countries }}
        </div>
      </div>

      <div v-show="loading" class="text-center">
        <b-spinner></b-spinner>
      </div>

      <div class="microdata-info" v-if="hasAbstract">
        <span class="xsl-caption field-caption">Abstract</span>
      </div>

      <div class="microdata-abstract" v-if="hasAbstract">
        <span style="white-space: pre-wrap">{{
          microdata_meta.dataset.metadata.study_desc.study_info.abstract
        }}</span>
      </div>
      <br />
    </div>
  </div>
</template>
<script>
export default {
  components: {},
  name: "MicrodataCard",
  props: {
    result: Object,
    metadata: Object,
  },
  computed: {
    year() {
      if (
        this.metadata[this.result.id].year_from ==
        this.metadata[this.result.id].year_to
      ) {
        return this.metadata[this.result.id].year_from;
      }
      return (
        this.metadata[this.result.id].year_from +
        "-" +
        this.metadata[this.result.id].year_to
      );
    },
    hasAbstract() {
      if (this.microdata_meta) {
        if (this.microdata_meta.dataset) {
          if (this.microdata_meta.dataset.metadata) {
            if (this.microdata_meta.dataset.metadata.study_desc) {
              if (this.microdata_meta.dataset.metadata.study_desc.study_info) {
                if (
                  this.microdata_meta.dataset.metadata.study_desc.study_info
                    .abstract
                ) {
                  return true;
                }
              }
            }
          }
        }
      }
      return false;
    },
  },
  mounted() {
    this.fetchMicrodataStudyInfo(this.result);
  },
  data() {
    return {
      //   results: [],
      loading: false,
      indicator_name: null,
      microdata_meta: null,
      //   metadata: null,
    };
  },
  methods: {
    fetchMicrodataStudyInfo(result) {
      this.loading = true;
      this.$http
        // .get("https://catalog.ihsn.org/api/catalog/" + result.id)

        .get("/nlp/extra/microdata/get_microdata_metadata/" + result.id)
        .then((response) => {
          this.microdata_meta = response.data;
          this.loading = false;
        });
    },
    metadataLink(result) {
      return "https://catalog.ihsn.org/catalog/study/" + result.id;
    },
  },
};
</script>
<style scoped>
.vue-horizontal {
  /* border: 3px solid #dbdbdb; */
  border: 0px;
  padding: 5px;
}
.microdata-related-section {
  /* width: 40vh; */
  width: 100%;
  padding: 0px 20px;
  margin: 3px;
  height: 400px;
  background: #ffffff;
  /* background: #f3f3f3; */
  border: 2px solid #ebebeb;
  border-radius: 4px;
  margin-bottom: 20px;
}
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

.microdata-info-wrapper {
  margin-bottom: 20px;
}
.microdata-info {
  margin-right: 50px;
}

.microdata-abstract {
  max-width: 100%;
  max-height: 500px;
  overflow-y: scroll;
}
</style>