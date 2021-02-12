<template>
  <div>
    <header class="blog-header wbg-internal-header">
      <div class="container">
        <div class="col-12 mb-2">
          <div id="breadcrumbs">
            <a href="/">Home</a>
            <span class="wbg-breadcrumb-separator">/</span>
            <a href="/explore">Explore</a>
            <span class="wbg-breadcrumb-separator">/</span>
            <a href="/explore">Explore</a>
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
      <!-- <div class=""> -->
      <div class="row">
        <aside class="col-sm-2 blog-sidebar">
          <h4>Explore sidebar</h4>
          <section class="sidebar-module">
            <ol class="list-unstyled">
              <li>
                <a href="/explore/explore/">Explore</a>
              </li>
              <li>
                <a
                  href="/explore/subcategories/sources/"
                  class="wbg_sidebar second-level"
                  >Sources</a
                >
              </li>
              <li>
                <a
                  href="/explore/subcategories/geographic-coverage/"
                  class="wbg_sidebar second-level"
                  >Geographic coverage</a
                >
              </li>
              <li>
                <a
                  href="/explore/subcategories/metadata/"
                  class="wbg_sidebar second-level"
                  >Metadata</a
                >
              </li>
              <li>
                <a
                  href="/explore/subcategories/training-subset/"
                  class="wbg_sidebar second-level"
                  >Training subset</a
                >
              </li>
              <li>
                <a href="/explore/topic-composition/">Topic composition</a>
              </li>
              <li>
                <a
                  href="/explore/subcategories/topic-browser/"
                  class="wbg_sidebar second-level"
                  >Topic browser</a
                >
              </li>
              <li>
                <a
                  href="/explore/subcategories/filtering-by-topic-share/"
                  class="wbg_sidebar second-level"
                  >Filtering by topic share</a
                >
              </li>
              <li>
                <a href="/explore/topic-profiles/">Topic profiles</a>
              </li>
              <li>
                <a href="/explore/topic-taxonomy/">Topic taxonomy</a>
              </li>
              <li>
                <a href="/explore/topic-relationships/">Topic relationships</a>
              </li>
              <li>
                <a href="/explore/word-embeddings/">Word embeddings</a>
              </li>
              <li>
                <a href="/explore/similarity/">Similarity</a>
              </li>
              <li>
                <a href="/explore/knowledge-page-service/"
                  >Knowledge page service</a
                >
              </li>
              <li>
                <a
                  href="/explore/subcategories/example/"
                  class="wbg_sidebar second-level"
                  >Example</a
                >
              </li>
              <li>
                <a
                  href="/explore/subcategories/instructions/"
                  class="wbg_sidebar second-level"
                  >Instructions</a
                >
              </li>
            </ol>
          </section>
        </aside>
        <div class="col-sm-10 blog-main">
          <article class="blog-post">
            <!-- <header>
              <h1 class="blog-post-title mb-3" dir="auto">
                <a href="/explore/explore/"
                  >Explore</a
                >
              </h1>
            </header>
            <p>Explore</p> -->
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
export default {
  name: "Explore",
  components: {},
};
</script>

<style scoped>
@import "../../node_modules/bootstrap-vue/dist/bootstrap-vue.css";

.content-row {
  min-height: 50vh;
}
@media (min-width: 1200px) {
  .flowing {
    max-width: 1600px;
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