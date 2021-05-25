<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <p class="mt-4 text-justify">
        Multilateral development banks (MDBs) make much of their respective
        research output and project documents publicly available. An analysis
        and the regular monitoring of the scope and coverage of these documents
        can reveal the extent to which issues related to forced displacement
        have been and will be covered in analytical and operational work, over
        time and by country. Considering the large volume of information
        available, such an analysis/assessment can only be conducted by applying
        advanced machine learning (natural language processing) techniques.
      </p>
      <p class="mt-1 text-justify">
        To train our natural language processing (NLP) models and to build our
        document catalog, we scraped a large collection of publicly-available
        documents from the websites of the UNHCR and of five MDBs. See the
        <router-link to="/explore/subcategories/sources">sources</router-link>,
        <router-link to="/explore/subcategories/volume">volume</router-link>,
        and
        <router-link to="/explore/subcategories/geographic-coverage"
          >geographic coverage</router-link
        >
        pages for more information on the composition of our corpus.
      </p>
      <p class="mt-1 text-justify">
        For users interested in conducting their own analysis, we also provide a
        dataset containing a list of all documents included in the corpus, with
        the available metadata and modeled topic composition. Users interested
        in replicating or adapting our NLP models are invited to visit our
        <a href="https://github.com/worldbank" target="_blank"
          >GitHub repository</a
        >
        and to read more about the
        <router-link to="#">methods and tools</router-link> we applied (external
        website).
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Corpus",
  props: {
    page_title: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
