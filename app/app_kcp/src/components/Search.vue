<template>
  <div>
    <header class="blog-header wbg-internal-header">
      <div class="container">
        <div class="col-12 mb-2">
          <div id="breadcrumbs">
            <router-link to="/">Home</router-link>
            <span class="wbg-breadcrumb-separator">/</span>
            <router-link to="/search">Search</router-link>
          </div>
        </div>
        <div class="col-12">
          <i class="fas fa-search fa-2x" aria-hidden="true"></i>
          <h1>Search</h1>
          <p></p>
        </div>
      </div>
    </header>

    <div class="container">
      <div class="row">
        <div class="col-12 col-md-12 mb-2">
          <div class="row justify-content-center">
            <div class="col-12 col-md-9 col-lg-8">
              <div
                class="input-group wbg-input-group mb-3 mt-3"
                style="display: flex"
              >
                <input
                  v-model="query"
                  type="text"
                  class="form-control wbg-search-text pl-4"
                  :placeholder="uploaded_file ? '' : 'Enter your keywords...'"
                  aria-label="Field for search"
                  aria-describedby="basic-addon2"
                  v-on:keyup.enter="sendSearch()"
                />
                <div v-if="hasUploadedFile" class="wbg-uploaded-file">
                  <div class="truncated-title">
                    {{ this.uploaded_file.name }}
                  </div>
                  <i
                    class="fas fa-times fa-sm ml-2"
                    @click="removeFile"
                    aria-hidden="true"
                  ></i>
                </div>
                <div
                  id="submit_file"
                  data-toggle="tooltip"
                  data-placement="bottom"
                  title="Upload a PDF or TXT document to search"
                >
                  <div class="file-input">
                    <input
                      @change="fileUpload"
                      type="file"
                      name="file-input"
                      :value="file_input"
                      :disabled="hasUploadedFile"
                      id="file-input"
                      class="file-input__input"
                      data-toggle="tooltip"
                      data-placement="bottom"
                      title="Upload a PDF or TXT document to search"
                      accept=".txt,.doc,.docx,.pdf"
                    />
                    <label class="file-input__label" for="file-input"
                      ><i
                        class="fas fa-file-upload fa-lg"
                        :style="hasUploadedFile ? 'color: gray' : ''"
                      ></i
                    ></label>
                  </div>
                </div>
                <div class="input-group-append">
                  <button
                    @click="sendSearch()"
                    class="btn btn-primary wbg-search-button pr-4 pl-4"
                    type="button"
                  >
                    Search
                  </button>
                </div>
              </div>
            </div>

            <div class="col-12 col-md-12 text-center">
              <span v-if="suggestions.length > 0" class="keyword-suggestions">
                <span class="suggestions">Suggestions:</span>
                <span
                  @click="searchSuggestion(word)"
                  v-for="word in suggestions"
                  :key="'suggest_' + word"
                  class="suggestion"
                  >{{ word }}
                </span>
                <br />
                <br />
              </span>
            </div>

            <div class="col-12 col-md-12 text-center">
              <div class="form-check form-check-inline">
                <input
                  class="form-check-input"
                  type="radio"
                  name="inlineRadioOptions"
                  id="inlineRadio1"
                  value="keyword"
                  :checked="!uploaded_file"
                  v-model="search_type"
                  :disabled="uploaded_file"
                  @change="resetFrom"
                />
                <label class="form-check-label" for="inlineRadio1"
                  >Keyword search</label
                >
              </div>
              <div class="form-check form-check-inline">
                <input
                  class="form-check-input"
                  type="radio"
                  name="inlineRadioOptions"
                  id="inlineRadio2"
                  value="semantic"
                  v-model="search_type"
                  @change="resetFrom"
                />
                <label class="form-check-label" for="inlineRadio2"
                  >Semantic search</label
                >
              </div>
            </div>
            <div class="col-12 text-center mt-3">
              <small
                >You can also try
                <router-link to="explore/subcategories/filtering-by-topic-share"
                  >filtering by topic composition</router-link
                ></small
              >
            </div>
          </div>
          <hr />
        </div>
        <a name="results"></a>
        <aside class="col-sm-3" id="blog-sidebar">
          <div>
            <div
              id="filter-by-access"
              class="sidebar-filter wb-ihsn-sidebar-filter filter-by-year filter-box"
            >
              <h6 class="togglable">
                <i class="fa fa-search pr-2"></i>Filter by Year {{ min_year }} -
                {{ max_year }}
              </h6>
              <div class="sidebar-filter-entries">
                <input type="hidden" />
                <p class="mt-3 mb-2">Show studies conducted between</p>
                <div class="form-group">
                  <select
                    name="from"
                    id="from"
                    v-model="min_year"
                    class="form-control"
                  >
                    <option
                      v-for="year_offset in 131"
                      :key="'from-' + (2022 - year_offset)"
                      :value="2022 - year_offset"
                    >
                      {{ 2022 - year_offset }}
                    </option>
                    <option value="1890" selected>1890</option>
                  </select>
                </div>
                <p class="mt-3 mb-2">and</p>
                <div class="form-group">
                  <select
                    name="to"
                    id="to"
                    v-model="max_year"
                    class="form-control"
                  >
                    <option
                      v-for="year_offset in 132"
                      :key="'to-' + (2022 - year_offset)"
                      :value="2022 - year_offset"
                    >
                      {{ 2022 - year_offset }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </aside>
        <div class="col-sm-9 blog-main">
          <article class="blog-post">
            <header></header>

            <div class="nada-pagination" v-show="hits.length > 0">
              <div
                class="row mt-3 mb-3 d-flex justify-content-lg-between align-items-center"
              >
                <div class="col-12 col-md-3 col-lg-4 mb-3 mb-md-0 small">
                  Showing <b>{{ start }}-{{ end }}</b> of
                  <b>{{ total.message }}</b> studies
                </div>
                <div
                  class="filter-action-bar d-flex col-12 col-md-9 col-lg-8 justify-content-lg-end"
                >
                  <div class="dropdown">
                    <button
                      class="btn btn-outline-secondary btn-sm dropdown-toggle wbg-button"
                      type="button"
                      id="dropdownMenuButton"
                      data-toggle="dropdown"
                      aria-haspopup="true"
                      aria-expanded="false"
                    >
                      Sort by
                    </button>
                    <div
                      class="dropdown-menu"
                      aria-labelledby="dropdownMenuButton"
                    >
                      <a class="dropdown-item" href="#">Relevance</a>
                      <a class="dropdown-item" href="#">Release date</a>
                      <a class="dropdown-item" href="#">Trending (past day)</a>
                      <a class="dropdown-item" href="#">Trending (past week)</a>
                    </div>
                  </div>
                  <button
                    type="button"
                    class="btn btn-outline-secondary btn-sm wbg-button ml-2"
                  >
                    <i class="fas fa-chart-bar fa-lg mr-1"></i>Show statistics
                  </button>
                  <a
                    target="_blank"
                    href="#"
                    class="btn btn btn-outline-success btn-sm wbg-button ml-2"
                    ><i class="fa fa-print"></i></a
                  ><a
                    target="_blank"
                    href="#"
                    class="btn btn btn-outline-success btn-sm wbg-button ml-2"
                    ><i class="fa fa-file-excel-o"></i
                  ></a>
                </div>
              </div>
            </div>
            <div v-if="min_year && max_year" class="active-filters-container">
              <div class="active-filters">
                <span
                  class="badge badge-default wb-badge-close remove-filter years"
                  data-type="years"
                  data-value="0"
                  >between {{ min_year }}-{{ max_year
                  }}<i class="fa fa-close"></i
                ></span>

                <a
                  href="#"
                  class="btn-reset-search btn btn-outline-primary btn-sm"
                  >Reset search</a
                >
              </div>
            </div>
            <SearchResultLoading :loading="loading" :size="curr_size" />
            <SearchResultCard
              v-for="result in hits"
              :result="result"
              v-bind:key="result.id"
            />
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
            <hr />
            <PageFooter :url="share_url" :share_text="share_text" />
          </article>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import $ from "jquery";
import saveState from "vue-save-state";

import SearchResultCard from "./common/SearchResultCard";
import SearchResultLoading from "./common/SearchResultLoading";
import Pagination from "./common/Pagination";
import PageFooter from "./common/PageFooter";
window.onbeforeunload = function () {
  localStorage.clear();
};

export default {
  name: "Search",
  props: {
    share_url: String,
    share_text: String,
  },
  components: { SearchResultCard, SearchResultLoading, Pagination, PageFooter },
  mixins: [saveState],
  mounted() {
    window.vm = this;
    this.flowSideBar();

    if (this.$route.query.search_type !== undefined) {
      this.search_type = this.$route.query.search_type;

      if (this.$route.query.search_text !== undefined) {
        this.query = this.$route.query.search_text;

        var page_num = 1;
        if (this.$route.query.page !== undefined) {
          page_num = Number(this.$route.query.page);
        }
        this.sendSearch(page_num);
      }
    }
  },
  computed: {
    hasUploadedFile() {
      if (this.uploaded_file !== null) {
        if (this.uploaded_file.name !== undefined) {
          return true;
        }
      }
      return false;
    },
    suggestionBody() {
      const body = {
        model_id: this.$config.default_model.word2vec.model_id,
        raw_text: this.query,
        topn_words: this.suggestion_count,
      };
      return body;
    },
    searchParams() {
      const params = new URLSearchParams();
      params.append("model_id", this.$config.default_model.word2vec.model_id);
      params.append("query", this.query);
      params.append("from_result", this.from_result);
      params.append("size", this.curr_size);
      return params;
    },
    fileParams() {
      const formData = new FormData();
      formData.append("model_id", this.$config.default_model.word2vec.model_id);
      formData.append("file", this.uploaded_file);
      formData.append("from_result", this.from_result);
      formData.append("size", this.curr_size);
      return formData;
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
  data: function () {
    return {
      min_year: null,
      max_year: null,
      search_type: "keyword",
      keyword_search_api_url: this.$config.search_url.keyword,
      semantic_search_api_url: this.$config.search_url.semantic,
      file_search_api_url: this.$config.search_url.file,
      suggestion_api_url:
        this.$config.nlp_api_url.word2vec + "/get_similar_words",
      page_sizes: this.$config.pagination.page_sizes,
      suggestions: [],
      suggestion_anchor: "",
      suggestion_count: 6,
      start: 0,
      end: 0,
      next: 0,
      page_window: this.$config.pagination.page_window,
      curr_page_num: 0,
      curr_size: this.$config.pagination.size,
      num_pages: 0,
      next_override: false,
      query: "",
      from_result: 0,
      hits: [],
      total: Object,
      errored: false,
      loading: false,
      uploaded_file: null,
      file_input: null,
      query_cache: "",
    };
  },
  methods: {
    fileUpload(event) {
      this.uploaded_file = event.target.files[0];
      this.query_cache = this.query;
      this.query = "";
      this.search_type = "semantic";
    },
    removeFile() {
      this.uploaded_file = null;
      this.file_input = null;
      this.query = this.query_cache;
    },
    getSaveStateConfig() {
      return {
        cacheKey: "searchPage",
      };
    },
    resetFrom: function () {
      this.from_result = 0;
    },
    getSuggestions: function () {
      if (!this.query) {
        return;
      }
      if (this.query === this.suggestion_anchor) {
        return;
      }
      this.suggestions = [];

      this.$http
        .post(this.suggestion_api_url, this.suggestionBody)
        .then((response) => {
          this.suggestions = response.data
            .map((o) => {
              if (
                o.score < 0.99 &&
                o.word.replaceAll("_", " ") !== this.query
              ) {
                return o.word;
              }
            })
            .filter((word) => word)
            .slice(0, this.suggestion_count - 1);
          this.suggestion_anchor = this.query;
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
        });
    },
    searchSuggestion: function (word) {
      this.query = word;
      this.sendSearch();
    },
    sendSearch: function (page_num = 1) {
      this.curr_page_num = page_num;
      var from = (page_num - 1) * this.curr_size;

      this.hits = [];
      this.next_override = true;

      if (this.search_type == "keyword") {
        this.next_override = false;
        this.sendKeywordSearch(from);
        this.getSuggestions();
      } else if (this.search_type == "semantic") {
        if (this.uploaded_file != null) {
          this.sendFileSearch(from);
        } else {
          this.sendSemanticSearch(from);
          this.getSuggestions();
        }
      } else {
        return;
      }

      this.$router.replace({
        name: "search",
        query: {
          search_text: this.query,
          search_type: this.search_type,
          page: this.curr_page_num,
        },
      });
    },
    sendKeywordSearch: function (from = 0) {
      if (!this.query) {
        return;
      }
      if (from > this.total.value) {
        return;
      }
      this.query = this.query.replaceAll("_", " ");
      this.from_result = from;
      this.loading = true;

      this.$http
        .get(this.keyword_search_api_url, {
          params: this.searchParams,
        })
        .then((response) => {
          this.hits = response.data.hits;
          this.total = response.data.total;
          this.next = this.curr_page_num + 1;
          // this.next = response.data.next;
          this.start = this.from_result + 1;
          this.end = this.from_result + this.hits.length;
          this.num_pages = Math.floor(this.total.value / this.curr_size);
          if (this.total.value % this.curr_size > 0) {
            this.num_pages += 1;
          }
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
          this.loading = false;
        })
        .finally(() => (this.loading = false));
    },
    sendSemanticSearch: function (from = 0) {
      if (!this.query) {
        return;
      }
      // if (from > this.total.value) {
      //   return;
      // }
      this.from_result = from;
      this.loading = true;

      this.$http
        .get(this.semantic_search_api_url, {
          params: this.searchParams,
        })
        .then((response) => {
          this.hits = response.data.hits;
          this.total = response.data.total;
          this.next = this.curr_page_num + 1;
          this.start = this.from_result + 1;
          this.end = this.from_result + this.hits.length;
          this.num_pages = Math.floor(this.total.value / this.curr_size);
          if (this.total.value % this.curr_size > 0) {
            this.num_pages += 1;
          }
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
          this.loading = false;
        })
        .finally(() => (this.loading = false));
    },
    sendFileSearch: function (from = 0) {
      this.from_result = from;
      this.loading = true;

      this.$http
        .post(this.file_search_api_url, this.fileParams)
        .then((response) => {
          this.hits = response.data.hits;
          this.total = response.data.total;
          this.next = this.curr_page_num + 1;
          this.start = this.from_result + 1;
          this.end = this.from_result + this.hits.length;
          this.num_pages = Math.floor(this.total.value / this.curr_size);
          if (this.total.value % this.curr_size > 0) {
            this.num_pages += 1;
          }
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
          this.loading = false;
        })
        .finally(() => (this.loading = false));
    },
    setCurrSize: function (size) {
      this.curr_size = size;
      this.sendSearch();
    },
    flowSideBar: function () {
      $(function () {
        var $sidebar = $("#blog-sidebar"),
          $window = $(window),
          offset = $sidebar.offset(),
          topPadding = 15;

        $window.scroll(function () {
          if (($window.scrollTop() > offset.top) & ($(window).width() > 768)) {
            $sidebar.stop().animate(
              {
                marginTop: $window.scrollTop() - offset.top + topPadding,
              },
              { easing: "ease", duration: 0 }
            );
          } else {
            $sidebar.stop().animate({
              marginTop: 0,
            });
          }
        });
      });
    },
  },
  watch: {
    search_type: function () {
      this.sendSearch();
    },
  },
};
</script>

<style scoped>
@import "../../node_modules/bootstrap-vue/dist/bootstrap-vue.css";

.content-row {
  min-height: 50vh;
}
@media (min-width: 1200px) {
  .flowing {
    max-width: 1200px;
  }
}

.wbg-internal-header {
  padding-top: 1rem;
  padding-bottom: 1rem;
}

/*
.blog-main {
  margin: 0;
  padding-left: 1rem;
}

.blog-sidebar {
  margin-left: -2rem;
  padding: 0;
} */

.truncated-title {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1; /* number of lines to show */
  -webkit-box-orient: vertical;
}
.active-filters-container {
  margin: 20px 0 30px;
  border-radius: 3px;
  position: relative;
}
.active-filters-container .active-filters {
  background: #f3f3f3;
  overflow: auto;
  color: white;
  clear: both;
  padding: 10px;
}
.active-filters-container .active-filters .years {
  background-color: #787878;
}
.active-filters-container .wb-badge-close {
  padding: 10px 10px;
  margin: 2px 4px 2px 0;
  position: relative;
  padding-right: 30px;
  cursor: pointer;
  transition: opacity 0.35s;
}
.btn-outline-primary {
  color: #0071bc;
}
.keyword-suggestions {
  width: 100%;
  margin-left: 15px;
  padding: 5px;
  padding-bottom: 25px;
}
.suggestions {
  margin-right: 10px;
}
.suggestion {
  color: #0062cc;
  margin-right: 10px;
  cursor: pointer;
}
</style>