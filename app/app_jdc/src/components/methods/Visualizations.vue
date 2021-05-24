<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <p>
        Visualization is a powerful tool to help unlock the potential of data.
        Data visualized could yield compelling and evidence-based data stories
        that could help in understanding trends, formulate interventions to
        improve any gaps in current policies, guide future policies, and ignite
        conversations in important issues.
      </p>
      <p>
        The data and metadata in our corpus and database are rich. While not
        exhaustively, we implemented visualizations to generate some examples of
        how the data and output of our models may be visualized to further the
        value of these data.
      </p>
      <p>The specific visualizations used are:</p>
      <ul>
        <li>
          Animated map chart – This visualization is used in the
          <router-link to="/explore/subcategories/geographic-coverage/"
            >Geographic coverage</router-link
          >
          page to demonstrate the variation in popularity of countries based on
          the count of mentions of the country in the documents year-over-year.
        </li>
        <li>
          <a
            href="https://echarts.apache.org/examples/en/editor.html?c=graph-label-overlap"
            target="_blank"
            >Graph chart</a
          >
          – The graph chart allows users to directly
          <router-link to="/explore/word-embeddings/"
            >interact with word embeddings</router-link
          >
          learned by the models. This tool shows how, and which words are
          related. This interactive visualization is designed to let users see
          the potential of word embeddings in the context of semantic search.
        </li>
        <li>
          Map charts based on
          <a href="https://github.com/maguayo/vue-map-chart" target="_blank"
            >vue-map-chart</a
          >
          – The map charts are used across different pages, mostly in document
          metadata page. It is also used in the
          <router-link to="/explore/similarity/">Analyze document</router-link>
          page to visualize which countries are popular in the user’s uploaded
          document.
        </li>
        <li>
          <a
            href="https://echarts.apache.org/examples/en/editor.html?c=bar-race-country"
            target="_blank"
            >Bar race chart</a
          >
          – The bar race chart is a recent invention for visualizing multiple
          timeseries. We have implemented a bar race chart of
          <router-link
            to="/explore/subcategories/geographic-coverage/#gc-race-chart"
            >most popular countries over time</router-link
          >
          in terms of cumulative mentions in documents.
        </li>
        <li>
          <a
            href="https://echarts.apache.org/examples/en/editor.html?c=area-stack"
            target="_blank"
            >Stacked area chart</a
          >
          – The stacked area chart is also used across pages in the project to
          compare different partitions of the data.
        </li>
        <li>
          Topic distribution bar charts (implemented using CSS) – This chart is
          used to visualize the proportion of topics present in the document as
          estimated by the LDA model.
        </li>
      </ul>
      <p>
        The frontend application is built with
        <a href="https://vuejs.org/" target="_blank">Vue.js</a> and we used
        <a href="https://echarts.apache.org/en/index.html" target="_blank"
          >Apache ECharts</a
        >
        for most of the interactive visualizations shown in the explore page.
        ECharts was chosen due to the library’s wide array of visualization
        options, flexibility, and performance. A Vue.js plugin (<a
          href="https://github.com/ecomfe/vue-echarts"
          target="_blank"
          >vue-echarts</a
        >) is also available which was used in the project to easily integrate
        ECharts into our project.
      </p>
      <p>
        We also forked
        <a href="https://github.com/maguayo/vue-map-chart" target="_blank"
          >vue-map-chart</a
        >
        and made key changes to accommodate for the
        <a
          href="http://documents1.worldbank.org/curated/en/154921467999692668/pdf/104857-MAN-Editorial-Style-Guide-PUBLIC.pdf"
          target="_blank"
          >World Bank’s map guidelines</a
        >. We also implemented new features to generate animated map chart.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Visualizations",
  props: {
    page_title: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
