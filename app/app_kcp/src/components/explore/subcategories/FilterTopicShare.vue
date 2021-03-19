<template>
  <div>
    <header>
      <h1 class="blog-post-title mb-3" dir="auto">
        <a
          href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/"
          >{{ page_title }}</a
        >
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

        <FilterTable @topicRangeReceived="submitTopicSearch" />

        <a name="results"></a>
        <div v-show="this.model_id">
          <h2>Filtering Results</h2>

          <SearchResultLoading :loading="loading" :size="size" />
          <SearchResultCard
            v-for="result in hits"
            :result="result"
            v-bind:key="result.id"
          />

          <Pagination
            @pageNumReceived="sendSearch"
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
  mounted() {
    window.vm = this;
  },
  computed: {
    searchBody() {
      const body = {
        model_id: this.model_id,
        topic_percentage: this.topic_percentage,
        from_result: this.from_result,
        size: this.size,
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
      nlp_api_url: "/nlp/models/lda",
      page_sizes: [10, 25, 50, 100],
      start: 0,
      end: 0,
      next: 0,
      page_window: 2,
      curr_page_num: 0,
      curr_size: 10,
      num_pages: 0,
      next_override: false,
      model_id: null,
      topic_percentage: {},
      from_result: 0,
      size: 10,
      hits: [],
      total: Object,
      errored: false,
      loading: false,
    };
  },
  methods: {
    sendSearch: function (page_num = 1) {
      this.loading = true;
      this.curr_page_num = page_num;
      var from = (page_num - 1) * this.size;

      if (from > this.total.value) {
        return;
      }
      this.hits = [];
      this.from_result = from;

      this.$http
        .post(
          this.nlp_api_url + "/get_docs_by_topic_composition",
          this.searchBody
        )
        .then((response) => {
          this.hits = response.data.hits;
          this.total = response.data.total;
          this.next = this.curr_page_num + 1;
          this.start = this.from_result + 1;
          this.end = this.from_result + this.hits.length;
          this.num_pages = Math.floor(this.total.value / this.size);
          if (this.total.value % this.size > 0) {
            this.num_pages += 1;
          }
        })
        .finally(() => (this.loading = false));
    },
    submitTopicSearch(filterPanelData) {
      this.model_id = filterPanelData.model_id;
      this.topic_percentage = {};
      Object.assign(this.topic_percentage, filterPanelData.topic_value);
      Object.entries(this.topic_percentage).forEach(
        ([key, val]) => (this.topic_percentage[key] = val / 100)
      );

      this.sendSearch();
    },

    setSize: function (size) {
      this.size = size;
      this.curr_size = size;
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
