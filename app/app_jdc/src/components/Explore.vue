<template>
  <div class="container-wrapper">
    <Banner />
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
                  to="/explore/topic-composition/"
                  :class="{
                    active: $route.name === 'explore_topic-composition',
                  }"
                  >Topic composition</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/topic-profiles/"
                  class="wbg_sidebar second-level"
                  :class="{ active: $route.name === 'explore_topic-profiles' }"
                  >Topic profiles</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/subcategories/filtering-by-topic-share/"
                  class="wbg_sidebar second-level"
                  :class="{
                    active: $route.name === 'explore_filtering-by-topic-share',
                  }"
                  >Filtering by topic composition</router-link
                >
              </li>
              <li>
                <router-link
                  to="/explore/word-embeddings/"
                  :class="{ active: $route.name === 'explore_word-embeddings' }"
                  >Word embeddings</router-link
                >
              </li>
            </ol>
          </section>
        </aside>
        <div
          class="blog-main"
          :class="aria_expanded ? 'col-sm-12' : 'col-sm-9'"
        >
          <article class="blog-post">
            <div class="content-row">
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

import Banner from "./Banner";

export default {
  name: "Explore",
  components: { Banner },
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

.nav-link {
  margin-top: 0px !important;
  margin: 10px;
  background-color: transparent !important;
  border: 0px !important;
  padding: 0px;
}

/* .container-wrapper {
  margin-top: 2rem;
} */

.fa-no-margin {
  margin: 0px;
}
</style>