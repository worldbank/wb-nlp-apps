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
        <h3 class="mb-3 mt-5">Available topics</h3>
        <p class="mt-2">You can choose up to three topics</p>
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
                tourism, conflict, south, migration, migrant, security,
                economic, country, west, community
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
                tourism, conflict, south, migration, migrant, security,
                economic, country, west, community
              </td>
            </tr>
          </tbody>
        </table>
        <h3 class="mb-3 mt-5">Select a topic</h3>
        <form>
          <div class="row align-items-center">
            <div class="col-12 col-md-3">
              <h5>Topic 0</h5>
            </div>
            <div class="col-12 col-md-9">
              <div class="form-group mt-2 mb-3">
                <label for="formControlRange" class="small">Range 0%-71%</label>
                <input
                  type="range"
                  class="form-control-range"
                  id="formControlRange"
                  min="10"
                  max="1000"
                  step="10"
                />
              </div>
            </div>
          </div>
          <hr />
          <div class="row align-items-center">
            <div class="col-12 col-md-3">
              <h5>Topic 2</h5>
            </div>
            <div class="col-12 col-md-9">
              <div class="form-group mt-2 mb-3">
                <label for="formControlRange" class="small">Range 0%-71%</label>
                <input
                  type="range"
                  class="form-control-range"
                  id="formControlRange"
                  min="10"
                  max="1000"
                  step="10"
                />
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-12">
              <button
                type="button"
                class="btn btn-link btn-sm wbg-button-danger"
              >
                <i class="fas fa-trash fa-sm mr-2" aria-hidden="true"></i>Remove
                topic
              </button>
            </div>
          </div>
        </form>
        <div class="row mb-4">
          <div class="col-12">
            <hr />
            <button type="button" class="btn btn-primary btn-lg wbg-button">
              <i class="fas fa-search fa-sm mr-1" aria-hidden="true"></i>Search
            </button>
            <hr />
          </div>
        </div>
        <h2>Filtering Results</h2>
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
        </div>
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
                  >Results per page
                  <span class="wbg-pagination-btn active">15</span>
                  <span class="wbg-pagination-btn">30</span>
                  <span class="wbg-pagination-btn">50</span>
                  <span class="wbg-pagination-btn">100</span></small
                >
              </div>
            </div>
            <div class="col-12 col-lg-6 d-flex justify-content-lg-end">
              <nav aria-label="Page navigation">
                <ul class="pagination pagination-md wbg-pagination-ul small">
                  <li class="page-item">
                    <a
                      href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                      class="page-link active"
                      data-page="1"
                      >1</a
                    >
                  </li>
                  <li class="page-item">
                    <a
                      href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                      class="page-link"
                      data-page="2"
                      >2</a
                    >
                  </li>
                  <li class="page-item">
                    <a
                      href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                      class="page-link"
                      data-page="3"
                      >3</a
                    >
                  </li>
                  <li class="page-item">
                    <a
                      href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                      class="page-link"
                      data-page="4"
                      >4</a
                    >
                  </li>
                  <li class="page-item">
                    <a
                      href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                      class="page-link"
                      data-page="5"
                      >5</a
                    >
                  </li>
                  <li class="page-item">
                    <a
                      href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                      class="page-link"
                      data-page="2"
                      >Next</a
                    >
                  </li>
                  <li class="page-item">
                    <a
                      href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/#"
                      class="page-link"
                      data-page="218"
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

export default {
  name: "FilterTopicShare",
  props: {
    page_title: String,
  },
  mounted () {
    window.vm = this;
  },
  components: {
    FilterTable,
  },
  data: function () {
    return {
      date_now: new Date().toDateString(),
      corpus_size: 200000,
      org_count: 14,
      total_tokens: 1029000000,
    };
  },
  methods: {
    submitTopicSearch(topicValue) {
      this.topic_value = topicValue;
    }
  }
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
