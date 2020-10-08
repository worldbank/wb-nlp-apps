<template>
  <b-nav vertical pills align="left" class="w-100">
    <b-nav-item v-for="nav_name in nav_names" :key="nav_name">
      <b-link :to="nav_name.toLowerCase()" :active="$route.name == nav_name">{{
        nav_name
      }}</b-link>
    </b-nav-item>
  </b-nav>
</template>

<script>
export default {
  name: "SidePanel",
  props: {},
  data: function () {
    return {
      nav_names: [
        "INTRODUCTION",
        "CORPUS",
        "TOPIC COMPOSITION",
        "TOPIC PROFILES",
        "TOPIC TAXONOMY",
        "TOPIC RELATIONSHIPS",
        "WORD EMBEDDINGS",
        "SIMILARITY",
        "MONITORING SYSTEM",
      ],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
/* ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
} */
/* a {
  color: #42b983;
} */
</style>
