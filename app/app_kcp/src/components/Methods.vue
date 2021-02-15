<template>
  <div>
    <header class="blog-header wbg-internal-header">
      <div class="container">
        <div class="col-12 mb-2">
          <div id="breadcrumbs">
            <router-link to="/">Home</router-link>
            <span class="wbg-breadcrumb-separator">/</span>
            <router-link to="/methods">Methods &amp; Tools</router-link>
            <span class="wbg-breadcrumb-separator">/</span>
            <router-link to="/methods">Methods &amp; Tools</router-link>
          </div>
        </div>
        <div class="col-12">
          <i class="fas fa-search fa-2x" aria-hidden="true"></i>
          <h1>Methods &amp; Tools</h1>
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
      <!-- <div class=""> -->
      <div class="row">
        <aside class="col-sm-3 blog-sidebar" id="blog-sidebar">
          <section class="sidebar-module">
            <ol class="list-unstyled">
              <li>
                <router-link to="/methods/corpus/">Corpus</router-link>
              </li>
              <li>
                <router-link
                  to="/methods/subcategories/sources/"
                  class="wbg_sidebar second-level"
                  >Sources and volume</router-link
                >
              </li>
              <li>
                <router-link
                  to="/methods/subcategories/geographic-coverage/"
                  class="wbg_sidebar second-level"
                  >Geographic coverage</router-link
                >
              </li>
              <li>
                <router-link
                  to="/methods/subcategories/metadata/"
                  class="wbg_sidebar second-level"
                  >Metadata</router-link
                >
              </li>
              <li>
                <router-link
                  to="/methods/subcategories/training-subset/"
                  class="wbg_sidebar second-level"
                  >Training subset</router-link
                >
              </li>
              <li>
                <router-link to="/methods/topic-composition/"
                  >Topic composition</router-link
                >
              </li>
              <li>
                <router-link
                  to="/methods/subcategories/topic-browser/"
                  class="wbg_sidebar second-level"
                  >Topic browser</router-link
                >
              </li>
              <li>
                <router-link
                  to="/methods/subcategories/filtering-by-topic-share/"
                  class="wbg_sidebar second-level"
                  >Filtering by topic share</router-link
                >
              </li>
              <li>
                <router-link to="/methods/topic-profiles/"
                  >Topic profiles</router-link
                >
              </li>
              <li>
                <router-link to="/methods/topic-taxonomy/"
                  >Topic taxonomy</router-link
                >
              </li>
              <li>
                <router-link to="/methods/topic-relationships/"
                  >Topic relationships</router-link
                >
              </li>
              <li>
                <router-link to="/methods/word-embeddings/"
                  >Word embeddings</router-link
                >
              </li>
              <li>
                <router-link to="/methods/similarity/">Similarity</router-link>
              </li>
              <li>
                <router-link to="/methods/knowledge-page-service/"
                  >Knowledge page service</router-link
                >
              </li>
              <li>
                <router-link
                  to="/methods/subcategories/example/"
                  class="wbg_sidebar second-level"
                  >Example</router-link
                >
              </li>
              <li>
                <router-link
                  to="/methods/subcategories/instructions/"
                  class="wbg_sidebar second-level"
                  >Instructions</router-link
                >
              </li>
            </ol>
          </section>
        </aside>
        <div class="col-sm-9 blog-main">
          <article class="blog-post">
            <!-- <header>
              <h1 class="blog-post-title mb-3" dir="auto">
                <a href="/methods/methods/"
                  >Methods &amp; Tools</a
                >
              </h1>
            </header>
            <p>Methods &amp; Tools</p> -->
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
                    href="https://twitter.com/intent/tweet?url=%2fexplore%2fexplore%2f&amp;text=Methods &amp; Tools"
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
  name: "Methods &amp; Tools",
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