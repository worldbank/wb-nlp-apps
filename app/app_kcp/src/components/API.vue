<template>
  <div>
    <!-- <div class="container flowing">
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
        <div class="col-sm-9 blog-main">
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
    </div> -->
    <iframe src="/redoc" frameborder="0" height="800px" width="100%"></iframe>
  </div>
</template>


<script>
export default {
  name: "API",
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