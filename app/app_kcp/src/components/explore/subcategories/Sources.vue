<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      <p>
        Collect documents from selected sections of the organizations’ website.
        Then run some procedure to exclude some documents (too short, not a
        readable format, etc.). No interest in procurement plans, administrative
        tribunal, budgets, … We cannot guarantee that all have been excluded,
        and that no useful document has been missed. Exclude documents that are
        not publicly available.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Sources",
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
