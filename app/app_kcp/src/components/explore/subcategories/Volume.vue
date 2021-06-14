<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      <p>
        Knowledge produced may be measured by the volume of documents published
        or the length of content in a document. In this page, we show some
        summary statistics regarding the breakdown of document count and total
        number of tokens present in the corpus by source over time. Furthermore,
        we show some World Bank specific breakdowns below.
      </p>

      <br />

      <VolumeChart
        v-if="corpus"
        :data="corpus"
        :field="corpus.field"
        field_name="source"
      />
      <br />
      <br />

      <p>
        The World Bank corpus, via its API, contains standardized data on
        document types and topics. We use these standardized metadata to further
        breakdown the World Bank corpus to also show trends of document count
        and token composition by document type and topics.
      </p>
      <br />
      <br />

      <VolumeChart
        v-if="major_doc_type"
        :data="major_doc_type"
        :field="major_doc_type.field"
        field_name="document type (WB)"
      />
      <br />
      <br />
      <p>
        As documents may be tagged with multiple topics, we see that the
        breakdown by share of topics in the WB corpus have a total of more than
        100%. Nonetheless, comparison of share among topics will yield some
        insights regarding the general interest or popularity over time of one
        topic over other topics of comparison.
      </p>
      <br />
      <br />
      <VolumeChart
        v-if="topics_src"
        :data="topics_src"
        :field="topics_src.field"
        field_name="topic (WB)"
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
    this.$http.get("/static/data/corpus_details.json").then((response) => {
      this.items = response.data;
    });
    this.getFullCorpusData();
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

      corpus: null,
      major_doc_type: null,
      topics_src: null,
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
      params.append("fields", "topics_src");

      this.$http
        .get(this.$config.corpus_url + "/get_corpus_volume_by", {
          params: params,
        })
        .then((response) => {
          let data = response.data;

          this.corpus = data.corpus;
          this.major_doc_type = data.major_doc_type;
          this.topics_src = data.topics_src;

          this.loading = false;
        })

        .finally(() => {});
    },
  },
  watch: {},
};
</script>
