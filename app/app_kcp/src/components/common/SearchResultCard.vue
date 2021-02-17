<template>
  <div>
    <div class="document-row" data-url="#" title="View study">
      <div class="row">
        <div class="col-3 col-lg-3">
          <img
            src="/static/files/doc_thumb.png"
            title="document thumbnail"
            alt="document thumbnail"
          />
        </div>
        <div class="col-9 col-lg-9">
          <span class="badge badge-primary wbg-badge">DOCUMENT</span>
          <h5 class="title">
            <a :href="result.url_pdf" :title="result.title">{{
              result.title
            }}</a>
          </h5>
          <div class="study-country">
            {{ result.country[0] }}, {{ result.year }}
          </div>
          <div class="sub-title">
            <div>
              <span class="study-by">Ministry of Public Health</span>
            </div>
            <div class="owner-collection">
              Corpus:
              <router-link to="/search/">{{ result.corpus }}</router-link>
            </div>
          </div>
          <div class="survey-stats">
            <span>Created on: {{ getDate(result.date_published) }} </span>
            <span>Last modified: {{ getDate(result.last_update_date) }} </span>
            <span>Views: {{ result.views }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchResultCard",
  props: {
    result: Object,
  },
  methods: {
    getDate: function (date) {
      date = new Date(date).toDateString();
      date = date.split(" ");

      return date[1] + " " + date[2] + ", " + date[3];
    },
  },
};
</script>