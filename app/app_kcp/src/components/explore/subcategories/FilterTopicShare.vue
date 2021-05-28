<template>
  <div>
    <header>
      <h1 class="blog-post-title mb-3" dir="auto">
        {{ page_title }}
      </h1>
    </header>

    <div>
      <article class="blog-post">
        <!-- <p class="lead"> -->
        <p>
          Topic models are able to extract topics present in a document. The
          extracted topics in a document are weighted based on how much a given
          topic is represented in the document.
        </p>
        <p>
          In this demo, we show that the topic composition extracted from
          documents by topic models can be a powerful tool for discovery and
          retrieval of highly relevant documents.
        </p>

        <p>
          To start exploring, select a topic model to use. Then, the topics
          learned by the model will be available in the table below. You can
          select up to 3 topics as filter. Use the filter box to easily explore
          the available topics. The value of the threshold for the selected
          topic can be adjusted using the slider. A real-time count of expected
          hits is shown for reference. Click
          <span style="font-weight: bold">Search</span> to render the relevant
          documents.
        </p>

        <FilterTable
          @topicRangeReceived="submitTopicSearch"
          @topicSelectionUpdated="topicSelectionUpdated"
        />

        <a name="results"></a>
        <div v-if="this.model_id">
          <h2>Filtering Results</h2>

          <div :class="topic_selection_dirty ? 'blurred' : ''">
            <SearchResultLoading :loading="loading" :size="curr_size" />
            <SearchResultCard
              v-for="(result, idx, key) in hits"
              :result="result"
              :match="match_stats[idx]"
              v-bind:key="result.id + key"
            />
          </div>

          <Pagination
            @pageNumReceived="sendSearch"
            @currSizeSet="setCurrSize"
            :num_pages="num_pages"
            :curr_page_num="curr_page_num"
            :has_hits="hits.length > 0 && !no_more_hits"
            :page_sizes="page_sizes"
            :page_window="page_window"
            :next="next"
            :next_override="next_override"
          />
        </div>
        <hr />
        <PageFooter :url="share_url" :share_text="share_text" />
      </article>
    </div>
  </div>
</template>

<script>
import saveState from "vue-save-state";

import FilterTable from "../../common/FilterTable";
import SearchResultCard from "../../common/SearchResultCard";
import SearchResultLoading from "../../common/SearchResultLoading";
import Pagination from "../../common/Pagination";

import PageFooter from "../../common/PageFooter";

export default {
  name: "FilterTopicShare",
  props: {
    page_title: String,
    share_url: String,
    share_text: String,
  },
  mixins: [saveState],
  mounted() {
    window.vm = this;
    this.model_id = null;
    this.hits = [];
  },
  computed: {
    searchBody() {
      const body = {
        model_id: this.model_id,
        topic_percentage: this.topic_percentage,
        from_result: this.from_result,
        size: this.curr_size,
      };
      return body;
    },
    no_more_hits() {
      var next_from = this.curr_page_num * this.curr_size;

      var no_more_hits = false;
      if (next_from > this.total.value) {
        no_more_hits = true;
      }

      return no_more_hits;
    },
  },
  components: {
    FilterTable,
    SearchResultCard,
    SearchResultLoading,
    Pagination,
    PageFooter,
  },
  data: function () {
    return {
      page_sizes: this.$config.pagination.page_sizes,
      start: 0,
      end: 0,
      next: 0,
      page_window: this.$config.pagination.page_window,
      curr_page_num: 0,
      curr_size: this.$config.pagination.size,
      num_pages: 0,
      next_override: false,
      model_id: null,
      model_name: null,
      topic_percentage: {},
      from_result: 0,
      size: 10,
      hits: [],
      match_stats: [],
      total: Object,
      errored: false,
      loading: false,
      topic_selection_dirty: false,
    };
  },
  methods: {
    topicSelectionUpdated(event) {
      this.topic_selection_dirty = event;
    },
    getSaveStateConfig() {
      return {
        cacheKey: "filterTopicSharePage",
      };
    },
    sendSearch: function (page_num = 1) {
      this.loading = true;
      this.curr_page_num = page_num;
      var from = (page_num - 1) * this.curr_size;

      if (from > this.total.value) {
        return;
      }
      this.hits = [];
      this.match_stats = [];
      this.from_result = from;

      this.$http
        .post(
          this.$config.nlp_api_url[this.model_name] +
            "/get_docs_by_topic_composition",
          this.searchBody
        )
        .then((response) => {
          this.hits = response.data.hits;
          this.match_stats = response.data.result.hits;
          this.total = response.data.total;
          this.next = this.curr_page_num + 1;
          this.start = this.from_result + 1;
          this.end = this.from_result + this.hits.length;
          this.num_pages = Math.floor(this.total.value / this.curr_size);
          if (this.total.value % this.curr_size > 0) {
            this.num_pages += 1;
          }
        })
        .finally(() => (this.loading = false));
    },
    submitTopicSearch(filterPanelData) {
      this.topic_selection_dirty = false;
      this.model_id = filterPanelData.model_id;
      this.model_name = filterPanelData.model_name;
      this.topic_percentage = {};
      Object.assign(this.topic_percentage, filterPanelData.topic_value);
      Object.entries(this.topic_percentage).forEach(
        ([key, val]) => (this.topic_percentage[key] = val / 100)
      );

      this.sendSearch();
    },
    setCurrSize: function (size) {
      this.curr_size = size;
      this.sendSearch();
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.blurred {
  -webkit-filter: blur(1px);
  -moz-filter: blur(1px);
  -o-filter: blur(1px);
  -ms-filter: blur(1px);
  filter: blur(1px);
}

/* h3 {
  margin: 40px 0 0;
} */
/* a {
  color: #42b983;
} */
</style>
