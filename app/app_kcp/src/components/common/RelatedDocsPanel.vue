<template>
  <vue-horizontal>
    <!-- <section v-for="item in items" :key="item.title"> -->
    <div class="related-section" v-for="item in items" :key="item.title">
      <div class="related-document-row" data-url="#" title="View study">
        <div class="row">
          <div class="col-12">
            <span class="title">
              <a :href="result.url_pdf" :title="result.title">{{
                result.title
              }}</a>
            </span>
            <div class="study-country">
              {{ result.country[0] }}, {{ result.year }}
            </div>
            <div class="survey-stats">
              <span>Created on: {{ getDate(result.date_published) }} </span
              ><br />
              <span>Last modified: {{ getDate(result.last_update_date) }} </span
              ><br />
              <span>Views: {{ result.views }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- <h3>{{ item.title }}</h3>
      <p>{{ item.content }}</p> -->
      <!-- </section> -->
    </div>
  </vue-horizontal>
</template>

<script>
import VueHorizontal from "vue-horizontal";

export default {
  components: { VueHorizontal },
  props: {
    result: Object,
  },
  data() {
    return {
      // E.g: creates 20 array items...
      items: [...Array(20).keys()].map((i) => {
        return { title: `Item ${i}`, content: `🚀 Content ${i}` };
      }),
    };
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

<style scoped>
/* <!-- Peeking Style --> */
/* .horizontal >>> .v-hl-container {
  scroll-padding-left: 16px;
  scroll-padding-right: 16px;
} */

.related-document-row {
  margin-top: 0;
}

.related-document-row .title {
  font-size: 0.85rem;
}

.related-document-row .survey-stats {
  font-size: 0.65rem;
  opacity: 0.7;
  margin: 8px auto;
}

.related-document-row .study-country {
  font-size: 0.75rem;
}

.vue-horizontal {
  border: 3px solid #dbdbdb;
  padding: 5px;
}
.related-section {
  width: 33vh;
  padding: 10px 5px;
  margin: 3px;
  height: 150px;
  background: #ffffff;
  border: 1px solid #7b7b7b;
  border-radius: 4px;
}
</style>

