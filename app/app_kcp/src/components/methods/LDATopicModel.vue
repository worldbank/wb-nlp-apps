<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <p>
        One of the challenges that hinders the wide adoption of text data in
        analytics is the common unavailability of structured metadata that could
        help describe the text, e.g., extracted texts from PDF documents only
        come with the raw text. Metadata like title, tags or topics, abstract,
        date published, etc. are not available “out-of-the-box.”
      </p>
      <p>
        In most cases, NLP could be applied to unstructured text data to build
        structured knowledge. Some questions of interest when analyzing text
        data, especially a large corpus, are—what topics and themes are
        contained in the corpus? How do these topics vary and evolve over time?
        How “important” is one topic over the other? Topic models are a powerful
        tool to build structure and help answer these questions.
      </p>

      <p>
        <b>Topic models</b> are a class of unsupervised machine learning models
        that attempt to learn topics from a collection of documents. One of the
        most popular topic modeling algorithms is the
        <b>Latent Dirichlet Allocation</b> (LDA). The LDA uses only the words
        and their frequency in documents as input. Different optimization
        strategies may be used to train the model depending on the variant of
        the LDA. The models used in this work employ Gibbs sampling (Mallet) and
        variational bayes algorithm (Gensim).
      </p>
      <p>
        We used the implementation of the LDA from Gensim and Mallet. Our
        initial tests suggested that, while the topic model itself has
        parameters that can be tuned, maximizing the quality of the input data
        is more impactful in having robust and interpretable topic models. We
        set up a pipeline of text processing specific for the data that was used
        to train the topic models. This was made possible by the composable text
        <router-link to="/methods/text-preparation"
          >cleaning toolkit</router-link
        >
        that we have developed.
      </p>
      <p>
        We found that limiting the words based on part-of-speech improves the
        interpretability of the resulting topics. The part-of-speech of words
        that were included was limited to nouns, adjectives, and adverbs. While
        we generally considered adverbs as acceptable words, some of the more
        common and less informative adverbs were added into our stop words list
        such as typically, usually, likely, etc.
      </p>
      <p>
        Despite the cleaning, some topics learned by the models were still found
        to be non-informative or irrelevant. This is one of the pitfalls of
        unsupervised models, i.e., we can’t predict a priori how or what topics
        will be captured; nonetheless, most of the topics that we captured are
        relevant. To address this, we analyzed the topics learned by the models
        and tagged which ones are to be excluded.
      </p>
      <p>(WIP)</p>
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
</style>
