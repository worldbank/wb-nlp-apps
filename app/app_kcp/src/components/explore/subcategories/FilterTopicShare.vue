<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      <p>Pending design</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "FilterTopicShare",
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
