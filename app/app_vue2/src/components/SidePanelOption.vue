<template>
  <div>
    <b-nav-item
      :to="'/explore/' + slugifyText(nav_item.page)"
      :active="$route.name == nav_item.page.toLowerCase()"
      v-b-toggle="'collapse-' + slugifyText(nav_item.page)"
    >
      {{ nav_item.page }}</b-nav-item
    >

    <b-collapse
      v-if="nav_item.subpages.length > 0"
      :id="'collapse-' + slugifyText(nav_item.page)"
      class="mt-2"
    >
      <b-nav-item style="float: right">
        <b-link
          v-for="subpage in nav_item.subpages"
          :key="nav_item.page + '-' + subpage"
          style="float: right"
          >{{ subpage }}</b-link
        >
      </b-nav-item>
    </b-collapse>
  </div>
</template>

<script>
export default {
  name: "SidePanelOption",
  props: {
    nav_item: Object,
  },
  methods: {
    slugifyText: function (text) {
      return text.toLowerCase().replaceAll(" ", "-");
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
</style>
