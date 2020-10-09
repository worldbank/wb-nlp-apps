<template>
  <div class="hello">
    <h1>{{ page_title }}</h1>
    <br />

    <b-container fluid>
      <b-row>
        <b-col cols="9" class="border-right">
          Word2vec is a simple embedding model.
          <Plotly
            :data="data"
            :layout="layout"
            :display-mode-bar="false"
          ></Plotly>
        </b-col>
        <b-col cols="3">
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
          <h4>Similar words</h4>

          <b-skeleton
            v-show="loading"
            animation="wave"
            width="85%"
          ></b-skeleton>
          <b-list-group v-show="!loading" flush>
            <b-list-group-item
              v-for="related_word in related_words"
              :key="related_word.word"
            >
              {{ related_word.word }}
            </b-list-group-item>
          </b-list-group></b-col
        >
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { Plotly } from "vue-plotly";

export default {
  name: "TopicProfiles",
  components: {
    Plotly,
  },
  props: {
    page_title: String,
  },
  data: function () {
    // http://10.0.0.25:8880/api/related_words?raw_text=poverty&model_id=ALL_50
    return {
      // api_url: "http://10.0.0.25:8880/api/related_words",
      api_url: "/api/related_words",
      related_words: [],
      raw_text: "",
      loading: true,
      // Plotly data and layout
      data: [
        {
          x: [1, 2, 3, 4],
          y: [10, 15, 13, 17],
          type: "scatter",
        },
      ],
      layout: {
        title: "My graph",
      },
    };
  },
  mounted() {
    this.getRelatedWords();
  },
  methods: {
    getRelatedWords: function () {
      this.loading = true;
      this.$http
        .get(this.api_url + "?model_id=ALL_50&raw_text=" + this.raw_text)
        .then((response) => {
          this.related_words = response.data.words;
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
        })
        .finally(() => (this.loading = false));
    },
    // plotStack: function (topic_shares) {
    //   this.topic_share_plot_ready = false;

    //   keys = Object.keys(topic_shares);
    //   traces = [];

    //   ph = 200.0;
    //   ps = 20.0;

    //   height = ph * keys.length + ps * (keys.length - 1);
    //   div_dt = ps / height;
    //   panel_dt = ph / height;

    //   var layout = {
    //     title: "Topic share per document group",
    //     xaxis: { domain: [0, 1], title: "Year" },
    //     // yaxis: {domain: [0, 0.325]},
    //     // yaxis2: {domain: [0.35, 0.675]},
    //     // yaxis3: {domain: [0.7, 1]},
    //     // yaxis4: {domain: [0.85, 1]},
    //     height: height,
    //     // xaxis4: {
    //     //   domain: [0.55, 1],
    //     //   anchor: 'y4'
    //     // },
    //     // xaxis2: {domain: [0.55, 1]},
    //     // yaxis3: {domain: [0.55, 1]},
    //     // yaxis4: {
    //     //   domain: [0.55, 1],
    //     //   anchor: 'x4'
    //     // }
    //     autosize: true,
    //   };

    //   Plotly.newPlot("myDiv", traces, layout);

    //   ix = 1;
    //   yd_start = 0;
    //   yd_end = yd_start + panel_dt;
    //   max_y = 0;

    //   for (name in topic_shares) {
    //     (y = topic_shares[name].map(function (x) {
    //       return x.topic_share;
    //     })),
    //       (y_max = Math.max.apply(null, y));

    //     if (y_max > max_y) {
    //       max_y = y_max;
    //     }

    //     tr = {
    //       x: topic_shares[name].map(function (x) {
    //         return x.year;
    //       }),
    //       y: y,
    //       name: name,
    //       type: "bar",
    //     };
    //     if (ix > 1) {
    //       tr.xaxis = "x";
    //       tr.yaxis = "y" + ix;
    //     }

    //     traces.push(tr);
    //     ix += 1;
    //   }

    //   for (ix = 1; ix <= keys.length; ix++) {
    //     if (ix > 1) {
    //       layout["yaxis" + ix] = {
    //         domain: [yd_start, yd_end],
    //         range: [0, max_y],
    //       };
    //     } else {
    //       layout.yaxis = { domain: [yd_start, yd_end], range: [0, max_y] };
    //     }

    //     yd_start = yd_end + div_dt;
    //     yd_end = yd_start + panel_dt;
    //   }

    //   layout.legend = { orientation: "h", x: 0, y: 1 };

    //   Plotly.newPlot("myDiv", traces, layout);

    //   // myPlot = document.getElementById('myDiv');
    //   // myPlot.on('plotly_afterplot', function() {
    //   //   this.topic_share_plot_ready = true;
    //   // });

    //   // Make the plotly responsive
    //   // https://gist.github.com/aerispaha/63bb83208e6728188a4ee701d2b25ad5
    //   this.makeResponsive();

    //   this.topic_share_plot_ready = true;
    //   return true;
    // },
    // makeResponsive: function () {
    //   var d3 = Plotly.d3;
    //   var WIDTH_IN_PERCENT_OF_PARENT = 100,
    //     HEIGHT_IN_PERCENT_OF_PARENT = 100;

    //   var gd3 = d3.selectAll(".responsive-plot").style({
    //     width: WIDTH_IN_PERCENT_OF_PARENT + "%",
    //     "margin-left": (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + "%",

    //     height: HEIGHT_IN_PERCENT_OF_PARENT + "vh",
    //     "margin-top": (100 - HEIGHT_IN_PERCENT_OF_PARENT) / 2 + "vh",
    //   });

    //   var nodes_to_resize = gd3[0]; //not sure why but the goods are within a nested array

    //   // Important to run this explicitly here to fix some weird resizing behavior.
    //   (function () {
    //     for (var i = 0; i < nodes_to_resize.length; i++) {
    //       Plotly.Plots.resize(nodes_to_resize[i]);
    //     }
    //   })();

    //   window.onresize = function () {
    //     for (var i = 0; i < nodes_to_resize.length; i++) {
    //       Plotly.Plots.resize(nodes_to_resize[i]);
    //     }
    //   };
    // },
    // topicShareActiveToggle: function (topic_share_active, topic_map_active) {
    //   if (topic_share_active == this.topic_share_active) {
    //     return;
    //   } else {
    //     this.topic_share_active = topic_share_active;
    //     this.topicMapActiveToggle(topic_map_active, this.topic_share_active);
    //   }
    // },
    // topicMapActiveToggle: function (topic_map_active, topic_share_active) {
    //   if (topic_map_active == this.topic_map_active) {
    //     return;
    //   } else {
    //     this.topic_map_active = topic_map_active;
    //     this.topicShareActiveToggle(topic_share_active, this.topic_map_active);
    //   }
    // },
    // togglePanels: function (topic_map_active, topic_share_active) {
    //   this.topicShareActiveToggle(topic_share_active, topic_map_active);
    //   this.topicMapActiveToggle(topic_map_active, topic_share_active);
    // },
    // findTopicShare: function (topic_id, model_id, corpus_id) {
    //   let vm = this;
    //   this.topic_share_searching = true;
    //   this.topic_share_plot_ready = false;

    //   options = {
    //     corpus_id: this.corpus_id,
    //     model_id: this.lda_model_id,
    //     topic_id: this.topic_id,
    //     year_start: 1960,
    //     adm_regions: this.topic_share_selected_adm_regions,
    //     major_doc_types: this.topic_share_selected_doc_types,
    //     lending_instruments: this.topic_share_selected_lending_instruments,
    //   };

    //   $.ajax({
    //     url:
    //       this.api_base_url +
    //       "lda_compare_partition_topic_share" +
    //       "?" +
    //       $.param(options, true),
    //     // data: options,
    //     processData: false,
    //     type: "POST",
    //     method: "POST",
    //     contentType: false,
    //     success: function (data) {
    //       if ("topic_shares" in data) {
    //         vm.topic_shares = data.topic_shares;
    //       }
    //       if ("topic_words" in data) {
    //         vm.topic_words = data.topic_words;
    //       }
    //       console.log(data);
    //     },
    //     error: function (e) {
    //       console.log(e);
    //       vm.errors.push(e);
    //       vm.topic_share_searching = false;
    //     },
    //   }).done(function () {
    //     vm.topic_share_searching = false;
    //     vm.plotStack(vm.topic_shares);
    //   });
    // },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
