<template>
  <div>
    <header class="blog-header wbg-internal-header">
      <div class="container">
        <div class="col-12 mb-2">
          <div id="breadcrumbs">
            <router-link to="/">Home</router-link>
            <span class="wbg-breadcrumb-separator">/</span>
            <router-link to="/explore">Explore</router-link>
            <span class="wbg-breadcrumb-separator">/</span>
            <router-link to="/explore">Explore</router-link>
          </div>
        </div>
        <div class="col-12">
          <i class="fas fa-search fa-2x" aria-hidden="true"></i>
          <h1>Explore</h1>
          <p>
            Describes the sources and coverage of our corpus, provides
            interactive visualizations of topic composition (extracted from LDA
            models), and allows you to filter documents by their topic
            composition. Also provides access to word embedding models,
            similarity measures, and others.
          </p>
        </div>
      </div>
    </header>
    <div class="container flowing">
      <button
        class="sidebar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#blog-sidebar"
        aria-controls="blog-sidebar"
        aria-expanded="true"
        aria-label="Toggle sidebar"
      >
        <i class="fas fa-compress"></i>
        <i class="fas fa-expand"></i>
      </button>

      <div class="row">
        <aside class="col-sm-3 blog-sidebar" id="blog-sidebar">
          <section class="sidebar-module">
            <ol class="list-unstyled">
              <li>
                <router-link to="/explore/corpus/">Corpus</router-link>
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/sources/"
                  class="wbg_sidebar second-level"
                  >Sources and volume</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/geographic-coverage/"
                  class="wbg_sidebar second-level"
                  >Geographic coverage</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/metadata/"
                  class="wbg_sidebar second-level"
                  >Metadata</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/training-subset/"
                  class="wbg_sidebar second-level"
                  >Training subset</router-link
                >
              </li>
              <li>
                <router-link to="/explore/topic-composition/"
                  >Topic composition</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/topic-browser/"
                  class="wbg_sidebar second-level"
                  >Topic browser</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/filtering-by-topic-share/"
                  class="wbg_sidebar second-level"
                  >Filtering by topic share</router-link
                >
              </li>
              <li>
                <router-link to="/explore/topic-profiles/"
                  >Topic profiles</router-link
                >
              </li>
              <li>
                <router-link to="/explore/topic-taxonomy/"
                  >Topic taxonomy</router-link
                >
              </li>
              <li>
                <router-link to="/explore/topic-relationships/"
                  >Topic relationships</router-link
                >
              </li>
              <li>
                <router-link to="/explore/word-embeddings/"
                  >Word embeddings</router-link
                >
              </li>
              <li>
                <router-link to="/explore/similarity/">Similarity</router-link>
              </li>
              <li>
                <router-link to="/explore/knowledge-page-service/"
                  >Knowledge page service</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/example/"
                  class="wbg_sidebar second-level"
                  >Example</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/instructions/"
                  class="wbg_sidebar second-level"
                  >Instructions</router-link
                >
              </li>
            </ol>
          </section>
        </aside>
        <div class="col blog-main">
          <article class="blog-post">
            <div class="content-row">
              <router-view></router-view>
            </div>
            <hr />
            <footer>
              <section>
                <h4>Share</h4>
                <nav class="nav sharing-icons mt-4">
                  <a
                    class="nav-item"
                    href="https://www.facebook.com/sharer/sharer.php?u=%2fexplore%2fexplore%2f"
                    title="Share on Facebook"
                    ><span
                      class="fab fa-facebook-f fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://www.linkedin.com/shareArticle?mini=true&amp;url=%2fexplore%2fexplore%2f"
                    title="Share on LinkedIn"
                    ><span
                      class="fab fa-linkedin-in fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://twitter.com/intent/tweet?url=%2fexplore%2fexplore%2f&amp;text=Explore"
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
    this.flowSideBar();
  },
  computed: {
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
  methods: {
    flowSideBar: function () {
      $(function () {
        var $sidebar = $(".blog-sidebar"),
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

.blog-header {
  margin-bottom: 0.5rem;
}

.sidebar-toggler {
  border: none;
  padding: 0;
  color: black;
  border-color: transparent;
  background-color: transparent;
}

button[aria-expanded="true"] .fa-expand {
  display: none;
}
button[aria-expanded="false"] .fa-compress {
  display: none;
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