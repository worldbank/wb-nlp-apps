<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <p>Model description (Gensim / Mallet)</p>
      <p>Choice of nb of topics</p>
      <p>Priors?</p>
      <p>Labeling topics</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "LDATopicModel",
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
