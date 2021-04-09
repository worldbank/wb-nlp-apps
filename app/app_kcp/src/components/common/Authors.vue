<template>
  <div v-if="authors && authors.length > 0" class="authors">
    Author(s):
    <span v-for="author in authors" :key="author">
      <router-link
        class="author-name"
        :to="{
          name: 'search',
          query: {
            search_text: author,
            search_type: 'keyword',
            page: 1,
          },
        }"
        >{{ author }}</router-link
      >,
      <a
        :href="'https://orcid.org/orcid-search/search?searchQuery=' + author"
        target="_blank"
        ><img class="a-icon" src="/static/files/orcid_128x128.png"
      /></a>
      <a
        :href="'https://scholar.google.com/scholar?q=' + author"
        target="_blank"
        ><img class="a-icon" src="/static/files/google-scholar.png"
      /></a>
      <a
        :href="
          'https://www.semanticscholar.org/search?sort=relevance&q=' + author
        "
        target="_blank"
        ><img
          class="a-icon a-icon-last"
          src="/static/files/ss-mstile-150x150.png"
      /></a>
    </span>
  </div>
</template>
<script>
export default {
  name: "Authors",
  props: {
    authors: {
      type: Array,
      default: function () {
        return [
          "Jose Rizal",
          "Richard Feynman",
          "Olivier Dupriez",
          "Aivin Solatorio",
        ];
      },
    },
  },
};
</script>
<style>
.authors {
  font-size: smaller;
}
.a-icon {
  width: 20px;
  height: 20px;
  padding: 2px;
}
.a-icon-last {
  margin-right: 10px;
}
</style>