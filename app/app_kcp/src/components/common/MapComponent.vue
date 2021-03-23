<template>
  <div id="mapDiv" />
</template>

<script>
// import { Plotly } from "vue-plotly";

// import map_methods from "../../../js/maps";
export default {
  name: "GeographicCoverage",
  props: {
    page_title: String,
  },
  data: function () {
    return {
      date_now: new Date().toDateString(),
      corpus_size: 200000,
      org_count: 14,
      total_tokens: 1029000000,
    };
  },
  mounted() {
    // this.findTopicMap();
    this.buildMap();
  },
  methods: {
    buildMap() {
      let vm = this;
      vm.$Plotly.d3.csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv",
        function (err, rows) {
          console.log(err);
          function unpack(rows, key) {
            return rows.map(function (row) {
              return row[key];
            });
          }

          var data = [
            {
              type: "choropleth",
              locations: unpack(rows, "CODE"),
              z: unpack(rows, "GDP (BILLIONS)"),
              text: unpack(rows, "COUNTRY"),
              colorscale: [
                [0, "rgb(5, 10, 172)"],
                [0.35, "rgb(40, 60, 190)"],
                [0.5, "rgb(70, 100, 245)"],
                [0.6, "rgb(90, 120, 245)"],
                [0.7, "rgb(106, 137, 247)"],
                [1, "rgb(220, 220, 220)"],
              ],
              autocolorscale: false,
              reversescale: true,
              marker: {
                line: {
                  color: "rgb(180,180,180)",
                  width: 0.5,
                },
              },
              tick0: 0,
              zmin: 0,
              dtick: 1000,
              colorbar: {
                autotic: false,
                tickprefix: "$",
                title: "GDP<br>Billions US$",
              },
            },
          ];

          var layout = {
            title:
              '2014 Global GDP<br>Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html"> CIA World Factbook</a>',
            geo: {
              showframe: false,
              showcoastlines: false,
              projection: {
                type: "mercator",
              },
            },
            height: 600,
            width: 900,
            margin: {
              l: 0,
              r: 0,
              b: 0,
              t: 0,
              pad: 2,
            },
          };
          vm.$Plotly.newPlot("mapDiv", data, layout, { showLink: false });
        }
      );
    },
    findTopicMap: function (
      csvFile = "/static/data/country_popularity.csv",
      divID = "mapDiv"
    ) {
      let vm = this;

      vm.$Plotly.d3.csv(csvFile, function (err, data) {
        // Create a lookup table to sort and regroup the columns of data,
        // first by year, then by continent:
        var mapr = (document.mapr = {});

        function getMapr(year) {
          var mapTrace;
          if (!(mapTrace = mapr[year])) {
            mapTrace = mapr[year] = {
              // type: 'choropleth',
              // name: year,
              locations: [],
              z: [],
              text: [],
            };
          }
          return mapTrace;
        }

        var i = 0;

        // Go through each row, get the right trace, and append the data:
        for (i = 0; i < data.length; i++) {
          var datum = data[i];
          var mapTrace = getMapr(datum.year);
          mapTrace.locations.push(datum.iso_alpha);
          mapTrace.z.push(datum.popularity);
          mapTrace.text.push(datum.country);
        }

        // Get the group names:
        var years = Object.keys(mapr);
        var traces = [];
        i = 0;

        traces.push({
          type: "choropleth",
          name: years[i],
          locations: mapr[years[i]].locations.slice(),
          z: mapr[years[i]].z.slice(),
          text: mapr[years[i]].text.slice(),
          colorscale: [
            [0, "rgb(5, 10, 172)"],
            [0.35, "rgb(40, 60, 190)"],
            [0.5, "rgb(70, 100, 245)"],
            [0.6, "rgb(90, 120, 245)"],
            [0.7, "rgb(106, 137, 247)"],
            [1, "rgb(220, 220, 220)"],
          ],
          reversescale: true,
          marker: {
            line: {
              color: "rgb(180,180,180)",
              width: 0.5,
            },
          },
          tick0: 0,
          zmin: 0,
          dtick: 1000,
          colorbar: {
            thickness: 10,
            autotic: false,
            tickprefix: "",
            len: 0.3,
            x: 0.9,
            y: 0.7,
            title: "Documents",
          },
        });

        var frames = [];
        for (i = 0; i < years.length; i++) {
          frames.push({
            name: years[i],
            data: [
              {
                locations: mapr[years[i]].locations.slice(),
                z: mapr[years[i]].z.slice(),
                text: mapr[years[i]].text.slice(),
                type: "choropleth",
              },
            ],
          });
        }

        // Now create slider steps, one for each frame. The slider
        // executes a plotly.js API command (here, Plotly.animate).
        // In this example, we'll animate to one of the named frames
        // created in the above loop.
        var sliderSteps = [];
        for (i = 0; i < years.length; i++) {
          sliderSteps.push({
            method: "animate",
            label: years[i],
            args: [
              [years[i]],
              {
                mode: "immediate",
                transition: {
                  duration: 300,
                },
                frame: {
                  duration: 500,
                  redraw: true,
                },
              },
            ],
          });
        }

        var layout = {
          title: "Popularity of countries in World Bank documents over time",
          geo: {
            showframe: true,
            showcoastlines: false,
            projection: {
              type: "natural earth", //'miller'
            },
          },
          height: 600,
          hovermode: "closest",
          // We'll use updatemenus (whose functionality includes menus as
          // well as buttons) to create a play button and a pause button.
          // The play button works by passing `null`, which indicates that
          // Plotly should animate all frames. The pause button works by
          // passing `[null]`, which indicates we'd like to interrupt any
          // currently running animations with a new list of frames. Here
          // The new list of frames is empty, so it halts the animation.
          updatemenus: [
            {
              x: 0,
              y: 0,
              yanchor: "top",
              xanchor: "left",
              showactive: true,
              direction: "left",
              type: "buttons",
              pad: {
                t: 30,
                r: 10,
              },
              buttons: [
                {
                  method: "animate",
                  args: [
                    null,
                    {
                      mode: "immediate",
                      fromcurrent: true,
                      transition: {
                        duration: 300,
                      },
                      frame: {
                        duration: 500,
                        redraw: true,
                      },
                    },
                  ],
                  label: "Play",
                },
                {
                  method: "animate",
                  args: [
                    [null],
                    {
                      mode: "immediate",
                      transition: {
                        duration: 100,
                      },
                      frame: {
                        duration: 100,
                        redraw: true,
                      },
                    },
                  ],
                  label: "Pause",
                },
              ],
            },
          ],
          // Finally, add the slider and use `pad` to position it
          // nicely next to the buttons.
          sliders: [
            {
              pad: {
                l: 130,
                t: 0,
              },
              currentvalue: {
                visible: true,
                prefix: "Year:",
                xanchor: "right",
                font: {
                  size: 20,
                  color: "#666",
                },
              },
              steps: sliderSteps,
            },
          ],
        };

        // Create the plot:
        vm.$Plotly.newPlot(divID, {
          data: traces,
          layout: layout,
          config: {
            showSendToCloud: true,
          },
          frames: frames,
        });
      });

      // this.makeResponsive();
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* h3 {
  margin: 40px 0 0;
} */
/* a {
  color: #42b983;
} */
</style>
