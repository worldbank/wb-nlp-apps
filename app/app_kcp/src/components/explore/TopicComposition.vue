<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      <p>
        We derive the topic composition of or corpus (and sub-corpuses) by
        running Latent Dirichlet Allocation (LDA) models. LDA (Blei, 2003) is an
        unsupervised machine learning approach, which does not require any
        pre-defined topic taxonomy. The main parameter to be provided to the
        model is the number of topics we assume are contained in the corpus. The
        LDA model will derive these topics and return them in the form of a list
        of keywords (each keyword with a “weight” indicating its importance). We
        ran models with this parameter set at 25, 50, and 100. More detailed
        information on the approach and its implementation can be found
        <router-link to="/methods/lda">here</router-link>; the models were
        applied using open source software and libraries; our scripts are
        accessible <a href="https://github.com/avsolatorio/wb_nlp">here</a>.
      </p>
      <p>
        We trained our LDA models on the full corpus. The output includes a
        description of the topic composition at the document level, which allows
        us to report on topic composition by year and sub-corpus. This topic
        composition is stored in our publicly available metadata files. It is
        used in our search tool, and as an input to classification models. It is
        also used in our exploration tool allowing users to filter documents
        based on their topic coverage. In our catalog, the topic composition
        based on the 40-topic model is shown for each document. The topic
        profiles allows you to review the patterns in a topic coverage over time
        and by region or sub-corpus.
      </p>
      <p>
        Running the LDA model on a large collection of documents is a
        compute-intensive task. We plan to re-train the model occasionally
        (every six months, or if/when large additions to our corpus justify it).
        The topic composition of documents acquired after the LDA models were
        trained is obtained by inference.
      </p>
      <!-- <p>Mallet implementation</p>
      <p>Labeling of topics</p>
      <p>Priors</p>
      <p>Tools (and acknowledgments):</p>
      <p>See Methods and Tools section for details, and Github repo.</p> -->

      <!-- <p>Automatic labeling ?</p>
      <p>Explain why some topics are clearly meaningful, some less.</p>
      <p>Visualization and reporting results: see topic browser, and …</p> -->
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
