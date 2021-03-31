<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      This page discusses the details regarding the primary components of our
      text processing pipeline. The following sections include technical
      information about our selection of tools, techniques adopted and
      developed, as well as some insights on our learnings while iterating on
      the development of the pipeline.
      <hr />
      <h5>PDF processing</h5>
      <p>
        Raw documents scraped from the different organizations primarily come as
        PDF files. In order for us to apply NLP models to improve discovery of
        these documents, we need to convert these PDF files into text documents.
      </p>
      <p>
        Different libraries are available such as PDF2text, PDFminer, etc.
        However, the library that we found that is most robust and flexible is
        Apachetika. Apachetika is an open source library implemented in Java
        with wrappers for Python. We implemented a pipeline that automatically
        captures content of pages in a PDF file, perform initial cleaning such
        as detection of headers and footers, and produce a raw text version of
        the file. On top of that, our implementation also accepts source of
        different formats including URLs to PDF files or binary content.
      </p>
      <h5>Metadata normalization</h5>
      <p>
        The document repositories of the different organizations provide a
        variety of metadata. Some fields are common across sources such as
        title, authors, date of publication, and country, while most fields come
        as relatively similar but may imply different content such as topics
        especially when organizations use their respective curated taxonomies.
        Also, some sources provide a wider variety of information compared to
        other sources. Given these cases, we developed a schema that capture the
        most common fields and also attempted to normalize some of the different
        related fields such as topics and document types.
      </p>
      <p>
        After defining a schema and constraints, we wrote scripts for each data
        source to properly map and transform the native fields into the
        standardized schema. The steps of standardization include extraction of
        authors into a list, mapping of topics mapped into a list of curated
        items, extraction of year from the date of publication date, definition
        of corpus ID, assigning the link of the PDF document to the url_pdf
        field, and assigning the link of the text version of the document to the
        url_text field, etc.
      </p>
      <p>
        Further automated augmentation of the metadata from the contents of the
        document are done and will be further discussed below.
      </p>

      <p class="lead">Sample metadata</p>
      <div v-if="this.$config.sample_metadata" class="sample-metadata">
        <vue-json-pretty
          :data="this.$config.sample_metadata"
          :highlightMouseoverNode="true"
        >
        </vue-json-pretty>
      </div>

      <h5>Stop words</h5>
      <p>
        Stop words are list of curated words that are excluded in the vocabulary
        of an NLP model or analysis. In general, stop words are identified based
        on the amount of information that they possess. If a word doesn't covey
        any concrete meaning or information with respect to the context of the
        analysis or model, then it's useful for it to be excluded in the
        vocabulary. Example of these words are:
        <span class="stop-word">the</span>, <span class="stop-word">a</span>,
        <span class="stop-word">an</span>, <span class="stop-word">if</span>,
        and other common words. Other tokens that may add noise to the analysis
        are also added to the stop words, this may include roman numerals and
        prepositions.
      </p>
      <p>
        Most NLP libraries come with a predefined stop words list. In our case,
        we use a combined stopwords from NLTK, SpaCy, and a custom list. This
        stop words list is then used in our cleaning pipeline to remove the
        unimportant words in our final cleaned dataset.
      </p>
      <h5>Phrase detection</h5>
      <p>Phrase detection</p>
      <h5>Spell checking and vocabulary</h5>
      <p>Spell check</p>
      <h5>Acronym extraction</h5>
      <p>Acronyms</p>
      <h5>Named Entity Extraction</h5>
      <p>NER</p>
      <h5>Extraction of country counts</h5>
      <p>Country counts (include CSV file)</p>
      <h5>Language detection</h5>
      <p>Tokenization</p>
      <p>
        Simple interactive application showing before and after text cleaning of
        input text.
      </p>
    </div>
  </div>
</template>

<script>
import VueJsonPretty from "vue-json-pretty";
import "vue-json-pretty/lib/styles.css";

export default {
  name: "TextPreparation",
  components: { VueJsonPretty },
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
.sample-metadata {
  word-wrap: break-word;
  max-height: 400px;
  overflow-y: scroll;
  margin-bottom: 20px;
  border: 1px solid #8ab7ff;
  padding: 10px;
}
</style>
