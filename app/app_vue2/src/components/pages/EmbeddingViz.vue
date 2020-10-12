<template>
  <div>
    <h1>{{ page_title }}</h1>
    <b-container fluid>
      <div
        v-show="plotReady"
        id="myPlotlyDiv"
        v-on:mouseover="stopAnimation"
        v-on:mouseleave="resumeAnimation"
        v-on:touchenter="stopAnimation"
        v-on:touchleave="resumeAnimation"
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

var cnt = 1;

export default {
  name: "EmbeddingViz",
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
      WAIT: 1000 / 120, // 30fps
      dt: 0.5, // from 0.2
      camZoom: -1,
      rotScale: Math.PI / 120,
      distanceSensitiveMarker: false,

      // Plotly data and layout
      plot_data: [],
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
      cluster_color_map: {},
      data_cluster: [],
    };
  },
  mounted() {
    let vm = this;

    // https://plotly.com/javascript/plotlyjs-events/#hover-event

    vm.$Plotly.d3.csv("/static/data/sample_embedding.csv", function (e, rows) {
      function unpack(rows, key) {
        return rows.map(function (row) {
          return row[key];
        });
      }

      vm.data_cluster = unpack(rows, "cluster");

      var marker_colors = [];
      for (var i = 0; i < vm.data_cluster.length; ++i) {
        var ix = vm.data_cluster[i];
        marker_colors.push(vm.getRGBAFromCluster(ix));
      }

      vm.plot_data = [
        {
          x: unpack(rows, "x"),
          y: unpack(rows, "y"),
          z: unpack(rows, "z"),
          text: unpack(rows, "word"),
          mode: "markers",
          marker: {
            size: 7,
            color: marker_colors,
            opacity: 0.6,
          },
          hoverinfo: "text",
          type: "scatter3d",
        },
      ];

      console.log(vm.plot_layout.scene.camera);

      vm.$Plotly.relayout("plotDiv", vm.plot_layout).then(function () {
        vm.update(cnt);
        vm.plotReady = true;
      });
    });
  },
  methods: {
    getRandomColor: function (a = 1) {
      var r = Math.floor(Math.random() * 256).toString();
      var g = Math.floor(Math.random() * 256).toString();
      var b = Math.floor(Math.random() * 256).toString();

      return { r: r, g: g, b: b, a: a };
    },
    getRGBAFromCluster: function (cluster, a = 1) {
      if (!(cluster in this.cluster_color_map)) {
        this.cluster_color_map[cluster] = this.getRandomColor(a);
      }
      var cluster_color = this.cluster_color_map[cluster];

      return (
        "rgba(" +
        cluster_color.r +
        ", " +
        cluster_color.g +
        ", " +
        cluster_color.b +
        ", " +
        a +
        ")"
      );
    },
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
          x: Math.cos(cnt * this.rotScale) * this.camZoom,
          y: Math.sin(cnt * this.rotScale) * this.camZoom,
          z: 1,
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
    computeDataDist: function (data, x, y, z) {
      // This function computes the distance of the data points to some vector.
      // Based on the distance, update the color opacity of the marker.
      var dist = [];
      var min_dist = Infinity;
      var max_dist = 0;
      for (var i = 0; i < data.x.length; ++i) {
        var p_dist =
          Math.pow(x - data.x[i], 2) +
          Math.pow(y - data.y[i], 2) +
          Math.pow(z - data.z[i], 2);
        dist.push(p_dist);
        if (p_dist > max_dist) {
          max_dist = p_dist;
        }
        if (p_dist < min_dist) {
          min_dist = p_dist;
        }
      }

      var normed_dist = [];
      for (var j = 0; j < dist.length; ++j) {
        var nd = (dist[j] - min_dist) / (max_dist - min_dist);
        var n_dist = 1 - nd;
        if (nd > 0.8) {
          n_dist = 0.5;
        }
        // else {
        //   n_dist = 0.8;
        // }
        normed_dist.push(this.getRGBAFromCluster(this.data_cluster[j], n_dist));
      }

      return normed_dist;
    },
    update: function (cnt) {
      let vm = this;

      console.log("Update motion");

      cnt = cnt + vm.dt;
      window.cnt = cnt;

      if (vm.stopMotion) return;

      setTimeout(function () {
        var plotUpdates = vm.computeLayoutUpdates(false, cnt);

        vm.$Plotly
          .relayout("plotDiv", plotUpdates.layout_update)
          .then(function () {
            if (vm.distanceSensitiveMarker) {
              vm.$Plotly
                .restyle("plotDiv", plotUpdates.trace_update)
                .then(function () {
                  vm.update(plotUpdates.cnt);
                });
            } else {
              vm.update(plotUpdates.cnt);
            }
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

      var plotUpdates = vm.computeLayoutUpdates(true);

      vm.$Plotly
        .relayout("plotDiv", plotUpdates.layout_update)
        .then(function () {
          if (vm.distanceSensitiveMarker) {
            vm.$Plotly
              .restyle("plotDiv", plotUpdates.trace_update)
              .then(function () {
                vm.update(plotUpdates.cnt);
              });
          } else {
            vm.update(plotUpdates.cnt);
          }
        });
    },
    computeLayoutUpdates: function (is_resume, cnt = 0) {
      let vm = this;

      var plotDiv = document.getElementById("plotDiv");
      var layout = plotDiv.layout;

      var data = plotDiv.data[0];
      var x = layout.scene.camera.eye.x;
      var y = layout.scene.camera.eye.y;
      var z = layout.scene.camera.eye.z;

      if (is_resume) {
        var atan = Math.atan(y / x);
        cnt = atan / vm.rotScale;
        vm.camZoom = x / Math.cos(cnt * vm.rotScale);

        layout.scene.camera.eye = {
          x: Math.cos(cnt * vm.rotScale) * vm.camZoom,
          y: Math.sin(cnt * vm.rotScale) * vm.camZoom,
          z: z,
        };
      } else {
        z = layout.scene.camera.eye.z;
        x = Math.cos(cnt * vm.rotScale) * vm.camZoom;
        y = Math.sin(cnt * vm.rotScale) * vm.camZoom;

        layout.scene.camera.eye = {
          x: x,
          y: y,
          z: z,
        };
      }

      return {
        layout_update: layout,
        // Markers with opacity are not rendering based on depth...
        // https://community.plotly.com/t/weird-marker-overlapping-using-scatter3d-and-opacity-1/20931
        // https://github.com/plotly/plotly.js/issues/1267
        // NOTE: If fixed, enable feature using distanceSensitiveMarker=true;
        trace_update: {
          marker: { color: vm.computeDataDist(data, x, y, z) },
        },
        cnt: cnt,
      };
    },
  },
};
</script>
