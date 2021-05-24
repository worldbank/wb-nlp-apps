<template>
  <div>
    <header class="blog-header wbg-internal-header">
      <div class="container">
        <div class="col-12 mb-2">
          <div id="breadcrumbs">
            <router-link to="/">Home</router-link>
            <span class="wbg-breadcrumb-separator">/</span>
            <router-link to="/about">About</router-link>
          </div>
        </div>
        <div class="col-12">
          <i class="fas fa-search fa-2x" aria-hidden="true"></i>
          <h1>About</h1>
        </div>
      </div>
    </header>
    <div class="container flowing">
      <div class="row justify-content-md-center">
        <div class="col-sm-8 blog-main">
          <article class="blog-post">
            <div class="content-row text-justify">
              <p>
                The Document Explorer was developed to demonstrate the benefits
                and use of Natural Language Processing (NLP) topic and word
                embedding models to improve document and data discoverability.
                The models were used to implement a
                <router-link
                  :to="{
                    name: 'search',
                    params: {
                      search_text: 'climate change',
                      search_type: 'semantic',
                      page: 1,
                    },
                  }"
                >
                  semantic search</router-link
                >
                engine and to generate summary, structured information on the
                <router-link to="/explore/topic-composition/"
                  >thematic</router-link
                >
                and
                <router-link to="/explore/subcategories/geographic-coverage/"
                  >geographic</router-link
                >
                composition of a large corpus of documents. We also seek to
                identify the closeness between documents and datasets including
                time series of indicators from the World Bank Development
                Indicators and the United Nations Sustainable Development Goals
                database.
              </p>
              <p>
                A GitHub repository provides open access to the scripts produced
                to prepare the documents for modeling and to fit our NLP models.
              </p>
              <p>The project relied exclusively on open source solutions.</p>
              <p>
                The ultimate goal of the project was to contribute to a broader
                project aiming to develop a better search engine for data (of
                all types) with semantic capability and a recommender system.
              </p>
              <p>The Grant financed the following activities:</p>

              <ul>
                <li>
                  <bold
                    >Building a large corpus of documents on development
                    issues.</bold
                  >
                  World Bank documents can easily be accessed via API (<a
                    href="https://documents.worldbank.org/en/publication/documents-reports"
                    target="_blank"
                    >Documents and Reports website</a
                  >). For other sources, web scrapers were developed (scrapers
                  are the only components of the project that we do not make
                  openly accessible, to avoid risks of abusive use).
                </li>
                <li>
                  <bold>Pre-processing of documents.</bold> To be used as input
                  for machine learning models, the documents must be
                  transformed. A pipeline of procedures (involving pdf-to-text
                  conversion, spell checking, stop-words suppression, n-grams
                  detection, lemmatization, tokenization, part-of-speech
                  tagging, metadata generation, acronyms detection and
                  conversion, named entity recognition, and more) has been
                  developed.
                </li>
                <li>
                  <bold>Fitting models.</bold> Latent Dirichlet Allocation (LDA)
                  topic models, and word2vec (word embedding models) were
                  trained on the multi-source corpus. The models are published
                  on GitHub. An API was developed to make the model inferencers
                  openly accessible.
                </li>
                <li>
                  <bold>Design of the dissemination platform.</bold> The Grant
                  co-financed the development of the Document Explorer.
                </li>
                <li>
                  <bold>Documentation and dissemination of outputs.</bold> All
                  outputs (including replicable scripts) of the project have
                  been documented, packaged and published in a GitHub repository
                  to allow adaptation, re-purposing, and use by third parties.
                </li>
              </ul>

              <br />
              <p class="lead"><i>ACKNOWLEDGMENTS</i></p>

              <p>
                The Document Explorer, and the related GitHub repository, are
                the main output of a project implemented by the World Bank
                Development Data Group, funded by the
                <i>Innovation in Data Production, Analysis and Dissemination</i>
                window of the
                <a
                  href="https://www.worldbank.org/en/programs/knowledge-for-change"
                  target="_blank"
                  >Knowledge for Change III (KCP) program</a
                >
                (project P173741-NLP for Development Knowledge). The project was
                implemented from March 2020 to March 2021. KCP funding was
                complemented by the Development Data Group’s administrative
                budget, and by a Grant from the UNHCR-World Bank
                <a href="https://www.jointdatacenter.org/" target="_blank"
                  >Joint Data Center on Forced Displacement</a
                >
                (JDC – project P174148-Machine Learning for Refugee Data
                Center). The JDC Grant is used to develop a specific tool to
                identify, publish and analyze a corpus of documents related to
                forced displacement (work in progress).
              </p>

              <p>
                The project was implemented by a team at the World Bank
                Development Data Group (Analytics and Tools Unit) composed of
                (by alphabetical order):
              </p>
              <ul>
                <li>
                  Aivin Solatorio, Data Scientist (expert in Natural Language
                  Processing; main developer of the processing and modeling
                  pipeline, and coordinator of the Document Explorer website
                  development)
                </li>
                <li>
                  Dharana Rijal, consultant (development of web scrapers for
                  document acquisition)
                </li>
                <li>
                  Mehmood Asghar, Senior Data Engineer (support to web
                  development, web scraping, and database applications)
                </li>
                <li>Olivier Dupriez, Senior Adviser (project manager)</li>
              </ul>

              <p>
                <a href="https://www.morethanthemes.com/" target="_blank"
                  >MoreThanThemes</a
                >
                (consultants) contributed to the design of the website.
              </p>
              <p>
                The project benefited considerably from the availability of
                multiple open source solutions for the acquisition, processing,
                modeling of documents, for the production of visualizations, and
                for dissemination of the output. The tools we used are listed in
                the Methods and Tools. We are very grateful to all identified
                and anonymous developers and contributors to these solutions.
              </p>
            </div>
            <hr />
            <footer>
              <section>
                <h4>Share</h4>
                <nav class="nav sharing-icons mt-4">
                  <a
                    class="nav-item"
                    href="https://www.facebook.com/sharer/sharer.php?u=%2fabout%2f"
                    title="Share on Facebook"
                    ><span
                      class="fab fa-facebook-f fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://www.linkedin.com/shareArticle?mini=true&amp;url=%2fabout%2f"
                    title="Share on LinkedIn"
                    ><span
                      class="fab fa-linkedin-in fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://twitter.com/intent/tweet?url=%2fabout%2f&amp;text=About"
                    title="Tweet this"
                    ><span
                      class="fab fa-twitter fa-lg"
                      aria-hidden="true"
                    ></span
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

export default {
  name: "Explore",
  components: {},
  mounted() {
    // this.flowSideBar();
  },
  computed: {},
  methods: {
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