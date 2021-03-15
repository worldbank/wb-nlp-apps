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
                  placeholder="Enter your keywords..."
                  aria-label="Field for search"
                  aria-describedby="basic-addon2"
                  v-on:keyup.enter="sendSearch()"
                />
                <div
                  id="submit_file"
                  data-toggle="tooltip"
                  data-placement="bottom"
                  title="Upload a PDF or TXT document to search"
                >
                  <div class="file-input">
                    <input
                      type="file"
                      name="file-input"
                      id="file-input"
                      class="file-input__input"
                      data-toggle="tooltip"
                      data-placement="bottom"
                      title="Upload a PDF or TXT document to search"
                    />
                    <label class="file-input__label" for="file-input"
                      ><i class="fas fa-file-upload fa-lg"></i
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
                  checked
                  v-model="search_type"
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

            <SearchResultCard
              v-for="result in hits"
              :result="result"
              v-bind:key="result.id"
            />

            <div class="nada-pagination mt-5">
              <div
                class="row mt-3 mb-3 d-flex justify-content-lg-between align-items-center"
              >
                <div class="col-12 col-lg-6 mb-3 small">
                  <div
                    id="items-per-page"
                    class="items-per-page light switch-page-size"
                  >
                    <small
                      >Results per page:
                      <span
                        class="wbg-pagination-btn"
                        :class="size === curr_size ? 'active' : ''"
                        v-for="size in page_sizes"
                        v-bind:key="size"
                        @click="setSize(size)"
                        >{{ size }}</span
                      >
                    </small>
                  </div>
                </div>
                <div class="col-12 col-lg-6 d-flex justify-content-lg-end">
                  <nav aria-label="Page navigation">
                    <ul
                      class="pagination pagination-md wbg-pagination-ul small"
                    >
                      <li
                        class="page-item"
                        v-for="page_num in num_pages"
                        v-bind:key="page_num"
                      >
                        <a
                          href="#results"
                          @click="sendSearch(page_num)"
                          class="page-link"
                          :class="page_num === curr_page_num ? 'active' : ''"
                          :data-page="page_num"
                          >{{ page_num }}</a
                        >
                      </li>

                      <li class="page-item" v-show="hits.length > 0">
                        <a
                          href="#results"
                          @click="sendSearch(next)"
                          class="page-link"
                          data-page="2"
                          >Next</a
                        >
                      </li>
                      <li class="page-item" v-show="hits.length > 0">
                        <a
                          href="#results"
                          @click="sendSearch(num_pages)"
                          class="page-link"
                          :data-page="num_pages + 1"
                          title="Last"
                          >»</a
                        >
                      </li>
                    </ul>
                  </nav>
                </div>
              </div>
            </div>
            <hr />
            <footer>
              <section>
                <h4>Share</h4>
                <nav class="nav sharing-icons mt-4">
                  <a
                    class="nav-item"
                    href="https://www.facebook.com/sharer/sharer.php?u=%2fsearch%2f"
                    title="Share on Facebook"
                    ><span
                      class="fab fa-facebook-f fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://www.linkedin.com/shareArticle?mini=true&url=%2fsearch%2f"
                    title="Share on LinkedIn"
                    ><span
                      class="fab fa-linkedin-in fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://twitter.com/intent/tweet?url=%2fsearch%2f&text=Search"
                    title="Tweet this"
                    ><span class="fab fa-twitter fa-lg"></span
                  ></a>
                </nav>
              </section>
            </footer>
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

window.onbeforeunload = function () {
  localStorage.clear();
};

export default {
  name: "Search",
  components: { SearchResultCard },
  mixins: [saveState],
  mounted() {
    this.flowSideBar();
  },
  computed: {
    searchParams() {
      const params = new URLSearchParams();
      params.append("query", this.query);
      params.append("from_result", this.from_result);
      params.append("size", this.size);
      return params;
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
      page_sizes: [10, 25, 50, 100],
      start: 0,
      end: 0,
      next: 0,
      curr_page_num: 0,
      curr_size: 10,
      num_pages: 0,
      query: "",
      from_result: 0,
      size: 10,
      hits: [],
      total: Object,
      errored: false,
      loading: false,
    };
  },
  methods: {
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
      var from = (page_num - 1) * this.size;

      if (this.search_type == "keyword") {
        this.sendKeywordSearch(from);
      } else if (this.search_type == "semantic") {
        this.sendSemanticSearch(from);
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
          this.num_pages = Math.floor(this.total.value / this.size);
          if (this.total.value % this.size > 0) {
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
          this.num_pages = Math.floor(this.total.value / this.size);
          if (this.total.value % this.size > 0) {
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
      this.size = size;
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