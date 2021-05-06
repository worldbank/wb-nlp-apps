<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      <p>
        Our focus on development issues and on publications and documents
        originating from development agencies implies that the majority of
        documents in our corpus relate to low and middle-income countries. But
        not all documents are country-specific and some cover, in part or in
        full, high-income countries. To assess the geographic coverage of the
        corpus and of its components, we cannot exclusively rely on metadata
        that may be provided by the source websites (the World Bank for example
        provides information on “Region” and “Country” for most of its
        documents).
      </p>
      <p>
        To obtain an estimate of country coverage, we count the number of times
        each country is mentioned in each document. This count is a simple word
        search based on a lookup list of country names (which includes multiple
        ways a country name can be spelled out; script and lookup file available
        <a href="#">here</a>). The counts are added to each document’s metadata.
        Combined with the information on the documents’ publication date and
        origin, this information allows us to generate aggregated counts by
        country and year (available <a href="#">here</a>), displayed in the
        following map.
      </p>

      <h4>Extracted countries timeseries</h4>
      <br />
      <b-row>
        <b-col cols="12"
          ><p>Filter data by document type for map and race chart</p></b-col
        >
        <b-col cols="4">
          <b-form-select
            v-model="doc_type_filter"
            :options="doc_type_options"
            size="sm"
          ></b-form-select>
        </b-col>
      </b-row>
      <br />
      <b-row>
        <b-col cols="8" offset="0">
          <p>Toggle map view</p>
          <b-form-radio-group
            v-model="map_type"
            value-field="item"
            text-field="name"
            :options="group_value_options"
        /></b-col>
      </b-row>
      <br />

      <b-skeleton-img
        v-if="
          country_stats_loading ||
          $refs.countryVolumeMap === $refs.countryShareMap
        "
        height="350px"
      ></b-skeleton-img>
      <div v-if="!country_stats_loading">
        <div v-show="$refs.countryVolumeMap !== $refs.countryShareMap">
          <div v-show="map_type === 'volume' && map_ready">
            <AnimatedMapChartWB
              v-if="timeseriesCountryDataVolume"
              :partition_type="doc_type_filter"
              :timeseriesCountryData="timeseriesCountryDataVolume"
              :pause_loop="map_type !== 'volume'"
              ref="countryVolumeMap"
              key="volume-c"
              highColor="#0000ff"
              lowColor="#efefff"
              countryStrokeColor="#909090"
              defaultCountryFillColor="#fff"
              @ready="(ready) => (map_ready = ready)"
              @mounted="$refs.countryVolumeMap.startAnimation()"
            />
            <br />
            <br />
          </div>
          <div v-show="map_type === 'share' && map_ready">
            <AnimatedMapChartWB
              v-if="timeseriesCountryDataShare"
              :partition_type="doc_type_filter"
              :timeseriesCountryData="timeseriesCountryDataShare"
              :pause_loop="map_type !== 'share'"
              ref="countryShareMap"
              key="share-c"
              highColor="#0000ff"
              lowColor="#efefff"
              countryStrokeColor="#909090"
              defaultCountryFillColor="#fff"
              @ready="(ready) => (map_ready = ready)"
              @mounted="$refs.countryShareMap.startAnimation()"
            />
            <br />
            <br />
          </div>
        </div>
      </div>

      <p v-if="countries_volume" class="lead">
        We also show a race chart of the cumulative country mentions in
        documents. This animated chart provides a glimpse on how countries'
        popularity, as measured by the total frequency of mentions, evolve over
        time.
      </p>
      <b-skeleton-img
        v-if="
          !race_ready || $refs.raceChart === undefined || country_stats_loading
        "
        height="500px"
      ></b-skeleton-img>

      <div v-if="countries_volume">
        <RaceChart
          v-if="!country_stats_loading"
          :title="doc_type_filter"
          :iso3map="iso3map"
          ref="raceChart"
          :input_data="countries_volume.records"
          @ready="(ready) => (race_ready = ready)"
        />
        <br />
        <br />
      </div>

      <p class="lead">
        The World Bank corpus contains metadata on the administrative and
        geographic regions that is relevant to documents. The charts below use
        these metadata to show insights on the relative popularity of regions
        over time within the World Bank corpus.
      </p>
      <br />
      <VolumeChart
        v-if="adm_region"
        :data="adm_region"
        :field="adm_region.field"
        field_name="admin regions"
      />
      <br />
      <br />

      <VolumeChart
        v-if="geo_region"
        :data="geo_region"
        :field="geo_region.field"
        field_name="geographic regions"
      />
      <br />
      <br />

      <!-- <div id="mapDiv" /> -->
    </div>
  </div>
</template>

<script>
import AnimatedMapChartWB from "../../common/AnimatedMapChartWB";
import VolumeChart from "../../common/VolumeChart";
import RaceChart from "../../common/RaceChart";

export default {
  name: "GeographicCoverage",
  props: {
    page_title: String,
  },
  components: {
    VolumeChart,
    AnimatedMapChartWB,
    RaceChart,
  },
  data: function () {
    return {
      map_type: "volume",
      race_ready: false,
      map_ready: false,
      data_cache: {},

      group_value_options: [
        { item: "volume", name: "By volume" },
        { item: "share", name: "By share" },
      ],

      doc_type_options: [
        { value: "Full corpus", text: "Full corpus" },
        { value: "WB - Board Documents", text: "WB - Board Documents" },
        {
          value: "WB - Economic and Sector Work",
          text: "WB - Economic and Sector Work",
        },
        { value: "WB - Project Documents", text: "WB - Project Documents" },
        { value: "WB - Publications", text: "WB - Publications" },
        {
          value: "WB - Publications and Research",
          text: "WB - Publications and Research",
        },
      ],
      doc_type_filter: "Full corpus",

      country_stats_loading: false,
      loading: false,

      date_now: new Date().toDateString(),
      corpus_size: 200000,
      org_count: 14,
      total_tokens: 1029000000,

      adm_region: null,
      geo_region: null,

      countries_volume: null,
      countries_share: null,

      iso3map: {},
      privateCountryData: null,
      timeseriesCountryDataVolume: null,
      timeseriesCountryDataShare: null,
    };
  },
  mounted() {
    window.gvm = this;
    this.getISOInfo();
    // this.findTopicMap();
    this.getFullCorpusData();

    // this.getExtractedCountriesStats();
  },
  methods: {
    getFullCorpusData: function () {
      this.loading = true;

      const params = new URLSearchParams();
      params.append("fields", "adm_region");
      params.append("fields", "geo_region");

      this.$http
        .get(this.$config.corpus_url + "/get_corpus_volume_by", {
          params: params,
        })
        .then((response) => {
          let data = response.data;

          this.adm_region = data.adm_region;
          this.geo_region = data.geo_region;

          this.loading = false;
        })

        .finally(() => {});
    },
    getExtractedCountriesStats: function () {
      if (!this.iso3map) {
        return;
      }

      this.countries_volume = {};
      this.countries_share = {};
      this.country_stats_loading = true;

      const searchParams = new URLSearchParams();
      searchParams.append(
        "major_doc_type",
        this.doc_type_filter === "Full corpus"
          ? ""
          : this.doc_type_filter.replace(/WB - /g, "")
      );
      const data_key = searchParams.toLocaleString();
      console.log(data_key);

      if (this.data_cache[data_key]) {
        let data = this.data_cache[data_key];

        this.countries_volume = data.volume;
        this.countries_share = data.share;

        this.country_stats_loading = false;

        return;
      }

      this.$http
        .get(this.$config.corpus_url + "/get_extracted_countries_stats", {
          params: searchParams,
        })
        .then((response) => {
          let data = response.data;

          this.countries_volume = data.volume;
          this.countries_share = data.share;

          this.data_cache[data_key] = {
            volume: data.volume,
            share: data.share,
          };

          this.country_stats_loading = false;
        })

        .finally(() => {});
    },
    countryData() {
      this.timeseriesCountryDataVolume = null;
      if (this.iso3map === null) {
        this.getISOInfo();
      } else {
        this.setCountryData();
      }

      return this.timeseriesCountryDataVolume;
    },
    setCountryData(timeseries, target) {
      // timeseries = this.countries_volume.year
      // target = this.timeseriesCountryDataVolume

      if (timeseries === null || timeseries === undefined) {
        return;
      }

      for (const [year, series] of Object.entries(timeseries)) {
        var dataSeries = {};

        for (const [code, value] of Object.entries(series)) {
          if (this.iso3map[code] !== undefined) {
            dataSeries[this.iso3map[code]["alpha-2"]] = value;
          }
        }

        target[year] = dataSeries;
      }
    },
    getISOInfo() {
      this.$http
        .get("/static/data/iso3166-3-country-info.json")
        .then((response) => {
          this.iso3map = response.data;

          // if (this.timeseriesCountryDataVolume === null) {
          //   this.setCountryData();
          // }
        });
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
  watch: {
    doc_type_filter() {
      this.getExtractedCountriesStats();
    },
    countries_volume() {
      if (this.countries_volume !== null) {
        // this.countryData();
        this.timeseriesCountryDataVolume = {};

        this.setCountryData(
          this.countries_volume.year,
          this.timeseriesCountryDataVolume
        );
      }
    },
    countries_share() {
      if (this.countries_share !== null) {
        // this.countryData();
        this.timeseriesCountryDataShare = {};

        this.setCountryData(
          this.countries_share.year,
          this.timeseriesCountryDataShare
        );
      }
    },
    iso3map() {
      if (Object.keys(this.iso3map).length > 0) {
        this.getExtractedCountriesStats();
      }
    },

    country_stats_loading() {
      if (!this.country_stats_loading) {
        console.log("Data updated!!!");

        if (this.$refs.countryVolumeMap) {
          this.$refs.countryVolumeMap.clearQueue();

          this.$refs.countryVolumeMap.timeseriesCountryData = this.timeseriesCountryDataVolume;
        }

        if (this.$refs.countryShareMap) {
          this.$refs.countryShareMap.clearQueue();

          this.$refs.countryShareMap.timeseriesCountryData = this.timeseriesCountryDataShare;
        }
        // this.$refs.countryVolumeMap.startAnimation();
        // this.$refs.countryShareMap.startAnimation();
      }
    },

    // <div v-if="!country_stats_loading">
    //   <div v-show="map_type === 'volume'">
    //     <AnimatedMapChartWB
    //       v-if="timeseriesCountryDataVolume"
    //       :timeseriesCountryData="timeseriesCountryDataVolume"
    //       :pause_loop="map_type !== 'volume'"
    //       ref="countryVolumeMap"
    //       key="volume-c"
    //       highColor="#0000ff"
    //       lowColor="#efefff"
    //       countryStrokeColor="#909090"
    //       defaultCountryFillColor="#fff"
    //       @ready="(ready) => (map_ready = ready)"
    //     />
    //     <br />
    //     <br />
    //   </div>
    //   <div v-show="map_type === 'share'">
    //     <AnimatedMapChartWB
    //       v-if="timeseriesCountryDataShare"
    //       :timeseriesCountryData="timeseriesCountryDataShare"
    //       :pause_loop="map_type !== 'share'"
    //       ref="countryShareMap"
    //       key="share-c"
    //       highColor="#0000ff"
    //       lowColor="#efefff"
    //       countryStrokeColor="#909090"
    //       defaultCountryFillColor="#fff"
    //     />
    //     <br />
    //     <br />
    //   </div>
    // </div>

    // country_stats_loading() {
    //   if (this.country_stats_loading === false) {
    //     this.timeseriesCountryDataVolume = {};
    //     this.timeseriesCountryDataShare = {};

    //     this.setCountryData(
    //       this.countries_volume,
    //       this.timeseriesCountryDataVolume
    //     );
    //     this.setCountryData(
    //       this.countries_share,
    //       this.timeseriesCountryDataShare
    //     );
    //   }
    // },
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
