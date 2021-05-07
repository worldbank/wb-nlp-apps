<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <p>
        NLP requires text data to be converted to numerical values (vector) that
        models can use as inputs.
      </p>
      <p>
        Early techniques to convert text to vector includes
        <i>bag-of-words</i>—a strategy that builds a vector of values
        corresponding to the count of each word found in a document. Example we
        have a text <i>“the dog and the cat.”</i> This could be converted into a
        vector with values <code class="no-break">v = [1, 1, 1, 2]</code>. To
        come up with this vector, the unique words in the text are extracted and
        sorted alphabetically—<i>and</i>, <i>cat</i>, <i>dog</i>, <i>the</i>.
        Then, the vector is filled with the count of each word. The count for
        the word is placed based on the order that the words are sorted—<code
          class="no-break"
          >and = 1</code
        >
        is placed in the first position,
        <code class="no-break">cat = 1</code> in the second,
        <code class="no-break">dog = 1</code> in the third, and
        <code class="no-break">the = 2</code> is placed in the fourth position.
      </p>
      <p>
        The bag-of-words representation, even though quite simple, serve as a
        foundation in formulating other sophisticated strategies of turning text
        into numeric values, one of the most common is
        <a href="https://en.wikipedia.org/wiki/Tf%E2%80%93idf" _target="blank"
          >TF-IDF</a
        >. However, a curious observer will notice that the bag-of-words method
        has plenty of short comings, one of which is that it is purely a lexical
        representation. This means that if our application is designed to find
        relevant documents given a set of words, then texts without the keywords
        will not be considered despite being relevant. Example, a text without
        the word <i>“malnutrition”</i> but talks about <i>“stunting”</i> will be
        ignored despite it being likely to be relevant. This issue is one of the
        main problems that word embeddings attempt to solve.
      </p>
      <p>
        Word embedding is a more complex and abstract method of representing
        texts into vectors. In this paradigm, each word (or token as defined by
        the problem) is mapped to a vector that is learned by a model. The type
        of models that are used to generate word embeddings are usually trained
        to learn the vectors based on how words co-occur with other words. This
        technique can capture semantic information between words and
        <i>“embed”</i>
        similar or related words into vectors that look similar with each other.
        The entire text can be summarized using various strategies. One of the
        most common is by averaging the vector of words in the text to get a
        single vector to represent the text.
      </p>
      <p>
        One of our project’s key objectives is to formulate a way to make
        different types of data to be discoverable. We identified that word
        embeddings possess ideal properties to help us meet this objective. We
        select a variant of word embedding model—word2vec.
      </p>
      <p>
        The algorithm behind the word2vec model simple, yet the resulting
        vectors show surprising properties. We used the word2vec implementation
        in Gensim. The word2vec model is parametrized by some parameters but the
        main parameters that we experimented with are the window, size,
        skip-gram vs continuous, number of negative samples for the skip-gram
        implementation, and the number of iterations.
      </p>
      <p>
        To get a sense of these parameters, consider the text:
        <i>“The sky is blue now, but it might rain later.”</i>
      </p>
      <p>
        The <b>window</b> parameter controls the number of neighboring words
        that will be considered as the context for a word during training. So,
        if the model is in the process of optimizing the vector for
        <i>blue</i> and our window is set to 2, then the context words (without
        stop words removal) will include <i>sky</i> and <i>is</i> (left context)
        and <i>now</i> and <i>but</i> (right context). The model will try to
        learn a vector for <i>blue</i> that is generally close to these words.
        Different contexts may appear over different occurrences of the word
        <i>blue</i> in the whole corpus.
      </p>
      <p>
        We found that a small window results to embeddings that represent local
        relationships between words while a larger window results to embeddings
        that are more thematic in nature. This difference can be exploited
        depending on the desired use-case. If one wants to use the embeddings to
        find synonyms, considering a small window may be a good option. Instead,
        if one is interested in applying the embeddings to find broad topics
        within the corpus, a larger window could yield a better outcome.
        However, if compute resources are not a constraint, we always recommend
        experimenting with different values of the parameters.
      </p>
      <p>
        The <b>size</b> parameter corresponds to the number of values in the
        vector that is present in the word embeddings. This is also known as the
        dimension of the embeddings. A common range for this parameter is
        between 100 to 300 for models trained with a large corpus. There is a
        trade-off in memory, however, when a higher dimension is used.
      </p>
      (WIP)
    </div>
  </div>
</template>

<script>
export default {
  name: "WordEmbeddings",
  props: {
    page_title: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.no-break {
  white-space: nowrap;
}
</style>
