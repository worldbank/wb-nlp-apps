<template>
  <div>
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      <p>
        Our corpus is composed of documents made publicly accessible by various
        agencies (listed below) involved in international development. These
        agencies were selected to cover a diversity of themes related to
        socio-economic development. We will keep enriching this corpus in the
        future.
      </p>
      <p>
        This corpus was built over several months by querying APIs when
        available, or by scraping websites. It is maintained on a regular basis
        using an automated (<a href="https://nifi.apache.org/">Apache NiFi</a
        >-based) system. Core metadata on each document (title, author, URL,
        type of document, abstract, etc. based on availability) are collected at
        the document acquisition stage. Information extraction procedures and
        NLP models are then applied to generate additional metadata (including
        number of tokens, country counts, topic composition, acronyms,
        extraction of named entities, and others). These approaches are
        described in the Methods & Tools section. The Metadata section provides
        a description of, and access to, the information collected on each
        document.
      </p>
      <p>
        <b
          >We do not provide direct access to any of the documents we
          process.</b
        >
        We only publish information on the documents, including a link to the
        document in its website of origin. We periodically check the links and
        try to fix broken URLs, but we do not guarantee that all documents are
        and will remain accessible. Links that are found to be broken at two
        successive checks are temporarily of definitively removed from our
        catalog.
      </p>

      <h4>Scope</h4>
      <p>
        The corpus … (project, research/knowledge) No exclusion based on
        region/country, but development means focus on low and middle-income
        countries. See section on Geographic coverage.
      </p>
      <h4>Volume</h4>
      <p>
        As of {{ date_now }}, our corpus contains
        {{ corpus_size.toLocaleString() }} documents from
        {{ org_count }} organizations, representing a total of
        {{ total_tokens.toLocaleString() }} useful words (‘tokens’). The volume
        has increased considerably after year 2000. Useful words are the words
        that are left in a document after it goes through our text cleaning
        pipeline, which excludes stop words, words not found in the English
        dictionary or Wikipedia (after spell checking and automatic correction
        is applied). Many documents in our corpus, especially older documents,
        are scanned documents converted to text using OCR. OCR errors generated
        a significant number of unknown words which could not be automatically
        corrected and created noise that had to be excluded.
      </p>
      <h4>Languages</h4>
      <p>
        Our corpus is intended to be a corpus of documents in English. Some of
        the scraped documents may be multi-lingual, and others may be in other
        languages. Automatic language detection was applied to retain English
        documents only. As our corpus is largely composed of documents from
        international agencies or regional agencies from the United Nations
        system, the selection of English documents is not considered as a major
        issue for most of the purposes we pursue. We made an exception for
        documents originating from the African Development Bank or Interamerican
        Development Bank, for the needs of a project that requires a
        comprehensive corpus of documents from multilateral development banks.
        Documents written in French and Spanish have been translated using
        Google / Amazon translation services. Although the translations may not
        be perfect, they were found to be remarkably good and suitable for being
        used in word embedding and topic models.
      </p>
      <h4>Exclusions</h4>
      <p>
        We have excluded documents that were found to have too little relevant
        content. This includes documents that, after processing, contained less
        than 250 tokens. We also excluded documents like procurement plans,
        reports from administrative tribunals, budgets, and other administrative
        documents. This exclusion is based on some heuristics and cannot be
        guaranteed without errors of inclusion or exclusion.
      </p>
      <h4>Sources</h4>
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
  name: "Corpus",
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
