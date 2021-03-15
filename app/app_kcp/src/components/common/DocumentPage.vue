<template>
  <div>
    <!-- <Header /> -->
    <div class="container">
      <div class="row">
        <h1>{{ $route.params.doc_id }}</h1>
      </div>
    </div>
  </div>
</template>

<script>
// import Header from "../Header.vue";

export default {
  name: "DocumentPage",
  props: {
    metadata: Object,
  },
  mounted() {},
  //   components: { Header },
  data: function () {
    return {};
  },
  methods: {},
};
</script>
