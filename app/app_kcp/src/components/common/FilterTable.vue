<template>
  <div>
    <h3 class="mb-3 mt-5">Choose a topic model</h3>
    <MLModelSelect
      @modelSelected="onModelSelect"
      :model_name="model_name"
      placeholder="Choose topic model..."
    />
    <div v-if="loading" class="d-flex justify-content-center">
      <b-spinner
        style="margin: 20px"
        variant="primary"
        label="Spinning"
      ></b-spinner>
    </div>
    <div v-show="model_run_info_id && rows.length > 0">
      <h3 class="mb-3 mt-5">Available topics</h3>
      <p class="mt-2">
        Scroll for more topics. You may also use the search box below to narrow
        down the topics list. You can choose up to three topics.
      </p>
      <input
        type="text"
        placeholder="Filter topic by keywords"
        v-model="filter"
      />

      <div class="table-wrapper">
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th>
                <div class="custom-control custom-checkbox">
                  <input
                    v-on:click="clearTopicSelect"
                    :checked="topicSelected"
                    type="checkbox"
                    class="custom-control-input"
                    id="globalTopicFilterSelect"
                  />
                  <label
                    class="custom-control-label"
                    for="globalTopicFilterSelect"
                  >
                    Topic
                  </label>
                </div>
              </th>
              <th>Keywords</th>
            </tr>
          </thead>
          <tbody v-if="rows.length > 0">
            <tr
              v-for="(row, index) in filteredRows"
              :key="`topic_word-${index}`"
            >
              <th scope="row">
                <div class="custom-control custom-checkbox">
                  <input
                    v-on:click="initOrRemoveTopicValue(row.topic_id, $event)"
                    type="checkbox"
                    class="custom-control-input"
                    :id="'topicSelect_' + index"
                    checked=""
                    :value="row.topic_id"
                    v-model="selected_topic"
                    :disabled="disableSelect(row.topic_id)"
                  />
                  <label
                    class="custom-control-label topic-label"
                    :for="'topicSelect_' + index"
                    >{{ row.topic_label }}</label
                  >
                </div>
              </th>
              <td
                class="keywords-class"
                v-html="
                  highlightMatches([...row.topic_words].sort().join(', '))
                "
              ></td>
            </tr>
          </tbody>
        </table>
      </div>
      <br />
    </div>

    <div v-if="selected_topic.length > 0">
      <h3 class="mb-3 mt-5">Set topic composition</h3>
      <p>
        Expected hits:
        <b-spinner small v-show="hits_loading" label="Spinning"></b-spinner>
        <span v-show="!hits_loading">{{ total_hits }}</span>
      </p>
    </div>

    <form v-if="selected_topic.length > 0">
      <div v-for="selected in selected_topic" :key="'slider_' + selected">
        <div class="row align-items-center">
          <div class="col-12 col-md-3">
            <h5>{{ topic_data[selected].label }}</h5>
            <button
              @click="removeSelected(selected)"
              type="button"
              class="btn btn-link btn-sm wbg-button-danger"
            >
              <i class="fas fa-trash fa-sm mr-2" aria-hidden="true"></i>Remove
            </button>
          </div>
          <div class="col-12 col-md-9">
            <div class="form-group mt-2 mb-3">
              <label for="formControlRange" class="small-label"
                >Current value: {{ getSliderValue(selected) }}%</label
              >
              <label style="float: right" class="small-label"
                >Range {{ Math.round(topic_ranges[selected].min * 100) }}%-{{
                  Math.round(topic_ranges[selected].max * 100)
                }}%</label
              >
              <input
                type="range"
                class="form-control-range"
                id="formControlRange"
                :min="topic_ranges[selected].min * 100"
                :max="topic_ranges[selected].max * 100"
                step="0.1"
                v-on:input="onSliderChange(selected, $event)"
                :value="getSliderValue(selected)"
                v-on:mouseup="getHitsCount"
                v-on:touchend="getHitsCount"
              />
            </div>
            <span class="topic-words">
              {{
                rows.filter((o) => {
                  return o.topic_id === selected;
                })[0].topic_words
              }}
            </span>
          </div>
        </div>
        <hr />
      </div>
      <!-- <div class="row">
        <div class="col-12">
          <button
            @click="removeLastSelected"
            type="button"
            class="btn btn-link btn-sm wbg-button-danger"
          >
            <i class="fas fa-trash fa-sm mr-2" aria-hidden="true"></i>Remove
            topic
          </button>
        </div>
      </div> -->
    </form>
    <div v-if="selected_topic.length > 0" class="row mb-4">
      <div class="col-12">
        <button
          type="button"
          class="btn btn-primary btn-lg wbg-button"
          @click="submitTopicRanges"
        >
          <i class="fas fa-search fa-sm mr-1" aria-hidden="true"></i>Search
        </button>
        <hr />
      </div>
    </div>
  </div>
</template>

topic_set


<script>
import MLModelSelect from "./MLModelSelect";
export default {
  name: "FilterTable",
  components: { MLModelSelect },
  mounted() {
    window.filter_table_vm = this;
    // this.getModelTopics();
  },
  data: function () {
    return {
      nlp_api_url: null,
      loading: false,
      hits_loading: false,
      total_hits: null,
      topic_data: {},
      topicValue: {},
      selected_topic: [],
      topic_ranges: {},
      model_name: "lda",
      model_run_info_id: null,
      filter: "",
      rows: [],
    };
  },
  methods: {
    submitTopicRanges() {
      this.$emit("topicRangeReceived", {
        model_name: this.model_name,
        model_id: this.model_run_info_id,
        topic_value: this.topicValue,
      });
    },
    getSliderValue(selected) {
      if (this.topicValue[selected] === undefined) {
        return Math.round(
          (100 *
            (this.topic_ranges[selected].max +
              this.topic_ranges[selected].min)) /
            2
        );
      }
      return this.topicValue[selected];
    },
    onSliderChange(selected, event) {
      //   this.topicValue = Object.assign({}, this.topicValue, {
      //     selected: event.target.value,
      //   });
      this.$set(this.topicValue, selected, event.target.value);
    },
    disableSelect(topic_id) {
      if (this.selected_topic.length >= 3) {
        if (!this.selected_topic.includes(topic_id)) {
          return true;
        }
      }
      return false;
    },
    initOrRemoveTopicValue(selected, event) {
      if (event.target.checked) {
        this.$set(this.topicValue, selected, this.getSliderValue(selected));
      } else {
        delete this.topicValue[selected];
      }
    },
    removeSelected(topic_id) {
      this.selected_topic = this.selected_topic.filter((o) => o != topic_id);
      delete this.topicValue[topic_id];
    },
    removeLastSelected() {
      var selected = this.selected_topic.pop();
      delete this.topicValue[selected];
    },
    clearTopicSelect(event) {
      if (!event.target.checked) {
        this.selected_topic = [];
        this.topicValue = {};
      }
    },
    highlightMatches(text) {
      const matchExists = text
        .toLowerCase()
        .includes(this.filter.toLowerCase());
      if (!matchExists) return text;

      const re = new RegExp(this.filter, "ig");
      return text.replace(
        re,
        (matchedText) => `<strong>${matchedText}</strong>`
      );
    },
    onModelSelect: function (result) {
      this.model_run_info_id = result.model_run_info_id;
      this.model_name = result.model_name;
      this.nlp_api_url = result.url;
      this.getModelTopics();

      // Call this inside the getModelTopics then clause to prevent race condition when running a single API worker.
      // this.getTopicRanges();
    },
    formatTopicText: function (topic, with_topic_id = false) {
      var topic_words = topic.topic_words
        .slice(0, 8)
        .map(function (x) {
          return x.word;
        })
        .join(", ");

      if (with_topic_id) {
        topic_words = "Topic " + topic.topic_id + ": " + topic_words;
      }

      return topic_words;
    },
    getHitsCount: function () {
      this.hits_loading = true;
      var data = {};
      Object.assign(data, this.topicValue);
      Object.entries(data).forEach(([key, val]) => (data[key] = val / 100));

      if (Object.keys(data).length === 0) {
        return;
      }

      this.$http
        .post(this.nlp_api_url + "/get_docs_by_topic_composition_count", {
          model_id: this.model_run_info_id,
          topic_percentage: data,
        })
        .then((response) => {
          this.total_hits = response.data.total;
        })
        .finally(() => (this.hits_loading = false));
    },
    getTopicRanges: function () {
      this.$http
        .get(
          this.nlp_api_url +
            "/get_model_topic_ranges?model_id=" +
            this.model_run_info_id
        )
        .then((response) => {
          this.topic_ranges = response.data;
        });
    },
    getModelTopics: function () {
      this.loading = true;
      this.$http
        .get(this.nlp_api_url + "/get_model_topic_words", {
          params: this.searchParams,
        })
        .then((response) => {
          this.model_topics = response.data;
          //   this.model_topics.
          this.rows = this.lodash.map(this.model_topics, (value) => {
            var topic_id = "topic_" + value.topic_id;
            var topic_label = "Topic " + (value.topic_id + 1);
            var topic_words = this.formatTopicText(value);
            this.topic_data[topic_id] = {
              label: topic_label,
              words: topic_words,
            };
            return {
              topic_id: topic_id,
              topic_label: topic_label,
              topic_words: topic_words,
            };
          });

          this.getTopicRanges();

          // this.current_lda_model_topics = response.data;
          // this.current_lda_model_topics_options = this.lodash.map(
          //   this.current_lda_model_topics,
          //   (topic) => {
          //     return {
          //       text: this.formatTopicText(topic),
          //       value: topic.topic_id,
          //     };
          //   }
          // );
          // this.topic_words = this.current_lda_model_topics[this.topic_id];
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
        })
        .finally(() => (this.loading = false));
    },
  },
  computed: {
    filteredRows() {
      return this.rows.filter((row) => {
        const topic_words = row.topic_words.toLowerCase();
        const searchTerm = this.filter.toLowerCase();

        return topic_words.includes(searchTerm);
      });
    },
    topicSelected() {
      return this.selected_topic.length > 0;
    },

    searchParams() {
      const params = new URLSearchParams();
      params.append("model_id", this.model_run_info_id);
      params.append("topn_words", 10);
      return params;
    },
  },
  watch: {
    selected_topic: function () {
      this.getHitsCount();

      this.$emit("topicSelectionUpdated", true);
    },
  },
};
</script>

<style scoped>
/* table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td,
th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

th {
  background-color: #dddddd;
} */

input[type="text"],
select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  /* margin-top: 25px; */
}
.table-wrapper {
  max-height: 300px !important;
  overflow-y: scroll !important;
}

.topic-words {
  font-size: 14px;
  color: rgb(119, 115, 115);
}

.topic-label {
  font-size: 1rem;
}

.keywords-class {
  font-size: 1rem;
}

.small-label {
  font-size: 14px;
}

/*
table tbody th {
  position: relative;
}
table thead tr th:first-child {
  position: sticky !important;
  left: 0;
  z-index: 2;
}
table tbody tr th {
  position: sticky !important;
  left: 0;
  z-index: 1;
} */
</style>