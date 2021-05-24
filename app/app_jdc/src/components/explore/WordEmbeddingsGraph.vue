<template>
  <div>
    <h1>{{ page_title }}</h1>
    <br />
    <p>
      This demo provides a glimpse of how word embedding models are able to
      learn relationships of words when trained on a large corpus of data.
    </p>

    <p>
      To start, input a word or phrase in the text box below and press
      <span style="font-weight: bold">Enter</span>. The input is processed and
      closely related words are identified using the model. For each related
      word, we also find the closest words to it as well. We then compute the
      similarity between all of the shortlisted words and form a network based
      on their similarity score. We use modularity clustering to identify
      clusters within the graph network of these words. An interactive graph of
      the words is rendered for exploration.
    </p>
    <p>
      You can also explore further by
      <span style="font-weight: bold">double-clicking</span> on a node. This
      will refresh the graph with the data corresponding to the selected node.
    </p>

    <hr />

    <b-row align-v="center">
      <div class="col-11">
        <b-form-input
          v-model="raw_text"
          placeholder="Enter word(s)"
          v-on:keyup.enter="getGraph"
        />
      </div>
      <div class="col-1">
        <a
          v-show="api_link"
          title="Get API link"
          v-b-modal.modal-lg
          href="javascript:void(0);"
          class="btn btn btn-outline-success btn-sm wbg-button ml-2"
          ><i class="fab fa-searchengin"></i
        ></a>
        <b-modal id="modal-lg" size="lg" title="API link"
          ><a :href="api_link" target="_blank"
            ><span style="font-family: 'Courier New', Courier, monospace">{{
              api_link
            }}</span></a
          >
          <template #modal-footer>
            <div v-if="navigator.clipboard" class="w-100">
              <b-button
                variant="primary"
                size="sm"
                class="float-right"
                @click="copyText"
              >
                Copy to clipboard
              </b-button>
            </div>
          </template>
        </b-modal>
      </div>
    </b-row>

    <b-badge
      @click="getGraph(rw.word)"
      v-for="rw in this.related_words"
      :key="rw.word + rw.id"
      variant="success"
      style="margin-right: 5px; cursor: pointer"
      >{{ rw.word }}
    </b-badge>

    <br />
    <div v-if="this.graph === null && loading">
      <b-skeleton-img></b-skeleton-img>
    </div>
    <br />
    <b-container fluid>
      <v-chart
        @dblclick="searchNode"
        @mouseover="isHighlighted"
        v-if="this.graph !== null"
        class="chart"
        refs="graphChart"
        :option="option2"
        :autoresize="true"
        :loading="loading"
      />
    </b-container>
  </div>
</template>

<script>
import { use } from "echarts/core";

// import { CanvasRenderer } from "echarts/renderers";
// import { GraphChart } from "echarts/charts";
// import {
//   TitleComponent,
//   TooltipComponent,
//   LegendComponent,
// } from "echarts/components";
// import VChart, { THEME_KEY } from "vue-echarts";
import VChart from "vue-echarts";

// import * as echarts from 'echarts/core';
import { TooltipComponent, LegendComponent } from "echarts/components";
import { GraphChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";

use([TooltipComponent, LegendComponent, GraphChart, CanvasRenderer]);

// use([
//   CanvasRenderer,
//   GraphChart,
//   TitleComponent,
//   TooltipComponent,
//   LegendComponent,
// ]);

export default {
  name: "WordEmbeddings",
  components: {
    VChart,
  },
  // provide: {
  //   [THEME_KEY]: "light",
  // },
  props: {
    page_title: String,
  },
  mounted() {
    // this.getGraph();
    window.vm = this;
    this.getGraph("refugee");
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
            // layout: "none",
            data: this.graph.nodes,
            links: this.graph.links,
            categories: this.graph.categories,
            roam: true,
            label: {
              show: true,
              position: "right",
              formatter: "{b}",
            },
            labelLayout: {
              hideOverlap: true,
            },
            scaleLimit: {
              min: 0.4,
              max: 2,
            },
            lineStyle: {
              normal: {
                color: "source",
                curveness: 0.3,
                width: 0.75,
                opacity: 0.5,
              },
              // emphasis: {
              //   focus: "adjacency",
              //   width: 5,
              //   opacity: 1,
              // },
            },
            focusNodeAdjacency: true,
            // itemStyle: {
            //   normal: {
            //     borderColor: "#fff",
            //     borderWidth: 1,
            //     shadowBlur: 10,
            //     shadowColor: "rgba(0, 0, 0, 0.3)",
            //   },
            //   emphasis: {
            //     focus: "adjacency",
            //     width: 5,
            //     opacity: 1,
            //     lineStyle: {
            //       width: 10,
            //     },
            //   },
            // },
            // emphasis: {
            //   focus: "adjacency",
            //   lineStyle: {
            //     width: 10,
            //   },
            // },
          },
        ],
        // series: [
        //   {
        //     name: "Les Miserables",
        //     type: "graph",
        //     layout: "none",
        //     data: this.graph.nodes,
        //     links: this.graph.links,
        //     categories: this.graph.categories,
        //     roam: true,
        //     label: {
        //       show: true,
        //       position: "right",
        //       formatter: "{b}",
        //     },
        //     labelLayout: {
        //       hideOverlap: true,
        //     },
        //     scaleLimit: {
        //       min: 0.4,
        //       max: 2,
        //     },
        //     lineStyle: {
        //       color: "source",
        //       curveness: 0.3,
        //     },
        //   },
        // ],
      };
    },
  },
  data() {
    return {
      navigator: window.navigator,
      api_link: null,
      graph: null,
      raw_text: "",
      related_words: [],
      loading: false,
    };
  },
  // data: function () {
  //   return {
  //     nlp_api_url: this.$config.nlp_api_url.word2vec + "/get_similar_words",
  //     related_words: [],
  //     raw_text: "",
  //     loading: true,
  //   };
  // },
  // mounted() {
  //   this.getRelatedWords();
  // },
  methods: {
    searchParams() {
      const params = new URLSearchParams();

      params.append("model_id", this.$config.default_model.word2vec.model_id);
      params.append("raw_text", this.text);
      params.append("topn_words", 8);
      params.append("topn_sub", 5);
      params.append("edge_thresh", 0.8);
      params.append("metric", "cosine_similarity");

      return params;
    },
    searchNode: function (event) {
      this.clicked_point = event;
      this.getGraph(this.clicked_point.data.name);
    },
    isHighlighted: function (action) {
      this.highlighted_point = action;
    },
    copyText() {
      this.navigator.clipboard.writeText(this.api_link);
    },
    getGraph: function (text = null) {
      this.loading = true;
      if (typeof text !== "string") {
        text = this.raw_text;
      } else {
        this.raw_text = text;
      }
      this.api_link = null;
      this.related_words = [];
      this.text = text;

      // const params = new URLSearchParams();

      // params.append("model_id", this.$config.default_model.word2vec.model_id);
      // params.append("raw_text", text);
      // params.append("topn_words", 8);
      // params.append("topn_sub", 5);
      // params.append("edge_thresh", 0.8);
      // params.append("metric", "cosine_similarity");

      // const body = {
      //   model_id: this.$config.default_model.word2vec.model_id,
      //   raw_text: text,
      //   topn_words: 8,
      //   topn_sub: 5,
      //   edge_thresh: 0.8,
      //   metric: "cosine_similarity",
      // };

      this.$http
        .get(this.$config.nlp_api_url.word2vec + "/get_similar_words_graph", {
          params: this.searchParams(),
        })
        .then((response) => {
          var graph = response.data.graph_data;
          this.related_words = response.data.similar_words;
          graph.nodes.forEach(function (node) {
            // node.label = {
            //   show: node.symbolSize > 5,
            // };
            node.draggable = true;
            // node.x = node.y = null;
          });
          this.graph = graph;

          this.api_link =
            location.origin +
            this.$config.nlp_api_url.word2vec +
            "/get_similar_words_graph" +
            "?" +
            this.searchParams().toLocaleString();
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
          this.loading = false;
        })
        .finally(() => {
          this.loading = false;
        });

      // this.$http
      //   .get("/static/data/les-miserables.json", body)
      //   .then((response) => {
      //     var graph = response.data;
      //     graph.nodes.forEach(function (node) {
      //       // node.label = {
      //       //   show: node.symbolSize > 5,
      //       // };
      //       node.draggable = true;
      //       // node.x = node.y = null;
      //     });
      //     this.graph = graph;
      //   })
      //   .catch((error) => {
      //     console.log(error);
      //     this.errored = true;
      //     this.loading = false;
      //   })
      //   .finally(() => {
      //     this.loading = false;
      //   });
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
