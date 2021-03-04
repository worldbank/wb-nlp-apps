<template>
  <div>
    <h1>{{ page_title }}</h1>
    <br />
    <b-form-input
      width="100%"
      v-model="raw_text"
      placeholder="Enter word(s)"
      v-on:keyup.enter="getGraph"
    />
    <b-badge
      v-for="rw in this.related_words"
      :key="rw"
      variant="success"
      style="margin-right: 5px"
      >{{ rw.word }}
    </b-badge>
    <br />
    <br />
    <b-container fluid>
      <v-chart v-if="this.graph !== null" class="chart" :option="option2" />

      <!-- <b-row>
        <b-col md="9" class="border-right">
          <EmbeddingViz @selected="getRelatedWords"></EmbeddingViz>
        </b-col>
        <b-col md="3">
          <h2>Try the API!</h2>
          <b-form-input
            width="100%"
            v-model="raw_text"
            placeholder="Enter word(s)"
            v-on:keyup.enter="getRelatedWords"
          />
          <br />
          <h4 v-show="raw_text">Input text</h4>
          {{ raw_text }}
          <br />
          <br />

          <div v-show="loading">
            <b-skeleton-table
              v-show="loading"
              animation="wave"
              :rows="10"
              :columns="1"
              :table-props="{ bordered: true, striped: true }"
            ></b-skeleton-table>
          </div>

          <h4 v-show="related_words.length > 0">Similar words</h4>

          <b-list-group v-show="!loading" flush>
            <b-list-group-item
              v-for="related_word in related_words"
              :key="related_word.word"
            >
              {{ related_word.word }}
            </b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row> -->
    </b-container>
  </div>
</template>

<script>
import { use } from "echarts/core";

import { CanvasRenderer } from "echarts/renderers";
import { GraphChart } from "echarts/charts";
import { PieChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";

use([
  CanvasRenderer,
  GraphChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
]);

export default {
  name: "WordEmbeddings",
  components: {
    VChart,
  },
  provide: {
    [THEME_KEY]: "light",
  },
  props: {
    page_title: String,
  },
  mounted() {
    this.getGraph();
    window.vm = this;
  },
  computed: {
    option2() {
      return {
        title: {
          text: "Related words graph",
          subtext: "Default layout",
          top: "bottom",
          left: "right",
        },
        tooltip: {},
        legend: [
          {
            // selectedMode: 'single',
            data: this.graph.categories.map(function (a) {
              return a.name;
            }),
          },
        ],
        animationDuration: 1500,
        animationEasingUpdate: "quinticInOut",
        series: [
          {
            name: "Les Miserables",
            type: "graph",
            layout: "none",
            data: this.graph.nodes,
            links: this.graph.links,
            categories: this.graph.categories,
            roam: true,
            label: {
              position: "right",
              formatter: "{b}",
            },
            lineStyle: {
              color: "source",
              curveness: 0.3,
            },
            emphasis: {
              focus: "adjacency",
              lineStyle: {
                width: 10,
              },
            },
          },
        ],
      };
    },
  },
  data() {
    return {
      graph: null,
      raw_text: "",
      related_words: [],
      option: {
        title: {
          text: "Traffic Sources",
          left: "center",
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        legend: {
          orient: "vertical",
          left: "left",
          data: [
            "Direct",
            "Email",
            "Ad Networks",
            "Video Ads",
            "Search Engines",
          ],
        },
        series: [
          {
            name: "Traffic Sources",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: [
              { value: 335, name: "Direct" },
              { value: 310, name: "Email" },
              { value: 234, name: "Ad Networks" },
              { value: 135, name: "Video Ads" },
              { value: 1548, name: "Search Engines" },
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      },
    };
  },
  // data: function () {
  //   return {
  //     nlp_api_url: "/nlp/models/word2vec/get_similar_words",
  //     related_words: [],
  //     raw_text: "",
  //     loading: true,
  //   };
  // },
  // mounted() {
  //   this.getRelatedWords();
  // },
  methods: {
    getGraph: function (text = null) {
      if (typeof text !== "string") {
        text = this.raw_text;
      } else {
        this.raw_text = text;
      }
      this.loading = true;
      this.related_words = [];
      const body = {
        model_id: "777a9cf47411f6c4932e8941f177f90a",
        raw_text: text,
        topn_words: 10,
        edge_thresh: 0.75,
        metric: "cosine_similarity",
      };

      this.$http
        .post("/nlp/models/word2vec2/get_similar_words_graph", body)
        .then((response) => {
          this.graph = response.data.graph_data;
          this.related_words = response.data.similar_words;
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
          this.loading = false;
        })
        .finally(() => (this.loading = false));
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.chart {
  height: 600px;
}

h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
