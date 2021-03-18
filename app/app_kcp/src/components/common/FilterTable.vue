<template>
  <div>
    <MLModelSelect @modelSelected="onModelSelect" :model_name="model_name" />

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
                  id="customCheck1"
                />
                <label class="custom-control-label" for="customCheck1">
                  Topic
                </label>
              </div>
            </th>
            <th>Keywords</th>
          </tr>
        </thead>
        <tbody v-if="rows.length > 0">
          <tr v-for="(row, index) in filteredRows" :key="`topic_word-${index}`">
            <th scope="row">
              <div class="custom-control custom-checkbox">
                <input
                  type="checkbox"
                  class="custom-control-input"
                  :id="'customCheck_' + index"
                  checked=""
                  :value="row.topic_id"
                  v-model="selected_topic"
                />
                <label
                  class="custom-control-label"
                  :for="'customCheck_' + index"
                  >{{ row.topic_id }}</label
                >
              </div>
            </th>
            <td
              v-html="highlightMatches([...row.topic_words].sort().join(', '))"
            ></td>
          </tr>
        </tbody>
      </table>
    </div>
    <br />
    <!--
    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th scope="col">
            <div class="custom-control custom-checkbox">
              <input
                type="checkbox"
                class="custom-control-input"
                id="customCheck1"
              />
              <label class="custom-control-label" for="customCheck1"
                >Topic</label
              >
            </div>
          </th>
          <th scope="col">Keywords</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">
            <div class="custom-control custom-checkbox">
              <input
                type="checkbox"
                class="custom-control-input"
                id="customCheck1"
                checked=""
              />
              <label class="custom-control-label" for="customCheck1"
                >Topic 0</label
              >
            </div>
          </th>
          <td>
            policy, sector, government, problem, make, large, cost, private,
            case, enterprise
          </td>
        </tr>
        <tr>
          <th scope="row">
            <div class="custom-control custom-checkbox">
              <input
                type="checkbox"
                class="custom-control-input"
                id="customCheck1"
              />
              <label class="custom-control-label" for="customCheck1"
                >Topic 1</label
              >
            </div>
          </th>
          <td>
            program, target, indicator, result, support, evaluation,
            beneficiary, outcome, improve, impact
          </td>
        </tr>
        <tr>
          <th scope="row">
            <div class="custom-control custom-checkbox">
              <input
                type="checkbox"
                class="custom-control-input"
                id="customCheck1"
                checked=""
              />
              <label class="custom-control-label" for="customCheck1"
                >Topic 2</label
              >
            </div>
          </th>
          <td>
            date, actual, project, target, current, end, jun, baseline,
            previous, status
          </td>
        </tr>
        <tr>
          <th scope="row">
            <div class="custom-control custom-checkbox">
              <input
                type="checkbox"
                class="custom-control-input"
                id="customCheck1"
              />
              <label class="custom-control-label" for="customCheck1"
                >Topic 3</label
              >
            </div>
          </th>
          <td>
            tourism, conflict, south, migration, migrant, security, economic,
            country, west, community
          </td>
        </tr>
        <tr>
          <th scope="row">...</th>
          <td>...</td>
        </tr>
        <tr>
          <th scope="row">
            <div class="custom-control custom-checkbox">
              <input
                type="checkbox"
                class="custom-control-input"
                id="customCheck1"
              />
              <label class="custom-control-label" for="customCheck1"
                >Topic 13</label
              >
            </div>
          </th>
          <td>
            tourism, conflict, south, migration, migrant, security, economic,
            country, west, community
          </td>
        </tr>
      </tbody>
    </table> -->
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
    this.getModelTopics();
  },
  data: function () {
    return {
      selected_topic: [],
      nlp_api_url: "/nlp/models/lda",
      model_name: "lda",
      model_run_info_id: null,
      filter: "",
      rows: [],
      //   [
      //     {
      //       department: "Accounting",
      //       employees: ["Bradley", "Jones", "Alvarado"],
      //     },
      //     {
      //       department: "Human Resources",
      //       employees: ["Juarez", "Banks", "Smith"],
      //     },
      //     {
      //       department: "Production",
      //       employees: ["Sweeney", "Bartlett", "Singh"],
      //     },
      //     {
      //       department: "Research and Development",
      //       employees: ["Lambert", "Williamson", "Smith"],
      //     },
      //     {
      //       department: "Sales and Marketing",
      //       employees: ["Prince", "Townsend", "Jones"],
      //     },
      //   ],
    };
  },
  methods: {
    clearTopicSelect(event) {
      if (!event.target.checked) {
        this.selected_topic = [];
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
    onModelSelect: function (model_run_info_id) {
      this.model_run_info_id = model_run_info_id;
      this.getModelTopics();
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
    getModelTopics: function () {
      this.$http
        .get(this.nlp_api_url + "/get_model_topic_words", {
          params: this.searchParams,
        })
        .then((response) => {
          this.model_topics = response.data;
          //   this.model_topics.
          this.rows = this.lodash.map(this.model_topics, (value) => {
            return {
              topic_id: "Topic " + value.topic_id,
              topic_words: this.formatTopicText(value),
            };
          });

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
};
</script>

<style scoped>
table {
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
}

input[type="text"],
select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  margin-top: 25px;
}
.table-wrapper {
  max-height: 300px !important;
  overflow-y: scroll !important;
}
</style>