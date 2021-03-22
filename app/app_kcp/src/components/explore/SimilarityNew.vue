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
        <h2>Heading two</h2>
        <p class="lead">
          Describe how we measure similarity between documents. Then provide the
          possibility to copy a document, or provide the URL of a TXT, DOC or
          PDF document (from our own catalog or external). The system should
          return (i) a list of N closest matches, and (ii) the topic composition
          for LDA model X.
        </p>
        <p>
          Describe how we measure similarity between documents. Then provide the
          possibility to copy a document, or provide the URL of a TXT, DOC or
          PDF document (from our own catalog or external). The system should
          return (i) a list of N closest matches, and (ii) the topic composition
          for LDA model X.
        </p>
        <div class="d-md-flex">
          <!-- <div class="dropdown mr-3 mr-3 mb-3 mb-md-0">
            <button
              class="btn btn-outline-secondary wbg-button dropdown-toggle"
              type="button"
              id="dropdownMenuButton"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Word2vec Model ALL_50
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
              <a
                class="dropdown-item"
                href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                >Action</a
              >
              <a
                class="dropdown-item"
                href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                >Another action</a
              >
              <a
                class="dropdown-item"
                href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                >Something else here</a
              >
            </div>
          </div>
          <div class="dropdown">
            <button
              class="btn btn-outline-secondary wbg-button dropdown-toggle"
              type="button"
              id="dropdownMenuButton"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              LDA Model ALL_50
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
              <a
                class="dropdown-item"
                href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                >Action</a
              >
              <a
                class="dropdown-item"
                href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                >Another action</a
              >
              <a
                class="dropdown-item"
                href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                >Something else here</a
              >
            </div>
          </div> -->
        </div>
        <div class="row">
          <div class="col-6 fluid">
            <MLModelSelect
              @modelSelected="onModelSelect"
              :model_name="'word2vec'"
              placeholder="Choose a word embedding model..."
            />
          </div>
          <div class="col-6 fluid">
            <MLModelSelect
              @modelSelected="onModelSelect"
              :model_name="'lda'"
              placeholder="Choose a topic model..."
            />
          </div>
        </div>
        <form class="mt-4">
          <div class="form-group">
            <label for="exampleFormControlFile1"
              ><strong>Choose PDF or TXT file</strong></label
            >
            <input
              type="file"
              class="form-control-file"
              id="exampleFormControlFile1"
            />
          </div>
          <label class="sr-only" for="inlineFormInputGroup"
            >Enter URL of PDF or TXT file</label
          >
          <div class="input-group mb-2">
            <div class="input-group-prepend">
              <div class="input-group-text">
                <i class="fas fa-link fa-md" aria-hidden="true"></i>
              </div>
            </div>
            <input
              type="text"
              class="form-control"
              id="inlineFormInputGroup"
              placeholder="Enter URL of file"
            />
          </div>
          <br /><a
            href="https://mtt-wb21h.netlify.app/explore/similarity/#"
            class="btn btn-primary wbg-button"
            role="button"
            aria-pressed="true"
            >Find similar documents</a
          >
        </form>
        <br />
        <h3 class="mt-4 mb-3">Comparison of results</h3>
        <ul class="nav nav-tabs" id="myTab" role="tablist">
          <li class="nav-item">
            <a
              class="nav-link active"
              id="home-tab"
              data-toggle="tab"
              href="https://mtt-wb21h.netlify.app/explore/similarity/#home"
              role="tab"
              aria-controls="home"
              aria-selected="true"
              >Model 1</a
            >
          </li>
          <li class="nav-item">
            <a
              class="nav-link"
              id="profile-tab"
              data-toggle="tab"
              href="https://mtt-wb21h.netlify.app/explore/similarity/#profile"
              role="tab"
              aria-controls="profile"
              aria-selected="false"
              >Model 2</a
            >
          </li>
        </ul>
        <div class="tab-content" id="myTabContent">
          <div
            class="tab-pane fade show active"
            id="home"
            role="tabpanel"
            aria-labelledby="home-tab"
          >
            <h4 class="mt-4">Model 1 results</h4>
            <div
              class="document-row"
              data-url="https://microdata.worldbank.org/index.php/catalog/3645"
              title="View study"
            >
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
                      href="https://microdata.worldbank.org/index.php/catalog/3645"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a
                        href="https://microdata.worldbank.org/index.php/catalog/dhs"
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
            <div
              class="document-row"
              data-url="https://microdata.worldbank.org/index.php/catalog/3645"
              title="View study"
            >
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
                      href="https://microdata.worldbank.org/index.php/catalog/3645"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a
                        href="https://microdata.worldbank.org/index.php/catalog/dhs"
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
            <div
              class="document-row"
              data-url="https://microdata.worldbank.org/index.php/catalog/3645"
              title="View study"
            >
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
                      href="https://microdata.worldbank.org/index.php/catalog/3645"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a
                        href="https://microdata.worldbank.org/index.php/catalog/dhs"
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
            <div
              class="document-row"
              data-url="https://microdata.worldbank.org/index.php/catalog/3645"
              title="View study"
            >
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
                      href="https://microdata.worldbank.org/index.php/catalog/3645"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a
                        href="https://microdata.worldbank.org/index.php/catalog/dhs"
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
            <div
              class="document-row"
              data-url="https://microdata.worldbank.org/index.php/catalog/3645"
              title="View study"
            >
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
                      href="https://microdata.worldbank.org/index.php/catalog/3645"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a
                        href="https://microdata.worldbank.org/index.php/catalog/dhs"
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
                <div class="col-12 col-lg-12 d-flex justify-content-lg-end">
                  <nav aria-label="Page navigation">
                    <ul
                      class="pagination pagination-md wbg-pagination-ul small"
                    >
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                          class="page-link active"
                          data-page="1"
                          >1</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                          class="page-link"
                          data-page="2"
                          >2</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                          class="page-link"
                          data-page="3"
                          >3</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                          class="page-link"
                          data-page="4"
                          >4</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                          class="page-link"
                          data-page="5"
                          >5</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                          class="page-link"
                          data-page="2"
                          >Next</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
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
          </div>
          <div
            class="tab-pane fade"
            id="profile"
            role="tabpanel"
            aria-labelledby="profile-tab"
          >
            <h4 class="mt-4">Model 2 results</h4>
            <div
              class="document-row"
              data-url="https://microdata.worldbank.org/index.php/catalog/3645"
              title="View study"
            >
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
                      href="https://microdata.worldbank.org/index.php/catalog/3645"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a
                        href="https://microdata.worldbank.org/index.php/catalog/dhs"
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
            <div
              class="document-row"
              data-url="https://microdata.worldbank.org/index.php/catalog/3645"
              title="View study"
            >
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
                      href="https://microdata.worldbank.org/index.php/catalog/3645"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a
                        href="https://microdata.worldbank.org/index.php/catalog/dhs"
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
            <div
              class="document-row"
              data-url="https://microdata.worldbank.org/index.php/catalog/3645"
              title="View study"
            >
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
                      href="https://microdata.worldbank.org/index.php/catalog/3645"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a
                        href="https://microdata.worldbank.org/index.php/catalog/dhs"
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
            <div
              class="document-row"
              data-url="https://microdata.worldbank.org/index.php/catalog/3645"
              title="View study"
            >
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
                      href="https://microdata.worldbank.org/index.php/catalog/3645"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a
                        href="https://microdata.worldbank.org/index.php/catalog/dhs"
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
            <div
              class="document-row"
              data-url="https://microdata.worldbank.org/index.php/catalog/3645"
              title="View study"
            >
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
                      href="https://microdata.worldbank.org/index.php/catalog/3645"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a
                        href="https://microdata.worldbank.org/index.php/catalog/dhs"
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
                <div class="col-12 col-lg-12 d-flex justify-content-lg-end">
                  <nav aria-label="Page navigation">
                    <ul
                      class="pagination pagination-md wbg-pagination-ul small"
                    >
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                          class="page-link active"
                          data-page="1"
                          >1</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                          class="page-link"
                          data-page="2"
                          >2</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                          class="page-link"
                          data-page="3"
                          >3</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                          class="page-link"
                          data-page="4"
                          >4</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                          class="page-link"
                          data-page="5"
                          >5</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                          class="page-link"
                          data-page="2"
                          >Next</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          href="https://mtt-wb21h.netlify.app/explore/similarity/#"
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
          </div>
        </div>
        <hr />
        <PageFooter :url="share_url" :share_text="share_text" />
      </article>
    </div>
  </div>
</template>

<script>
import MLModelSelect from "../common/MLModelSelect";

import PageFooter from "../common/PageFooter";

export default {
  name: "SimilarityNew",
  props: {
    page_title: String,
    share_url: String,
    share_text: String,
  },
  components: { PageFooter, MLModelSelect },
  methods: {
    onModelSelect() {},
  },
};
</script>
