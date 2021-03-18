<template>
  <div v-if="loading">
    <div class="document-row">
      <div class="row" v-for="v in Array(size)" :key="'sk_' + v">
        <div class="col-12">
          <b-skeleton height="231px"></b-skeleton>
        </div>
        <hr style="margin-top: 26px" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchResultLoading",
  props: {
    loading: Boolean,
    size: Number,
  },
};
</script>
