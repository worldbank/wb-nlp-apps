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
        <div v-show="!loading && hasNation" class="microdata-info">
          <span class="xsl-caption field-caption">Country / countries:</span>
          {{ countries }}
        </div>
      </div>

      <div v-show="loading" class="text-center">
        <b-spinner></b-spinner>
      </div>

      <div class="microdata-info" v-if="hasAbstract">
        <span class="xsl-caption field-caption">Abstract</span>
      </div>

      <div class="microdata-abstract" v-if="hasAbstract">
        <div class="text-justify" v-html="abstract"></div>
      </div>

      <div class="microdata-info" v-if="hasStudyScope">
        <span class="xsl-caption field-caption">Scope</span>
      </div>

      <div class="microdata-study-scope" v-if="hasStudyScope">
        <div class="text-justify" v-html="study_scope"></div>
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
    countries() {
      if (this.microdata_meta) {
        return this.microdata_meta.dataset.metadata.study_desc.study_info.nation
          .map((o) => {
            return o.name;
          })
          .join("; ");
      }
      return null;
    },
    abstract() {
      return this.microdata_meta.dataset.metadata.study_desc.study_info.abstract.replaceAll(
        "\n",
        "<br/>"
      );
    },
    study_scope() {
      return this.microdata_meta.dataset.metadata.study_desc.study_info.study_scope.replaceAll(
        "\n",
        "<br/>"
      );
    },
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
      return this.hasField("abstract");
    },
    hasNation() {
      return this.hasField("nation");
    },
    hasStudyScope() {
      return this.hasField("study_scope");
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
        .get("/nlp/extra/microdata/get_microdata_study_info/" + result.id)
        .then((response) => {
          this.microdata_meta = response.data;
          this.loading = false;
        });
    },
    metadataLink(result) {
      return "https://catalog.ihsn.org/catalog/study/" + result.id;
    },
    hasField(field) {
      if (this.microdata_meta) {
        if (this.microdata_meta.dataset) {
          if (this.microdata_meta.dataset.metadata) {
            if (this.microdata_meta.dataset.metadata.study_desc) {
              if (this.microdata_meta.dataset.metadata.study_desc.study_info) {
                if (
                  this.microdata_meta.dataset.metadata.study_desc.study_info[
                    field
                  ]
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
  margin-bottom: 20px;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* Internet Explorer 10+ */
}

.microdata-study-scope {
  max-width: 100%;
  max-height: 500px;
  overflow-y: scroll;
  margin-bottom: 20px;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* Internet Explorer 10+ */
}

.microdata-abstract::-webkit-scrollbar {
  /* WebKit */
  width: 0;
  height: 0;
}

.microdata-study-scope::-webkit-scrollbar {
  /* WebKit */
  width: 0;
  height: 0;
}
</style>