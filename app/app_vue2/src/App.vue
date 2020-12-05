<template>
  <div id="app">
    <br />
    <b-container fluid>
      <b-row>
        <b-col class="ml-auto" cols="11">
          <div>
            <b-nav align="right">
              <b-nav-item active>HOME</b-nav-item>
              <b-nav-item>SEARCH</b-nav-item>
              <b-nav-item>EXPLORE</b-nav-item>
              <b-nav-item>ANALYZE</b-nav-item>
              <b-nav-item>METHODS & TOOLS</b-nav-item>
              <b-nav-item>API</b-nav-item>
              <b-nav-item>ABOUT</b-nav-item>
            </b-nav>
          </div>
        </b-col>
        <b-col cols="1"></b-col>
      </b-row>

      <b-row>
        <b-col md="2">
          <br />
          <br />
          <br />
          <br />
          <br />
          <b-row>
            <b-col cols="2" md="1"></b-col>
            <b-col cols="8" md="10"> <SidePanel /> </b-col>
            <b-col cols="2" md="1"></b-col> </b-row
        ></b-col>
        <b-col md="10" class="mr-auto">
          <b-row>
            <!-- <b-col sm="10" offset-sm="1" offset-md="0" md="11"> -->
            <b-col md="11">
              <br />
              <br />
              <div>
                <router-view class="view"></router-view>
              </div>
            </b-col>
            <b-col md="1"></b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import SidePanel from "./components/SidePanel.vue";

export default {
  name: "App",
  components: {
    SidePanel,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>
