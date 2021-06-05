<template>
  <div>
    <header>
      <h1 class="blog-post-title mb-3" dir="auto">
        {{ page_title }}
      </h1>
    </header>
    <div>
      <p class="mt-3">
        As of {{ date_now }}, our corpus contains
        {{ corpus_size.toLocaleString() }} documents (last updated on
        <span v-if="last_update_date">{{
          last_update_date.toDateString()
        }}</span
        >).
      </p>
      <p class="mt-1 text-justify">
        The volume of the corpus can be measured by the number of documents it
        contains, or by the number of tokens in the documents (tokens are the
        ‘useful’ words that remain in a document after we remove stop words,
        links, etc.). The charts below show summary statistics (numbers and
        percentages) of the number of documents and tokens by year, source, and
        type.
      </p>

      <br />

      <VolumeChart
        v-if="corpus"
        :data="corpus"
        :field="corpus.field"
        field_name="source"
      />

      <p class="mt-4"></p>

      <VolumeChart
        v-if="major_doc_type"
        :data="major_doc_type"
        :field="major_doc_type.field"
        field_name="document type"
      />
    </div>
  </div>
</template>

<script>
import VolumeChart from "../../common/VolumeChart";

export default {
  name: "Volume",
  components: {
    // VChart,
    VolumeChart,
  },
  props: {
    page_title: String,
  },
  mounted() {
    this.getFullCorpusData();
    this.getCorpusSize();
    this.getLastUpdateDate();
  },
  computed: {
    defaultOptions() {
      return {
        title: {
          text: "Corpus volume",
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#6a7985",
            },
          },
        },
        legend: {
          data: [],
        },
        toolbox: {
          feature: {
            // dataZoom: {
            //   yAxisIndex: "none",
            // },
            // restore: {},
            saveAsImage: {},
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "10%",
          containLabel: true,
        },
        xAxis: [
          {
            type: "category",
            boundaryGap: false,
            data: [],
          },
        ],
        yAxis: [
          {
            type: "value",
            axisLabel: {
              formatter: "{value}",
            },
          },
        ],
        dataZoom: [
          {
            type: "inside",
            start: 20,
            end: 100,
          },
          {
            start: 20,
            end: 100,
            handleIcon:
              "M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z",
            handleSize: "50%",
            handleStyle: {
              color: "#fff",
              shadowBlur: 3,
              shadowColor: "rgba(0, 0, 0, 0.6)",
              shadowOffsetX: 2,
              shadowOffsetY: 2,
            },
          },
        ],
        series: [],
      };
    },
  },
  data: function () {
    return {
      loading: false,

      date_now: new Date().toDateString(),
      corpus_size: "",

      corpus: null,
      major_doc_type: null,

      last_update: null,
      last_update_date: null,
    };
  },
  methods: {
    updateOption(data, value, label) {
      return {
        title: {
          text: "Topic profiles" + "(" + label + ")",
        },
        legend: {
          data: data[value].legend,
        },
        xAxis: [
          {
            type: "category",
            boundaryGap: false,
            data: data[value].year,
          },
        ],
        yAxis: [
          {
            type: "value",
            axisLabel: {
              formatter: value === "share" ? "{value} %" : "{value}",
            },
          },
        ],
        series: data[value].series,
      };
    },
    getFullCorpusData: function () {
      this.loading = true;

      const params = new URLSearchParams();
      params.append("fields", "corpus");
      params.append("fields", "major_doc_type");
      params.append("app_tag_jdc", true);

      this.$http
        .get(this.$config.corpus_url + "/get_corpus_volume_by", {
          params: params,
        })
        .then((response) => {
          let data = response.data;

          this.corpus = data.corpus;
          this.major_doc_type = data.major_doc_type;

          this.loading = false;
        })

        .finally(() => {});
    },
    getCorpusSize() {
      this.$http
        .get("/nlp/corpus/get_corpus_size?app_tag_jdc=true")
        .then((response) => {
          this.corpus_size = response.data.size;
        });
    },
    getLastUpdateDate() {
      this.$http.get("/nlp/corpus/get_last_update_date").then((response) => {
        this.last_update = response.data;
        if (this.last_update) {
          this.last_update_date = new Date(this.last_update.last_update_date);
        }
      });
    },
  },
  watch: {},
};
</script>
