<template>
  <footer>
    <section>
      <h4>Share</h4>
      <nav class="nav sharing-icons mt-4">
        <a
          class="nav-item"
          :href="'https://www.facebook.com/sharer/sharer.php?u=' + url"
          title="Share on Facebook"
          ><span class="fab fa-facebook-f fa-lg" aria-hidden="true"></span
        ></a>
        <a
          class="nav-item"
          :href="
            'https://www.linkedin.com/shareArticle?mini=true&amp;url=' + url
          "
          title="Share on LinkedIn"
          ><span class="fab fa-linkedin-in fa-lg" aria-hidden="true"></span
        ></a>
        <a
          class="nav-item"
          :href="
            'https://twitter.com/intent/tweet?url=' + url + '&amp;text=' + text
          "
          title="Tweet this"
          ><span class="fab fa-twitter fa-lg" aria-hidden="true"></span
        ></a>
      </nav>
    </section>
  </footer>
</template>

<script>
export default {
  name: "PageFooter",
  props: {
    url: String,
    text: String,
  },
};
</script>
