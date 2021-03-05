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
      <v-chart
        v-if="this.graph !== null"
        class="chart"
        :option="option2"
        autoresize="true"
        :loading="loading"
      />
      <!-- <div v-if="this.graph === null">
        <b-skeleton-img></b-skeleton-img>
      </div> -->
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
    blurContent: function () {
      return this.loading;
    },
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
            name: "Related word",
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
            focusNodeAdjacency: true,
            itemStyle: {
              borderColor: "#fff",
              borderWidth: 1,
              shadowBlur: 10,
              shadowColor: "rgba(0, 0, 0, 0.3)",
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
      loading: false,
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
      this.loading = true;
      if (typeof text !== "string") {
        text = this.raw_text;
      } else {
        this.raw_text = text;
      }
      this.related_words = [];
      const body = {
        model_id: "777a9cf47411f6c4932e8941f177f90a",
        raw_text: text,
        topn_words: 8,
        topn_sub: 5,
        edge_thresh: 0.8,
        metric: "cosine_similarity",
      };

      this.$http
        .post("/nlp/models/word2vec2/get_similar_words_graph", body)
        .then((response) => {
          var graph = response.data.graph_data;
          this.related_words = response.data.similar_words;
          graph.nodes.forEach(function (node) {
            node.label = {
              show: node.symbolSize > 5,
            };
            node.draggable = true;
            // node.x = node.y = null;
          });
          this.graph = graph;
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
          this.loading = false;
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.chart {
  height: 600px;
}

.blur {
  filter: blur(1px);
  opacity: 0.4;
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
