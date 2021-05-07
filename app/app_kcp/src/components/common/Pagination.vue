<template>
  <div class="nada-pagination mt-5">
    <div
      class="row mt-3 mb-3 d-flex justify-content-lg-between align-items-center"
    >
      <div class="col-12 col-lg-6 mb-3 small">
        <div id="items-per-page" class="items-per-page light switch-page-size">
          <small
            >Results per page:
            <a href="#results">
              <span
                class="wbg-pagination-btn"
                :class="size === curr_size ? 'active' : ''"
                v-for="size in page_sizes"
                v-bind:key="size"
                @click="setSize(size)"
                >{{ size }}</span
              ></a
            >
          </small>
        </div>
      </div>
      <div class="col-12 col-lg-6 d-flex justify-content-lg-end">
        <nav aria-label="Page navigation">
          <ul class="pagination pagination-md wbg-pagination-ul small">
            <li class="page-item" v-if="curr_page_num - page_window > 1">
              <a
                href="#results"
                @click="sendPageNum(1)"
                class="page-link"
                :data-page="0"
                title="First"
                >«</a
              >
            </li>
            <li
              class="page-item"
              v-for="page_num in num_pages"
              v-bind:key="page_num"
            >
              <div v-if="Math.abs(curr_page_num - page_num) <= page_window">
                <a
                  href="#results"
                  @click="sendPageNum(page_num)"
                  class="page-link"
                  :class="page_num === curr_page_num ? 'active' : ''"
                  :data-page="page_num"
                  >{{ page_num }}</a
                >
              </div>
            </li>

            <li class="page-item" v-show="has_hits || next_override">
              <a
                href="#results"
                @click="sendPageNum(next)"
                class="page-link"
                data-page="2"
                >Next</a
              >
            </li>
            <li class="page-item" v-show="has_hits || next_override">
              <a
                href="#results"
                @click="sendPageNum(num_pages)"
                class="page-link"
                :data-page="num_pages + 1"
                title="Last"
                >»</a
              >
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "Pagination",
  props: {
    num_pages: Number,
    curr_page_num: Number,
    has_hits: Boolean, // hits.length > 0 && !no_more_hits
    size: Number,
    page_sizes: Array,
    page_window: Number,
    next: Number,
    next_override: Boolean,
  },
  data: function () {
    return {
      curr_size: this.$config.pagination.size,
    };
  },
  methods: {
    setSize: function (size) {
      this.curr_size = size;
      this.$emit("currSizeSet", this.curr_size);
    },
    sendPageNum: function (page_num) {
      this.$emit("pageNumReceived", page_num);
    },
  },
};
</script>
