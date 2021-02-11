<template>
  <b-nav vertical pills align="left" class="w-100">
    <SidePanelOption
      v-for="nav_item in nav_items"
      :key="nav_item.page"
      :nav_item="nav_item"
    />
  </b-nav>
</template>

<script>
import SidePanelOption from "./SidePanelOption.vue";
export default {
  name: "SidePanel",
  components: {
    SidePanelOption,
  },
  props: {},
  data: function () {
    return {
      nav_items: [
        { page: "INTRODUCTION", subpages: [] },
        {
          page: "CORPUS",
          subpages: [
            "Sources and volume",
            "Geographic coverage",
            "Metadata and API",
            "Test corpus",
          ],
        },
        { page: "TOPIC COMPOSITION", subpages: [] },
        { page: "TOPIC PROFILES", subpages: [] },
        { page: "TOPIC TAXONOMY", subpages: [] },
        { page: "TOPIC RELATIONSHIPS", subpages: [] },
        // { page: "EMBEDDING VIZ", subpages: [] },
        { page: "WORD EMBEDDINGS", subpages: [] },
        { page: "SIMILARITY", subpages: [] },
        { page: "MONITORING SYSTEM", subpages: [] },
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
