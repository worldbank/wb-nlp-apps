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
        <p class="lead">
          Brief description of how the system works... (paragraph text with
          class "lead")
        </p>
        <p>... then provide the tool (regular paragraph text)</p>

        <FilterTable @topicRangeReceived="submitTopicSearch" />

        <h2>Filtering Results</h2>
        <SearchResultCard
          v-for="result in hits"
          :result="result"
          v-bind:key="result.id"
        />

        <!--
        <div class="document-row" data-url="#" title="View study">
          <div class="row">
            <div class="col-3 col-lg-3">
              <img
                src="/static/files/doc_thumb.png"
                title="document thumbnail"
                alt="document thumbnail"
              />
            </div>
            <div class="col-9 col-lg-9">
              <span class="badge badge-primary wbg-badge">DOCUMENT</span>
              <h5 class="title">
                <a
                  href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                  title="Service Provision Assessment Survey 2018-2019"
                  >Service Provision Assessment Survey 2018-2019</a
                >
              </h5>
              <div class="study-country">Afghanistan, 2018-2019</div>
              <div class="study-id d-md-flex mt-2">
                <span class="badge badge-pill badge-secondary"
                  >ID: wb_17427272</span
                >
                <div class="small ml-md-3 mt-2 mt-md-0">
                  Rank: 1, Score: 0.1723729397
                </div>
              </div>
              <div class="study-meta d-flex">
                <div class="small mt-2 mb-2 mr-3">
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/"
                    ><i class="fas fa-database mr-1" aria-hidden="true"></i
                    >Metadata</a
                  >
                </div>
                <div class="small mt-2 mb-2">
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/"
                    ><i
                      class="fas fa-chart-bar fa-lg mr-1"
                      aria-hidden="true"
                    ></i
                    >Topics</a
                  >
                </div>
              </div>
              <div class="sub-title">
                <div>
                  <span class="study-by">Ministry of Public Health</span>
                </div>
                <div class="owner-collection">
                  Collection:
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                    >MEASURE DHS: Demographic and Health Surveys</a
                  >
                </div>
              </div>
              <div class="survey-stats">
                <span>Created on: Mar 17, 2020</span>
                <span>Last modified: Mar 17, 2020</span>
                <span>Views: 3320</span>
              </div>
            </div>
          </div>
        </div>
        <div class="document-row" data-url="#" title="View study">
          <div class="row">
            <div class="col-3 col-lg-3">
              <img
                src="/static/files/doc_thumb.png"
                title="document thumbnail"
                alt="document thumbnail"
              />
            </div>
            <div class="col-9 col-lg-9">
              <span class="badge badge-primary wbg-badge">DOCUMENT</span>
              <h5 class="title">
                <a
                  href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                  title="Service Provision Assessment Survey 2018-2019"
                  >Service Provision Assessment Survey 2018-2019</a
                >
              </h5>
              <div class="study-country">Afghanistan, 2018-2019</div>
              <div class="study-id d-md-flex mt-2">
                <span class="badge badge-pill badge-secondary"
                  >ID: wb_17427272</span
                >
                <div class="small ml-md-3 mt-2 mt-md-0">
                  Rank: 1, Score: 0.1723729397
                </div>
              </div>
              <div class="study-meta d-flex">
                <div class="small mt-2 mb-2 mr-3">
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/"
                    ><i class="fas fa-database mr-1" aria-hidden="true"></i
                    >Metadata</a
                  >
                </div>
                <div class="small mt-2 mb-2">
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/"
                    ><i
                      class="fas fa-chart-bar fa-lg mr-1"
                      aria-hidden="true"
                    ></i
                    >Topics</a
                  >
                </div>
              </div>
              <div class="sub-title">
                <div>
                  <span class="study-by">Ministry of Public Health</span>
                </div>
                <div class="owner-collection">
                  Collection:
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                    >MEASURE DHS: Demographic and Health Surveys</a
                  >
                </div>
              </div>
              <div class="survey-stats">
                <span>Created on: Mar 17, 2020</span>
                <span>Last modified: Mar 17, 2020</span>
                <span>Views: 3320</span>
              </div>
            </div>
          </div>
        </div>
        <div class="document-row" data-url="#" title="View study">
          <div class="row">
            <div class="col-3 col-lg-3">
              <img
                src="/static/files/doc_thumb.png"
                title="document thumbnail"
                alt="document thumbnail"
              />
            </div>
            <div class="col-9 col-lg-9">
              <span class="badge badge-primary wbg-badge">DOCUMENT</span>
              <h5 class="title">
                <a
                  href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                  title="Service Provision Assessment Survey 2018-2019"
                  >Service Provision Assessment Survey 2018-2019</a
                >
              </h5>
              <div class="study-country">Afghanistan, 2018-2019</div>
              <div class="study-id d-md-flex mt-2">
                <span class="badge badge-pill badge-secondary"
                  >ID: wb_17427272</span
                >
                <div class="small ml-md-3 mt-2 mt-md-0">
                  Rank: 1, Score: 0.1723729397
                </div>
              </div>
              <div class="study-meta d-flex">
                <div class="small mt-2 mb-2 mr-3">
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/"
                    ><i class="fas fa-database mr-1" aria-hidden="true"></i
                    >Metadata</a
                  >
                </div>
                <div class="small mt-2 mb-2">
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/"
                    ><i
                      class="fas fa-chart-bar fa-lg mr-1"
                      aria-hidden="true"
                    ></i
                    >Topics</a
                  >
                </div>
              </div>
              <div class="sub-title">
                <div>
                  <span class="study-by">Ministry of Public Health</span>
                </div>
                <div class="owner-collection">
                  Collection:
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                    >MEASURE DHS: Demographic and Health Surveys</a
                  >
                </div>
              </div>
              <div class="survey-stats">
                <span>Created on: Mar 17, 2020</span>
                <span>Last modified: Mar 17, 2020</span>
                <span>Views: 3320</span>
              </div>
            </div>
          </div>
        </div>
        <div class="document-row" data-url="#" title="View study">
          <div class="row">
            <div class="col-3 col-lg-3">
              <img
                src="/static/files/doc_thumb.png"
                title="document thumbnail"
                alt="document thumbnail"
              />
            </div>
            <div class="col-9 col-lg-9">
              <span class="badge badge-primary wbg-badge">DOCUMENT</span>
              <h5 class="title">
                <a
                  href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                  title="Service Provision Assessment Survey 2018-2019"
                  >Service Provision Assessment Survey 2018-2019</a
                >
              </h5>
              <div class="study-country">Afghanistan, 2018-2019</div>
              <div class="study-id d-md-flex mt-2">
                <span class="badge badge-pill badge-secondary"
                  >ID: wb_17427272</span
                >
                <div class="small ml-md-3 mt-2 mt-md-0">
                  Rank: 1, Score: 0.1723729397
                </div>
              </div>
              <div class="study-meta d-flex">
                <div class="small mt-2 mb-2 mr-3">
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/"
                    ><i class="fas fa-database mr-1" aria-hidden="true"></i
                    >Metadata</a
                  >
                </div>
                <div class="small mt-2 mb-2">
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/"
                    ><i
                      class="fas fa-chart-bar fa-lg mr-1"
                      aria-hidden="true"
                    ></i
                    >Topics</a
                  >
                </div>
              </div>
              <div class="sub-title">
                <div>
                  <span class="study-by">Ministry of Public Health</span>
                </div>
                <div class="owner-collection">
                  Collection:
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                    >MEASURE DHS: Demographic and Health Surveys</a
                  >
                </div>
              </div>
              <div class="survey-stats">
                <span>Created on: Mar 17, 2020</span>
                <span>Last modified: Mar 17, 2020</span>
                <span>Views: 3320</span>
              </div>
            </div>
          </div>
        </div>
        <div class="document-row" data-url="#" title="View study">
          <div class="row">
            <div class="col-3 col-lg-3">
              <img
                src="/static/files/doc_thumb.png"
                title="document thumbnail"
                alt="document thumbnail"
              />
            </div>
            <div class="col-9 col-lg-9">
              <span class="badge badge-primary wbg-badge">DOCUMENT</span>
              <h5 class="title">
                <a
                  href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                  title="Service Provision Assessment Survey 2018-2019"
                  >Service Provision Assessment Survey 2018-2019</a
                >
              </h5>
              <div class="study-country">Afghanistan, 2018-2019</div>
              <div class="study-id d-md-flex mt-2">
                <span class="badge badge-pill badge-secondary"
                  >ID: wb_17427272</span
                >
                <div class="small ml-md-3 mt-2 mt-md-0">
                  Rank: 1, Score: 0.1723729397
                </div>
              </div>
              <div class="study-meta d-flex">
                <div class="small mt-2 mb-2 mr-3">
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/"
                    ><i class="fas fa-database mr-1" aria-hidden="true"></i
                    >Metadata</a
                  >
                </div>
                <div class="small mt-2 mb-2">
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/"
                    ><i
                      class="fas fa-chart-bar fa-lg mr-1"
                      aria-hidden="true"
                    ></i
                    >Topics</a
                  >
                </div>
              </div>
              <div class="sub-title">
                <div>
                  <span class="study-by">Ministry of Public Health</span>
                </div>
                <div class="owner-collection">
                  Collection:
                  <a
                    href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                    >MEASURE DHS: Demographic and Health Surveys</a
                  >
                </div>
              </div>
              <div class="survey-stats">
                <span>Created on: Mar 17, 2020</span>
                <span>Last modified: Mar 17, 2020</span>
                <span>Views: 3320</span>
              </div>
            </div>
          </div>
        </div> -->
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
                <ul class="pagination pagination-md wbg-pagination-ul small">
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
                href="https://www.facebook.com/sharer/sharer.php?u=%2fexplore%2fsubcategories%2ffiltering_by_topic_share%2f"
                title="Share on Facebook"
                ><span class="fab fa-facebook-f fa-lg" aria-hidden="true"></span
              ></a>
              <a
                class="nav-item"
                href="https://www.linkedin.com/shareArticle?mini=true&amp;url=%2fexplore%2fsubcategories%2ffiltering_by_topic_share%2f"
                title="Share on LinkedIn"
                ><span
                  class="fab fa-linkedin-in fa-lg"
                  aria-hidden="true"
                ></span
              ></a>
              <a
                class="nav-item"
                href="https://twitter.com/intent/tweet?url=%2fexplore%2fsubcategories%2ffiltering_by_topic_share%2f&amp;text=Filtering%20by%20topic%20share"
                title="Tweet this"
                ><span class="fab fa-twitter fa-lg" aria-hidden="true"></span
              ></a>
            </nav>
          </section>
        </footer>
      </article>
    </div>
  </div>
</template>

<script>
import FilterTable from "../../common/FilterTable";
import SearchResultCard from "../../common/SearchResultCard";

export default {
  name: "FilterTopicShare",
  props: {
    page_title: String,
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
  },
  components: {
    FilterTable,
    SearchResultCard,
  },
  data: function () {
    return {
      nlp_api_url: "/nlp/models/lda",
      page_sizes: [10, 25, 50, 100],
      start: 0,
      end: 0,
      next: 0,
      curr_page_num: 0,
      curr_size: 10,
      num_pages: 0,
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
    submitTopicSearch(filterPanelData) {
      this.model_id = filterPanelData.model_id;
      this.topic_percentage = {};
      Object.assign(this.topic_percentage, filterPanelData.topic_value);
      Object.entries(this.topic_percentage).forEach(
        ([key, val]) => (this.topic_percentage[key] = val / 100)
      );

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
        .finally(() => (this.hits_loading = false));
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
