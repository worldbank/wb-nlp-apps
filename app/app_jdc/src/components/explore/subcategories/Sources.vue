<template>
  <div>
    <header>
      <h1 class="blog-post-title mb-3" dir="auto">
        {{ page_title }}
      </h1>
    </header>
    <div>
      <p class="mt-3 text-justify">
        The corpus contains documents made publicly available by the UNHCR and
        five multilateral development banks MDBs). It is updated on a monthly
        basis. The documents were obtained by web scraping (all sources except
        World Bank) or by querying an API (World Bank). We do not distribute
        these documents, but we provide links to the documents in the
        originating sources. Broken links may occur when the sources (re)move
        documents from their respective website. Documents from the sources
        listed in the table below have been collected. To be included in our
        corpus, a document must:
      </p>
      <ul>
        <li>Be written in English</li>

        <li>Be available publicly</li>
        <li>
          Be of a relevant type (we are interested in analytical documents and
          reports, and in project documents from MDBs (excluding procurement
          documents and similar; we are interested in project descriptions,
          assessments, and reports)
        </li>
        <li>
          Be related to forced displacement; this is determined by setting a
          threshold on the refugee-related topic extracted from the LDA model,
          and by the presence of selected keywords in the document.
          <span style="font-weight: bold; color: red"
            >!!![when we have the exact filter, describe it here]!!!</span
          >
        </li>
      </ul>

      <br />
      <h3>List of data sources</h3>
      <div class="table-container">
        <b-table :fields="fields" :items="items">
          <template #cell(name)="data">
            <!-- `data.value` is the value after formatted by the Formatter -->
            <a :href="data.value.url" target="_blank">{{ data.value.name }}</a>
          </template>
        </b-table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Volume",
  props: {
    page_title: String,
  },
  mounted() {
    window.cvm = this;
    this.$http.get("/static/data/corpus_details.json").then((response) => {
      this.items = response.data.filter((o) =>
        this.valid_corpus_ids.includes(o.corpus_id)
      );
    });
  },
  data: function () {
    return {
      valid_corpus_ids: ["ADB", "AFDB", "EBRD", "IDB", "UNHCR", "WB"],
      items: [],
      fields: [
        {
          key: "name",
          label: "Organization",
          formatter: (value, key, item) => {
            return item;
          },
        },
        {
          key: "corpus_id",
          label: "Corpus ID",
          formatter: (value) => {
            return value;
          },
        },
        {
          key: "selection",
          label: "Description",
          formatter: (value) => {
            return value;
          },
        },
      ],
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
.table-container {
  /* overflow: scroll;
  height: 51
  0px; */
}

ul {
  list-style: disc;
  margin-top: 20px;
  padding-left: 50px;
}

li {
  margin-bottom: 5px;
}
</style>
