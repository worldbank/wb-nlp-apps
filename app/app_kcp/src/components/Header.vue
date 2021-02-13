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
              <li
                @click="activate('home')"
                :class="{ active: active_el == 'home' }"
                class="nav-link nav-item"
              >
                <a class="nav-link" href="/">Home</a>
              </li>
              <li
                @click="activate('search')"
                :class="{ active: active_el == 'search' }"
                class="nav-link nav-item"
              >
                <a class="nav-link" href="/search" title="Search">Search</a>
              </li>
              <li
                @click="activate('explore')"
                :class="{ active: active_el == 'explore' }"
                class="nav-link nav-item"
              >
                <a class="nav-link" href="/explore" title="Explore">Explore</a>
              </li>
              <li
                @click="activate('analyze')"
                :class="{ active: active_el == 'analyze' }"
                class="nav-link nav-item"
              >
                <a class="nav-link" href="/analyze" title="Analyze">Analyze</a>
              </li>
              <li
                @click="activate('methods')"
                :class="{ active: active_el == 'methods' }"
                class="nav-link nav-item"
              >
                <a class="nav-link" href="/methods" title="Methods &amp; Tools"
                  >Methods &amp; Tools</a
                >
              </li>
              <li
                @click="activate('api')"
                :class="{ active: active_el == 'api' }"
                class="nav-link nav-item"
              >
                <a class="nav-link" href="/api" title="API">API</a>
              </li>
              <li
                @click="activate('about')"
                :class="{ active: active_el == 'about' }"
                class="nav-link nav-item"
              >
                <a class="nav-link" href="/about" title="About">About</a>
              </li>
              <li
                @click="activate('styleguide')"
                :class="{ active: active_el == 'styleguide' }"
                class="nav-link nav-item"
              >
                <a class="nav-link" href="/styleguide/" title="Styleguide"
                  >Styleguide</a
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
  data: function () {
    return { active_el: "home" };
  },
  methods: {
    activate: function (el) {
      this.active_el = el;
    },
  },
  // components: {
  //   SidePanel,
  // },
};
</script>
