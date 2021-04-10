<template>
  <div
    v-if="authors && valid_authors.length > 0"
    :class="authors_class"
    class="authors"
  >
    Author(s):
    <span v-for="author in valid_authors" :key="author">
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
        return [];
        // [
        //   "Jose Rizal",
        //   "Richard Feynman",
        //   "",
        //   "Olivier Dupriez",
        //   "Aivin Solatorio",
        // ];
      },
    },
    authors_class: {
      type: String,
      default: "authors-small",
    },
  },
  computed: {
    valid_authors: function () {
      // return this.$props.authors;
      return this.authors.filter((word) => word.trim().length > 0);
    },
  },
};
</script>
<style>
.authors {
  margin-bottom: 5px;
}
.authors-small {
  font-size: 0.8rem;
}
.authors-medium {
  font-size: 0.9rem;
}
.authors-large {
  font-size: 1rem;
}

.authors-small .a-icon {
  width: 1.2rem;
  height: 1.2rem;
  padding: 2px;
}
.authors-medium .a-icon {
  width: 1.3rem;
  height: 1.3rem;
  padding: 2px;
}
.authors-large .a-icon {
  width: 1.4rem;
  height: 1.4rem;
  padding: 2px;
}
.a-icon-last {
  margin-right: 10px;
}
</style>