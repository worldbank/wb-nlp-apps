<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <p>
        The collection of documents covered by our corpus come from different
        multilateral development banks, UN organizations, and other
        international organizations working on development and economic issues.
      </p>

      <p>
        After shortlisting the organizations of interest, we assessed each
        source for the availability of a public repository of documents. We take
        only the organizations that have publicly accessible sources that can be
        automatically scraped using web scraping or through API access.
      </p>
      <p>
        Sample pages from each document repository were analyzed for the
        availability of metadata and downloadable pdf or text files. A scraper
        for each organization was then developed using
        <a href="https://scrapy.org/" target="_blank">Scrapy</a> to automate the
        acquisition of metadata from the source page as well as to download the
        pdf or text files.
      </p>
      <p>
        The scraped metadata and pdf/text files were then stored as our raw
        corpus.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "TextAcquisition",
  props: {
    page_title: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* h3 {
  margin: 40px 0 0;
} */
/* a {
  color: #42b983;
} */
</style>
