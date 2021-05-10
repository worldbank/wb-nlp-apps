<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <p>
        Generation of knowledge on development and economic issues come from
        <router-link to="/explore/subcategories/sources/"
          >various sources</router-link
        >. The collection of documents (and metadata when available) covered by
        our corpus come from multilateral development banks such as the ADB,
        AfDB, IDB, and The World Bank; various UN organizations, and other
        international organizations working on development and economic issues.
      </p>
      <p>
        After shortlisting the organizations of interest, we assessed each
        source for the availability of a public repository of documents. We only
        take the organizations that have publicly accessible sources that can be
        automatically scraped using web scraping or through API access. Note
        that care in reducing the impact of our scraping activity was ensured by
        making sure that the scrapers follow the site’s
        <code>robots.txt</code> and by limiting the rate of requests made to
        each site.
      </p>
      <p>
        Sample pages from each document repository were analyzed for the
        availability of metadata and downloadable PDF or text files. A scraper
        for each organization was then developed using
        <a href="https://scrapy.org/" target="_blank">Scrapy</a> to automate the
        acquisition of metadata from the source page as well as to download the
        PDF or text files. For APIs we implemented customized end-point access
        functions using the
        <a href="https://docs.python-requests.org/en/master/" target="_blank"
          >requests library</a
        >
        in Python.
      </p>
      <p>
        The scraped metadata and pdf/text files were then stored as our raw
        corpus. The metadata scraped using Scrapy are in the form of JSON lines
        while the
        <a href="https://search.worldbank.org/api/v2/wds" target="_blank"
          >World Bank’s Documents and Reports API</a
        >
        produces json data with well-defined schema. We stored the metadata in
        MongoDB and Elasticsearch. The PDFs are stored as well for processing
        and the extracted texts from these were used as input to our NLP models.
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
