<template>
  <div class="banner">
    <header class="blog-header wbg-header banner-header">
      <div class="container banner-container">
        <div class="row justify-content-center">
          <div class="col-12 col-md-8">
            <h1 class="blog-title text-center banner-blog-title" dir="auto">
              JDC Document Explorer
            </h1>
          </div>
        </div>
      </div>
    </header>
    <div class="banner-nav-container">
      <div class="container banner-container-navbar">
        <div>
          <b-navbar
            type="dark"
            variant="dark"
            sticky="true"
            class="banner-navbar"
          >
            <b-navbar-nav>
              <b-nav-item
                @click="routeTo('home')"
                :class="{
                  active: $route.name === 'home',
                }"
                >About</b-nav-item
              >
              <b-nav-item
                @click="routeTo('search')"
                :class="{
                  active: $route.name === 'search',
                }"
                >Search</b-nav-item
              >
              <b-nav-item
                @click="routeTo('explore')"
                :class="{
                  active: $route.name.startsWith('explore'),
                }"
                >Explore</b-nav-item
              >
            </b-navbar-nav>
          </b-navbar>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    routeTo(route_name) {
      this.$router.replace({
        name: route_name,
      });
    },
  },
};
</script>


<style scoped>
.banner-header {
  padding: 0px;
  margin: 0px;
  border: 0px;
  height: 120px;
}

.banner-container {
  padding-top: 10px !important;
}

.banner-blog-title {
  font-size: 3rem;
}

.banner-nav-container {
  background-color: #0072bc;
}
.banner-container-navbar {
  padding: 0px !important;
}

.banner-navbar {
  padding: 0px;
  padding-left: 20px;
  background-color: #0072bc !important;
}
</style>