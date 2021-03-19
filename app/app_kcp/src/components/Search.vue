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
                  {{ this.uploaded_file.name }}
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
                <i class="fa fa-search pr-2"></i>Filter by Year
              </h6>
              <div class="sidebar-filter-entries">
                <input type="hidden" />
                <p class="mt-3 mb-2">Show studies conducted between</p>
                <div class="form-group">
                  <select name="from" id="from" class="form-control">
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
                  <select name="to" id="to" class="form-control">
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
            <SearchResultLoading :loading="loading" :size="curr_size" />
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
    searchParams() {
      const params = new URLSearchParams();
      params.append("query", this.query);
      params.append("from_result", this.from_result);
      params.append("size", this.curr_size);
      return params;
    },
    fileParams() {
      const formData = new FormData();
      formData.append("file", this.uploaded_file);
      formData.append("from_result", this.from_result);
      formData.append("size", this.curr_size);
      return formData;
    },
    myProps() {
      var retVal = null;
      if (this.$route.name === "a") {
        retVal = { foo: this.foo };
      }
      if (this.$route.name === "b") {
        retVal = { bar: this.bar };
      }
      return retVal;
    },
  },
  data: function () {
    return {
      search_type: "keyword",
      keyword_search_api_url: "/nlp/search/keyword",
      semantic_search_api_url: "/nlp/search/semantic",
      file_search_api_url: "/nlp/search/file",
      page_sizes: [10, 25, 50, 100],
      start: 0,
      end: 0,
      next: 0,
      page_window: 2,
      curr_page_num: 0,
      curr_size: 10,
      num_pages: 0,
      query: "",
      from_result: 0,
      hits: [],
      no_more_hits: false,
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
      this.search_type = "semantic";
      this.query_cache = this.query;
      this.query = "";
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
    sendSearch: function (page_num = 1) {
      this.curr_page_num = page_num;
      var from = (page_num - 1) * this.curr_size;
      var next_from = page_num * this.curr_size;

      this.no_more_hits = false;
      if (next_from > this.total.value) {
        this.no_more_hits = true;
      }
      this.hits = [];

      if (this.search_type == "keyword") {
        this.sendKeywordSearch(from);
      } else if (this.search_type == "semantic") {
        if (this.uploaded_file != null) {
          this.sendFileSearch(from);
        } else {
          this.sendSemanticSearch(from);
        }
      } else {
        return;
      }
    },
    sendKeywordSearch: function (from = 0) {
      if (from > this.total.value) {
        return;
      }
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
          this.next = response.data.next;
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
          this.next = response.data.next;
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
    setSize: function (size) {
      this.curr_size = size;
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
</style>