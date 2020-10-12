<template>
  <div>
    <b-nav-item
      :to="'/explore/' + slugifyText(nav_item.page)"
      :active="$route.name.startsWith(slugifyText(nav_item.page))"
      v-b-toggle="'collapse-' + slugifyText(nav_item.page)"
    >
      {{ nav_item.page }}</b-nav-item
    >

    <b-collapse
      v-if="
        nav_item.subpages.length > 0 &&
        $route.name.startsWith(slugifyText(nav_item.page))
      "
      :id="'collapse-' + slugifyText(nav_item.page)"
      class="mt-2"
    >
      <b-nav vertical align="right" class="w-10">
        <b-link
          style="margin-left: 40px"
          v-for="subpage in nav_item.subpages"
          :key="nav_item.page + '-' + subpage"
          active-class="active-link"
          :to="
            '/explore/' +
            slugifyText(nav_item.page) +
            '/' +
            slugifyText(subpage)
          "
          >{{ subpage }}</b-link
        >
      </b-nav>
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
.active-link {
  color: red;
}
</style>
