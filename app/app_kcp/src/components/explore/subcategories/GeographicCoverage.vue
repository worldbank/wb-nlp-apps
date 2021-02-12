<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      <p>
        Our focus on development issues and on publications and documents
        originating from development agencies implies that the majority of
        documents in our corpus relate to low and middle-income countries. But
        not all documents are country-specific and some cover, in part or in
        full, high-income countries. To assess the geographic coverage of the
        corpus and of its components, we cannot exclusively rely on metadata
        that may be provided by the source websites (the World Bank for example
        provides information on “Region” and “Country” for most of its
        documents).
      </p>
      <p>
        To obtain an estimate of country coverage, we count the number of times
        each country is mentioned in each document. This count is a simple word
        search based on a lookup list of country names (which includes multiple
        ways a country name can be spelled out; script and lookup file available
        <a href="#">here</a>). The counts are added to each document’s metadata.
        Combined with the information on the documents’ publication date and
        origin, this information allows us to generate aggregated counts by
        country and year (available <a href="#">here</a>), displayed in the
        following map.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "GeographicCoverage",
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
