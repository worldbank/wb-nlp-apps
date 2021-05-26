<template>
  <div>
    <header>
      <h1 class="blog-post-title mb-3" dir="auto">
        {{ page_title }}
      </h1>
    </header>
    <div>
      <p class="mt-3 text-justify">
        We derive the topic composition of or corpus (and sub-corpuses) by
        running a Latent Dirichlet Allocation (LDA) model. LDA is an
        unsupervised machine learning approach that does not require any
        pre-defined topic taxonomy. The main parameter to be provided to the
        model is the number of topics we assume are contained in the corpus. The
        LDA model will derive these topics and return them in the form of a list
        of keywords. The model trained for the JDC Document Explorer is an
        80-topic model. More detailed information on the LDA approach and its
        implementation can be found in an external website
        <a href="#" target="_blank">here</a>; the models were applied using
        open-source software and libraries; our text processing and modeling
        scripts are accessible
        <a href="https://www.github.com/avsolatorio/wb_nlp" target="_blank"
          >here</a
        >.
      </p>
      <p class="mt-1 text-justify">
        The topic composition of each document can be found in the description
        of the documents in our <a href="#" target="_blank">catalog</a> and in
        our <a href="#" target="_blank">dataset</a>. In the
        <router-link to="/explore/subcategories/topic-profiles/"
          >topic profiles</router-link
        >
        page, we summarize the composition of the corpus as a whole, with
        breakdowns by source, document type, region, and year.
      </p>
      <p class="mt-1 text-justify">
        Running the LDA model on a large collection of documents is a
        compute-intensive task. We may re-train the model occasionally (every
        six months, or if/when large additions to our corpus justify it). The
        topic composition of documents acquired after the LDA model was trained
        is obtained by inference.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "TopicComposition",
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
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
/* a {
  color: #42b983;
} */
</style>
