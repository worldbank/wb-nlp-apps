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
            <router-link to="#">{{ currentPageTitle }}</router-link>
          </div>
        </div>
        <div class="col-12">
          <i class="fas fa-search fa-2x" aria-hidden="true"></i>
          <h1>{{ currentPageTitle }}</h1>
          <p v-show="currentPageTitle === 'Explore'">
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
      <b-button
        v-if="toggleButtonShow"
        class="sidebar-toggler"
        @click="toggleButton"
        :variant="aria_expanded ? 'light' : 'dark'"
      >
        {{ aria_expanded ? "Collapse" : "Expand" }}</b-button
      >
      <div class="row">
        <aside id="blog-sidebar" class="col-sm-3" v-show="!aria_expanded">
          <section class="sidebar-module">
            <ol class="list-unstyled">
              <li>
                <router-link
                  to="/explore/corpus/"
                  :class="{ active: $route.name === 'explore_corpus' }"
                  >Corpus</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/sources/"
                  class="wbg_sidebar second-level"
                  :class="{
                    active: $route.name === 'explore_sources',
                  }"
                  >Sources</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/volume/"
                  class="wbg_sidebar second-level"
                  :class="{
                    active: $route.name === 'explore_volume',
                  }"
                  >Volume</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/geographic-coverage/"
                  class="wbg_sidebar second-level"
                  :class="{
                    active: $route.name === 'explore_geographic-coverage',
                  }"
                  >Geographic coverage</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/metadata/"
                  class="wbg_sidebar second-level"
                  :class="{ active: $route.name === 'explore_metadata' }"
                  >Metadata</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/topic-composition/"
                  :class="{
                    active: $route.name === 'explore_topic-composition',
                  }"
                  >Topic composition</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/topic-browser/"
                  class="wbg_sidebar second-level"
                  :class="{ active: $route.name === 'explore_topic-browser' }"
                  >Topic browser</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/filtering-by-topic-share/"
                  class="wbg_sidebar second-level"
                  :class="{
                    active: $route.name === 'explore_filtering-by-topic-share',
                  }"
                  >Filtering by topic share</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/topic-profiles/"
                  :class="{ active: $route.name === 'explore_topic-profiles' }"
                  >Topic profiles</router-link
                >
              </li>
              <!-- <li>
                <router-link
                  to="/explore/topic-taxonomy/"
                  :class="{ active: $route.name === 'explore_topic-taxonomy' }"
                  >Topic taxonomy</router-link
                >
              </li> -->
              <!-- <li>
                <router-link
                  to="/explore/topic-relationships/"
                  :class="{
                    active: $route.name === 'explore_topic-relationships',
                  }"
                  >Topic relationships</router-link
                >
              </li> -->
              <li>
                <router-link
                  to="/explore/word-embeddings/"
                  :class="{ active: $route.name === 'explore_word-embeddings' }"
                  >Word embeddings</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/similarity/"
                  :class="{ active: $route.name === 'explore_similarity' }"
                  >Analyze document</router-link
                >
              </li>
              <!-- <li>
                <router-link
                  to="/explore/knowledge-page-service/"
                  :class="{
                    active: $route.name === 'explore_knowledge-page-service',
                  }"
                  >Knowledge page service</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/example/"
                  class="wbg_sidebar second-level"
                  :class="{ active: $route.name === 'explore_example' }"
                  >Example</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/instructions/"
                  class="wbg_sidebar second-level"
                  :class="{ active: $route.name === 'explore_instructions' }"
                  >Instructions</router-link
                >
              </li> -->
            </ol>
          </section>
        </aside>
        <div
          class="blog-main"
          :class="aria_expanded ? 'col-sm-12' : 'col-sm-9'"
        >
          <article class="blog-post">
            <div class="content-row">
              <!-- {{ toggleButtonShow }} -->
              <!-- {{ aria_expanded }} -->
              <router-view></router-view>
            </div>
            <hr />
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
  computed: {
    currentPageTitle() {
      var name = this.$route.name;

      if (name.includes("_")) {
        name = name.split("_")[1];
      }
      name = name.replace(/-/g, " ");

      return name[0].toUpperCase() + name.slice(1);
    },
    toggleButtonShow() {
      const valid_routes = [
        "explore_topic-browser",
        "explore_filtering-by-topic-share",
        "explore_topic-profiles",
        "explore_word-embeddings",
        "explore_similarity",
      ];
      return valid_routes.includes(this.$route.name);
    },
  },
  data() {
    return {
      aria_expanded: false,
    };
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
    toggleButton() {
      this.aria_expanded = !this.aria_expanded;
    },
  },
};
</script>

<style scoped>
@import "../../node_modules/bootstrap-vue/dist/bootstrap-vue.css";

.content-row {
  min-height: 50vh;
}
/* @media (min-width: 1200px) {
  .flowing {
    max-width: 1200px;
  }
} */

.blog-header {
  margin-bottom: 2rem;
}

.sidebar-toggler {
  margin-top: -20px;
  margin-left: 75vw;
  position: absolute;
}

.flowing {
  width: 80%;
  max-width: 80rem;
  margin: auto;
}
</style>