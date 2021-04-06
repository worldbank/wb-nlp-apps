<template>
  <div>
    <header class="blog-header wbg-internal-header">
      <div class="container">
        <div class="col-12 mb-2">
          <div id="breadcrumbs">
            <router-link to="/">Home</router-link>
            <span class="wbg-breadcrumb-separator">/</span>
            <router-link to="/methods">Methods</router-link>
            <span class="wbg-breadcrumb-separator">/</span>
            <router-link to="/methods">Methods</router-link>
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
    <div class="container">
      <div class="row">
        <aside class="col-sm-3 blog-sidebar">
          <section class="sidebar-module">
            <ol class="list-unstyled">
              <li>
                <router-link to="/methods">Methods &amp; Tools</router-link>
              </li>
              <li>
                <router-link to="/methods/text-acquisition"
                  >Text acquisition</router-link
                >
              </li>
              <li>
                <router-link to="/methods/text-preparation"
                  >Text preparation</router-link
                >
              </li>
              <li>
                <router-link to="/methods/lda">LDA Topic Model</router-link>
              </li>
              <li>
                <router-link to="/methods/word-embeddings"
                  >Word embeddings</router-link
                >
              </li>
              <li>
                <router-link to="/methods/topic-classification"
                  >Topic classification</router-link
                >
              </li>
              <li>
                <router-link to="/methods/cataloguing">Cataloguing</router-link>
              </li>
              <li>
                <router-link to="/methods/search-engine"
                  >Search engine</router-link
                >
              </li>
              <li>
                <router-link to="/methods/visualizations"
                  >Visualizations</router-link
                >
              </li>
              <li>
                <router-link to="/methods/training-materials"
                  >Training materials</router-link
                >
              </li>
            </ol>
          </section>
        </aside>
        <div class="col-sm-9 blog-main">
          <article class="blog-post">
            <!-- <header>
              <h1 class="blog-post-title mb-3" dir="auto">
                <a href="https://mtt-wb21h.netlify.app/methods/methods/"
                  >Methods &amp; Tools</a
                >
              </h1>
            </header>
            <p>
              Brief introduction on the tools and methods we use, on our
              commitment to be reproducible and open (and to only use
              open-source solutions), on the value of our scripts as training
              materials, etc.
            </p>
            <p>
              Provide link to GitHub repo, invite feedback, describe licenses.
            </p> -->

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
                    href="https://www.facebook.com/sharer/sharer.php?u=%2fmethods%2fmethods%2f"
                    title="Share on Facebook"
                    ><span
                      class="fab fa-facebook-f fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://www.linkedin.com/shareArticle?mini=true&amp;url=%2fmethods%2fmethods%2f"
                    title="Share on LinkedIn"
                    ><span
                      class="fab fa-linkedin-in fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://twitter.com/intent/tweet?url=%2fmethods%2fmethods%2f&amp;text=Methods%20%26%20Tools"
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