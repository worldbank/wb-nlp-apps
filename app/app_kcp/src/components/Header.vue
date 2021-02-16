<template>
  <div id="appHeader">
    <noscript>
      <strong
        >We're sorry but <%= htmlWebpackPlugin.options.title %> doesn't work
        properly without JavaScript enabled. Please enable it to
        continue.</strong
      >
    </noscript>
    <div class="container">
      <div class="row mb-3">
        <div class="col-12 col-md-4 col-lg-3 mt-3">
          <img src="/static/files/logo.svg" height="40px" alt="WBG logo" />
        </div>
        <div class="col-12 col-md-8 col-lg-3 mt-3 wbg-header-title__block">
          <div class="wbg-title">Document Explorer</div>
          <div class="wbg-subtitle">
            Natural Language Processing for knowledge discovery
          </div>
        </div>
      </div>
    </div>
    <div class="blog-masthead wbg-masthead">
      <div class="container">
        <nav class="nav blog-nav navbar wbg-navbar navbar-expand-lg">
          <button
            class="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <i class="fas fa-bars" aria-hidden="true"></i
            ><span class="ml-1">Menu</span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              <!-- <li
                @click="activate('home')"
                :class="{
                  active:
                    ($route.name == 'home')
                    | ($route.name == ''),
                }"
                class="nav-link nav-item"
              > -->
              <li
                class="nav-link nav-item"
                :class="{
                  active: $route.name.startsWith('home'),
                }"
              >
                <router-link class="nav-link" to="/">Home</router-link>
              </li>
              <li
                :class="{ active: $route.name.startsWith('search') }"
                class="nav-link nav-item"
              >
                <router-link class="nav-link" to="/search">Search</router-link>
              </li>
              <li
                :class="{ active: $route.name.startsWith('explore') }"
                class="nav-link nav-item"
              >
                <router-link class="nav-link" to="/explore"
                  >Explore</router-link
                >
              </li>
              <!-- <li
                :class="{ active: $route.name.startsWith('analyze') }"
                class="nav-link nav-item"
              >
                <router-link class="nav-link" to="/analyze"
                  >Analyze</router-link
                >
              </li> -->
              <li
                :class="{ active: $route.name.startsWith('methods') }"
                class="nav-link nav-item"
              >
                <router-link class="nav-link" to="/methods"
                  >Methods &amp; Tools</router-link
                >
              </li>
              <li
                :class="{ active: $route.name.startsWith('api') }"
                class="nav-link nav-item"
              >
                <router-link class="nav-link" to="/content-api"
                  >API</router-link
                >
              </li>
              <li
                :class="{ active: $route.name.startsWith('about') }"
                class="nav-link nav-item"
              >
                <router-link class="nav-link" to="/about">About</router-link>
              </li>
              <li
                :class="{ active: $route.name.startsWith('styleguide') }"
                class="nav-link nav-item"
              >
                <router-link class="nav-link" to="/styleguide/"
                  >Styleguide</router-link
                >
              </li>
            </ul>
          </div>
        </nav>
      </div>
    </div>
  </div>
</template>


<script>
// import SidePanel from "./components/SidePanel.vue";

export default {
  name: "Header",
  props: {
    nav_name: String,
  },
  data: function () {
    // return { active_el: localStorage.active_el };
    return { active_el: "home" };
  },
  methods: {
    activate: function (el) {
      // localStorage.active_el = el;
      this.active_el = el;
    },
  },
  // components: {
  //   SidePanel,
  // },
};
</script>
