<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      <p>
        Listed in the table below are details on the sources of the documents
        and metadata used in this project. We selected sections of each
        organization's website where relevant documents and metadata are found.
        A series of scrapers were implemented to capture available metadata as
        well as download the corresponding documents.
      </p>

      <p>
        In selecting the sources, we limit our selection to content that can be
        classified as publications, project documents, and research papers. We
        excluded documents pertaining to procurement plans, administrative
        tribunals, budgets, etc. However, we cannot guarantee that we have
        exhaustively filtered out documents of these types. Furthermore,
        documents that may be useful are likewise possible to be omitted. Since
        these documents are scraped, the dataset only covers content that are
        publicly available.
      </p>
      <p>
        The availability of the metadata is dependent on the source
        organization's published content. We tried to extract and curate as much
        of the metadata found on each source's page.
      </p>
      <br />
      <h3>List of data sources</h3>
      <div class="table-container text-left">
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
    this.items = this.$config.corpus_details;
    // this.$http.get("/static/data/corpus_details.json").then((response) => {
    //   this.items = response.data;
    // });
  },
  data: function () {
    return {
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
  height: 510px; */
}
</style>
