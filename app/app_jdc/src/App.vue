<template>
  <div id="appID">
    <Header />
    <router-view />

    <!-- <router-view class="view"></router-view> -->
  </div>
</template>

<script>
// import SidePanel from "./components/SidePanel.vue";
import Header from "./components/Header.vue";

export default {
  name: "App",
  // data: function () {
  //   return { active_el: "home" };
  // },
  // methods: {
  //   activate: function (el) {
  //     this.active_el = el;
  //   },
  // },
  components: {
    // SidePanel,
    Header,
  },
};
</script>

<style>
#appID {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  /* -webkit-font-smoothing: antialiased; */
  /* -moz-osx-font-smoothing: grayscale; */
  /* text-align: center; */
  /* color: #2c3e50; */
  color: #212529;
  /* margin-top: 60px; */
}
</style>
