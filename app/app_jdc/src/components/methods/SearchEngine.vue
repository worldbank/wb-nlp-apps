<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <p>
        Keyword search is a common tool for users to find relevant information.
        While the focus of this project is to explore, develop, and apply NLP
        models to improve the discoverability of text data, we also recognize
        the immense power of a well tuned keyword search engine. This motivated
        us to integrate a full-text search engine on the platform.
      </p>
      <p>
        The most common tool used in applications to find data in databases is
        <b>keyword search</b>. A keyword search provides users an interface with
        a search engine to define and submit keyword(s) which they assume would
        best satisfy their “information need.” A keyword search gives people
        what they want assuming (1) people use the most relevant keyword(s) and
        (2) the search engine used is optimized to handle the type of queries
        from the user. However, a vast portion of relevant knowledge may not
        contain the exact word(s) that users choose as keywords in their search.
        Furthermore, words with multiple meaning may result to sub-optimal
        search results.
      </p>
      <p>
        While it is not yet as common as keyword search,
        <b>semantic search</b> offers a new paradigm on how users interact with
        and discover data. Semantic search leverages various NLP methods and
        models to form semantic relationships between words and other entities
        in the database. These semantic relationships go beyond how the words
        are structured; the models used in sematic search often attempt to learn
        which words are close with each other based on how they are used and how
        words co-occur in documents. This property implicitly allows users to
        search in terms of themes so that even documents that don’t have the
        words in the query chosen by users may still be retrieved.
      </p>
      <p>
        These two complementary strategies for building text search: keyword
        search and semantic search, are implemented in this project. They
        complement each other since: (1) keyword search guarantees a user to get
        the documents that contain the keywords that they want, whereas (2) the
        semantic search return results that may contain other relevant
        information that, even without the keyword in the document, may still be
        of interest to the user. These two methods of searching could fit in the
        “exploration vs. exploitation” paradigm of optimizing for information
        retrieval: the former “exploits” the existing knowledge of users while
        the latter allows users to “explore.”
      </p>
      <h4>Implementing the keywords search</h4>
      <p>
        The backend of the search engine for the keyword search used in this
        project is
        <a href="https://www.elastic.co/" target="_blank">Elasticsearch</a>.
        Elasticsearch powers efficient and scalable full-text search
        functionality and is based on Apache Lucene. Elasticsearch has good
        Python wrappers and for this project we relied heavily on the
        <a
          href="https://elasticsearch-dsl.readthedocs.io/en/latest/"
          target="_blank"
          >Elasticsearch DSL</a
        >
        library. The current version has missing functionalities, however, so we
        <a
          href="https://github.com/avsolatorio/elasticsearch-dsl-py"
          target="_blank"
          >forked</a
        >
        the DSL library and introduced some improvements. We will attempt to
        introduce these small additions back to the main branch as improvements
        via PRs.
      </p>
      <p>
        We used the docker installation of Elasticsearch to fit with our overall
        service-oriented architecture. We deployed 1 replica and 2 shards for
        the service. This configuration can easily be updated as necessary.
      </p>
      <p>
        We indexed the raw text extracted from our collection of PDFs. The
        metadata is also stored in the index. Specific data types were assigned
        accordingly. Texts and abstracts were assigned as a text data with the
        Snowball analyzer which does stemming of the words. Other fields were
        set to have the keyword type for exact term search. Some of the fields
        set as keywords are authors, corpus, country, topics, document type,
        etc.
      </p>
      <p>
        Since some documents have very long text, we also needed to increase the
        <b>highlight.max_analyzed_offset</b> configuration since the default
        value caused problems when processing these long documents when we
        enabled the highlight feature.
      </p>
      <p>
        We also implemented custom preprocessing to improve the search
        experience of users including the automatic translation of queries to
        English and the identification of countries associated with country
        group(s) found in the search query. Example, the query “poverty in
        ASEAN” will detect the ASEAN keyword and expand it to automatically add
        the list of ASEAN’s member countries as filters. We plan to further
        enrich our preprocessing analyzers to better anticipate and help users
        with their information need.
      </p>
      (WIP)
      <!--
      <p>
        We are using
        <a href="https://www.elastic.co/" target="_blank">Elasticsearch</a> as
        our full-text search engine.
      </p> -->
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchEngine",
  props: {
    page_title: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* h3 {
  margin: 40px 0 0;
}
a {
  color: #42b983;
} */
</style>
