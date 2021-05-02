<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      <p>
        Knowledge produced may be measured by the volume of documents published.
      </p>

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
    this.$http.get("/static/data/corpus_details.json").then((response) => {
      this.items = response.data;
    });
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
