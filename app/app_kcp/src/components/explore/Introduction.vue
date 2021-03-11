<template>
  <div>
    <!-- <h1>{{ page_title }}</h1> -->
    <div>
      <p>
        The <span style="font-weight: bold">Explore</span> pages showcase a
        variety of details and demos regarding the data and models used in the
        project. We also provide an overview of the data sources, links to
        sample datasets, and materials that individuals who want to replicate
        the methods used in the project or who want to experiment could use.
      </p>
      <p>
        The <router-link to="/explore/corpus">Corpus</router-link> section
        provides detailed description of the sources and coverage of our corpus.
        Additional insights regarding the corpus can be explored under the
        <router-link to="/explore/subcategories/geographic-coverage"
          >geographic coverage</router-link
        >
        page where we present the evolution of the volume of documents over time
        with respect to countries. Under the
        <router-link to="/explore/subcategories/metadata">metadata</router-link>
        subsection, we provide a brief outline about the metadata contained in
        our dataset. Lastly, the
        <router-link to="/explore/subcategories/training-subset"
          >training subset</router-link
        >
        page contains links to a subset of our corpus, metadata, and repository
        containing the code to replicate our results.
      </p>

      <p>
        In this project, we focus in two categories of models commonly used in
        natural language processing (NLP) to analyse and extract value from
        unstructured text data. The first is topic modeling and the second is
        word embedding model. The
        <router-link to="/explore/topic-composition"
          >topic composition</router-link
        >
        section highlights some practical use-cases where the output of a topic
        model can be used. The
        <router-link to="/explore/subcategories/topic-browser"
          >topic browser</router-link
        >
        page provides an interactive visualization of the topics learned by the
        topic model. The
        <router-link to="/explore/subcategories/filtering-by-topic-share"
          >filtering by topic share</router-link
        >
        page explores a novel way of discovering documents simply by setting a
        desired level of topic intensity. Another application of a topic model
        is that it allows us to analyze the evolution of topic popularity across
        varying document types over time. This feature can be explored in the
        <router-link to="/explore/topic-profiles">topic profiles</router-link>
        page.
      </p>

      All code (except scrapers) in GitHub. See Methods and Tools.
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
