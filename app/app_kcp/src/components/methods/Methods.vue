<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <p>
        Our project benefited considerably from methods and tools developed and
        made openly accessible by the community. We are equally committed to
        contribute to the public good, by making our processes transparent and
        reproducible to the extent possible. Apart from our web scrapers, all
        our scripts are available in our Github repository. We relied
        exclusively on open source solutions and are most grateful to all those
        who contributed to these tools.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Methods",
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
a {
  color: #42b983;
}
</style>
