<template>
  <div id="content">
    <h1>{{ page_title }}</h1>
    <b-container fluid>
      <div
        v-show="plotReady"
        id="myPlotlyDiv"
        v-on:mouseover="stopAnimation"
        v-on:mouseleave="resumeAnimation"
        style="width: 100%; height: 100%"
      >
        <Plotly
          id="plotDiv"
          :data="plot_data"
          :layout="plot_layout"
          :display-mode-bar="false"
        ></Plotly>
      </div>
    </b-container>
  </div>
</template>

<script>
import { Plotly } from "vue-plotly";

var camZoom = -1;
var cnt = 0;

export default {
  name: "TopicRelationshipsVuePlotly",
  components: {
    Plotly,
  },
  props: {
    page_title: String,
  },
  data: function () {
    return {
      plotReady: false,

      // Animation variables
      stopMotion: false,
      WAIT: 1000 / 30, // 30fps
      dt: 0.2,
      rotScale: Math.PI / 60,

      // Plotly data and layout
      plot_data: [
        // {
        //   x: [1, 2, 3, 4],
        //   y: [10, 15, 13, 17],
        //   type: "scatter",
        // },
      ],
      plot_layout: {
        height: 800,
        autosize: true,
        xaxis: this.axisParams(),
        yaxis: this.axisParams(),
        zaxis: this.axisParams(),
        scene: {
          xaxis: this.sceneAxisParams(),
          yaxis: this.sceneAxisParams(),
          zaxis: this.sceneAxisParams(),
          camera: this.sceneCameraParams(),
        },
        title: "Word embedding space",
        margin: {
          r: 0,
          t: 25,
          b: 0,
          l: 0,
        },
      },
    };
  },
  mounted() {
    let vm = this;

    vm.$Plotly.d3.csv("/static/data/sample_embedding.csv", function (e, rows) {
      function unpack(rows, key) {
        return rows.map(function (row) {
          return row[key];
        });
      }
      vm.plot_data = [
        {
          x: unpack(rows, "x"),
          y: unpack(rows, "y"),
          z: unpack(rows, "z"),
          text: unpack(rows, "word"),
          mode: "markers",
          marker: {
            size: 2,
            color: unpack(rows, "cluster"),
            opacity: 0.6,
          },
          hoverinfo: "text",
          type: "scatter3d",
        },
      ];

      vm.$Plotly.relayout("plotDiv", vm.plot_layout).then(function () {
        vm.update(cnt);
        vm.plotReady = true;
      });
    });
  },
  methods: {
    sceneCameraParams: function () {
      return {
        up: {
          x: 0,
          y: 0,
          z: 1,
        },
        center: {
          x: 0,
          y: 0,
          z: 0,
        },
        eye: {
          x: Math.cos(cnt * this.rotScale) * camZoom,
          y: Math.sin(cnt * this.rotScale) * camZoom,
          z: Math.sin(cnt * this.rotScale) * camZoom,
        },
      };
    },

    axisParams: function () {
      return {
        autorange: true,
        showgrid: false,
        zeroline: false,
        showline: false,
        autotick: true,
        ticks: "",
        showticklabels: false,
        range: [-1, 1],
      };
    },

    sceneAxisParams: function () {
      return {
        autorange: true,
        showgrid: false,
        zeroline: false,
        showline: false,
        autotick: true,
        ticks: "",
        showticklabels: false,
        title: "",
        showspikes: false,
        range: [-1, 1],
      };
    },

    update: function (cnt) {
      let vm = this;

      console.log("Update motion");

      cnt = cnt + vm.dt;
      window.cnt = cnt;

      if (vm.stopMotion) return;

      setTimeout(function () {
        var plotDiv = document.getElementById("plotDiv");
        var layout = plotDiv.layout;
        var z = layout.scene.camera.eye.z;

        layout.scene.camera.eye = {
          x: Math.cos(cnt * vm.rotScale) * camZoom,
          y: Math.sin(cnt * vm.rotScale) * camZoom,
          z: z,
        };

        vm.$Plotly.relayout("plotDiv", layout).then(function () {
          vm.update(cnt);
        });
      }, vm.WAIT);
    },

    stopAnimation: function () {
      console.log("Stop motion");
      this.stopMotion = true;
    },

    resumeAnimation: function () {
      let vm = this;
      console.log("Start motion");
      vm.stopMotion = false;

      var plotDiv = document.getElementById("plotDiv");
      var layout = plotDiv.layout;
      // var layout = this.plot_layout;

      var x = layout.scene.camera.eye.x;
      var y = layout.scene.camera.eye.y;
      var z = layout.scene.camera.eye.z;

      var atan = Math.atan(y / x);
      var cnt = atan / vm.rotScale;
      var camZoom = x / Math.cos(cnt * vm.rotScale);

      layout.scene.camera.eye = {
        x: Math.cos(cnt * vm.rotScale) * camZoom,
        y: Math.sin(cnt * vm.rotScale) * camZoom,
        z: z,
      };

      vm.$Plotly.relayout("plotDiv", layout).then(function () {
        vm.update(cnt);
      });
    },
  },
};
</script>
