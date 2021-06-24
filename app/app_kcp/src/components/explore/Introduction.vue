<template>
  <div>
    <!-- <h1>{{ page_title }}</h1> -->
    <div>
      <p>
        The <span style="font-weight: bold">Explore</span> pages provide a
        detailed description of the sources of documents that compose of our
        corpus. Additional insights regarding the corpus can be explored under
        the
        <router-link to="/explore/subcategories/geographic-coverage"
          >geographic coverage</router-link
        >
        page where we present the evolution of the volume of documents over time
        with respect to the countries they cover. Under the
        <router-link to="/explore/subcategories/metadata">metadata</router-link>
        subsection, we provide a brief outline about the metadata we collect or
        generate for each document. Lastly, the
        <router-link to="/explore/subcategories/training-subset">
          training subset</router-link
        >
        page contains links to a subset of our corpus, metadata, and repository
        containing the code to replicate our results.
      </p>
      <p>
        The project applied two categories of models commonly used in natural
        language processing (NLP) to analyze and extract information from
        unstructured text data. The first is
        <router-link to="/methods/lda"> topic modeling</router-link> and the
        second is
        <router-link to="/methods/word-embeddings">word embedding</router-link>
        model. The
        <router-link to="/explore/topic-composition"
          >topic composition</router-link
        >
        section of the Explore pages highlights some practical use-cases of
        topic models. The
        <router-link to="/explore/subcategories/topic-browser"
          >topic browser</router-link
        >
        page provides an interactive visualization of the topics learned by the
        topic model. The
        <router-link to="/explore/subcategories/filtering-by-topic-share"
          >filtering by topic share</router-link
        >
        page explores a novel way of discovering documents by setting a desired
        level of topic intensity for one or a combination of topics. Topic model
        also allow us to analyze the evolution of topic popularity across
        document types and over time. This feature can be explored in the
        <router-link to="/explore/topic-profiles">topic profiles</router-link>
        page.
      </p>
      <p>
        More information on the NLP approaches that we implemented is available
        in the
        <router-link to="/methods">Methods and Tools</router-link> section of
        the site, and reproducible code (except the scrapers) is available in
        <router-link to="/methods/github">GitHub</router-link>.
      </p>
    </div>

    <!-- <footer>
              <section>
                <h4>Share</h4>
                <nav class="nav sharing-icons mt-4">
                  <a
                    class="nav-item"
                    href="https://www.facebook.com/sharer/sharer.php?u=%2fexplore%2fexplore%2f"
                    title="Share on Facebook"
                    ><span
                      class="fab fa-facebook-f fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://www.linkedin.com/shareArticle?mini=true&amp;url=%2fexplore%2fexplore%2f"
                    title="Share on LinkedIn"
                    ><span
                      class="fab fa-linkedin-in fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://twitter.com/intent/tweet?url=%2fexplore%2fexplore%2f&amp;text=Explore"
                    title="Tweet this"
                    ><span
                      class="fab fa-twitter fa-lg"
                      aria-hidden="true"
                    ></span
                  ></a>
                </nav>
              </section>
            </footer> -->
  </div>
</template>

<script>
export default {
  name: "Introduction",
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
/* a {
  color: #42b983;
} */
</style>
