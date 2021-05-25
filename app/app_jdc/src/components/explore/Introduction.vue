<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <p class="mt-4 text-justify">
        We describe in this section the content of the corpus of documents we
        used to train our NLP models and to build our document catalog. This
        description covers the
        <router-link to="/explore/subcategories/sources">sources</router-link>
        of documents, the
        <router-link to="/explore/subcategories/volume">volume</router-link> of
        information available, and its time and
        <router-link to="/explore/subcategories/geographic-coverage"
          >geographic coverage</router-link
        >. The corpus composition is also available as a CSV dataset, for users
        interested in conducting their own analysis.
      </p>
      <p class="mt-1 text-justify">
        We provide visualizations of the results of our topic extraction model
        (a Latent Dirichlet Allocation or LDA model) in the form of
        <router-link to="/explore/topic-profiles">topic profiles</router-link>,
        and a tool that allows users to
        <router-link to="/explore/subcategories/filtering-by-topic-share"
          >filter documents by their topic composition</router-link
        >.
      </p>
      <p class="mt-1 text-justify">
        Last, we present some results of our
        <router-link to="/explore/word-embeddings">word embedding</router-link>
        model (word2vec), which extracts semantic similarities between terms and
        allows us to implement the semantic search in our catalog.
      </p>
      <p class="mt-1 text-justify">
        The tools and methods used to implement these approaches and the models
        themselves are described in more detail in the generic
        <router-link to="/">Document Explorer</router-link> website. We relied
        exclusively on open sources software, and our scripts and models are all
        made
        <a href="https://github.com/worldbank" target="_blank"
          >publicly available</a
        >
        on GitHub.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Introduction",
  props: {
    page_title: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
/* a {
  color: #42b983;
} */
</style>
