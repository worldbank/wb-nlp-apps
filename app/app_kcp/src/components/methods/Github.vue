<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <p>
        We open source the codebases that we implemented for the cleaning,
        processing, training of the models, APIs, and this application. The code
        are logically split into two repositories.
      </p>

      <p>
        The first repository contains a self-contained suite of text cleaning
        and data augmentation tools. Wrappers for
        <a
          href="https://github.com/worldbank/wb-nlp-tools/blob/main/src/wb_cleaning/translate/translation.py"
          target="_blank"
          >translation</a
        >
        of texts across languages are available in this repository. Tools to
        extract
        <a
          href="https://github.com/worldbank/wb-nlp-tools/blob/main/src/wb_cleaning/extraction/acronyms.py"
          target="_blank"
          >acronyms</a
        >,
        <a
          href="https://github.com/worldbank/wb-nlp-tools/blob/main/src/wb_cleaning/extraction/country_extractor.py"
          target="_blank"
          >country details</a
        >,
        <a
          href="https://github.com/worldbank/wb-nlp-tools/blob/main/src/wb_cleaning/extraction/pdf_cover.py"
          target="_blank"
          >covers of PDF documents</a
        >, etc. are available as well. A statistical method of automatically
        extracting specific text fragment in the language of interest is also
        <a
          href="https://github.com/worldbank/wb-nlp-tools/blob/main/src/wb_cleaning/extraction/english_content_extractor.py"
          target="_blank"
          >implemented</a
        >. This is useful when dealing with documents that contain multilingual
        contents but only contents in, example English, are of interest. The
        different tools that are available in this repository can be used by
        other users across other text analysis and data extraction use-cases.
      </p>
      <p>
        The second repository contains the code for the cleaning pipeline, the
        model training, modules for interacting with the interfaces (MongoDB,
        ElasticSearch, and Milvus), backend application APIs, and frontend of
        the application. This also contains the orchestration files for Docker
        and docker-compose to deploy the services of the application on a server
        easily.
      </p>
      <p>The two repositories are accessible at the links below.</p>
      <br /><br />
      <div class="row mb-2">
        <div class="col-12 col-md-6">
          <div class="wbg-homepage-block">
            <div class="wbg-homepage-block__fa">
              <i class="fab fa-github fa-lg" aria-hidden="true"></i>
            </div>
            <h3>
              <a
                href="https://github.com/worldbank/wb-nlp-tools"
                target="_blank"
                >Text processing tools</a
              >
            </h3>
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="wbg-homepage-block">
            <div class="wbg-homepage-block__fa">
              <i class="fab fa-github fa-lg" aria-hidden="true"></i>
            </div>
            <h3>
              <a href="https://github.com/worldbank/wb-nlp-apps" target="_blank"
                >Modeling and application</a
              >
            </h3>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Github",
  props: {
    page_title: String,
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
