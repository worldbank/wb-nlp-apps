<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      <p>
        Information on each document is collected at the stage of web scraping.
        This includes the source, title, author, abstract if available, URL.
        Some website provide more information than others. The WB for example
        provides topic tagging, region, document type, link to projects, and
        much more. This information is not available, and cannot be deducted,
        for other sources. Therefore, not all metadata are available for all
        documents. We augment these metadata by running data extraction scripts
        (such as country counts,…) or NLP models. All metadata are stored in a
        MongoDB database (content available in CSVs here or via API here). This
        meta-database is maintained on a daily basis, using a Nifi-based
        automation process.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Metadata",
  props: {
    page_title: String,
  },
  data: function () {
    return {
      date_now: new Date().toDateString(),
      corpus_size: 200000,
      org_count: 14,
      total_tokens: 1029000000,
    };
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
