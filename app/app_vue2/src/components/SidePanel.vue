<template>
  <b-nav vertical pills align="left" class="w-100">
    <!-- <b-nav-item
      v-for="nav_name in nav_names"
      :key="nav_name"
      :to="nav_name.toLowerCase().replaceAll(' ', '-')"
      :active="$route.name == nav_name.toLowerCase()"
      >{{ nav_name }}
      <b-nav-link>{{ nav_name }}</b-nav-link>
    </b-nav-item> -->
    {{ $route.name }}

    <b-nav-item
      v-for="nav_item in nav_items"
      :key="nav_item.page"
      :to="'/explore/' + nav_item.page.toLowerCase().replaceAll(' ', '-')"
      :active="$route.name == nav_item.page.toLowerCase()"
      v-b-toggle.collapse-corpus
    >
      {{ nav_item.page }}
      <div v-if="$route.name == 'corpus' && nav_item.page == 'CORPUS'">
        <b-collapse id="collapse-corpus" class="mt-2">
          <b-nav-item style="float: right">
            <b-link
              v-for="subpage in nav_item.subpages"
              :key="nav_item.page + '-' + subpage"
              style="float: right"
              >{{ subpage }}</b-link
            >
          </b-nav-item>
          <!--
          <b-card>
            <p class="card-text">Collapse contents Here</p>
            <b-button v-b-toggle.collapse-1-inner size="sm"
              >Toggle Inner Collapse</b-button
            >
            <b-collapse id="collapse-1-inner" class="mt-2">
              <b-card>Hello!</b-card>
            </b-collapse>
          </b-card> -->
        </b-collapse>
      </div>
      <!-- <b-link></b-link> -->
    </b-nav-item>

    <!--

    <b-nav-item
      v-for="nav_name in nav_names"
      :key="nav_name"
      :to="nav_name.toLowerCase().replaceAll(' ', '-')"
      :active="$route.name == nav_name.toLowerCase()"
      v-b-toggle.collapse-corpus
      >{{ nav_name }}
      <b-collapse v-if="nav_name == 'Corpus'" id="collapse-corpus" class="mt-2">
        <b-card>
          <p class="card-text">Collapse contents Here</p>
          <b-button v-b-toggle.collapse-1-inner size="sm"
            >Toggle Inner Collapse</b-button
          >
          <b-collapse id="collapse-1-inner" class="mt-2">
            <b-card>Hello!</b-card>
          </b-collapse>
        </b-card>
      </b-collapse>
    </b-nav-item> -->
  </b-nav>
</template>

<script>
export default {
  name: "SidePanel",
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
