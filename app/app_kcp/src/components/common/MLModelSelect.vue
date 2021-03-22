<template>
  <div class="model-select-wrapper">
    <!-- <b-form-select
      v-model="model_run_info_id"
      :options="model_run_infos"
    ></b-form-select> -->

    <model-select
      :options="model_run_infos"
      v-model="model_run_info_id"
      :placeholder="model_placeholder"
      class="wbg-model-select"
    >
    </model-select>
  </div>
</template>

<script>
import { ModelSelect } from "vue-search-select";

export default {
  name: "MLModelSelect",
  components: {
    ModelSelect,
  },
  props: {
    model_name: String,
    placeholder: String,
  },
  mounted() {
    this.model_run_infos = [];

    if (this.model_name === "lda") {
      this.model_run_infos = this.lda_model_run_infos;
    } else if (this.model_name === "word2vec") {
      this.model_run_infos = this.word2vec_model_run_infos;
    }
  },
  computed: {
    model_placeholder() {
      console.log(this.placeholder);
      if (this.placeholder !== undefined) {
        return this.placeholder;
      } else {
        return "Select model...";
      }
    },
  },
  data: function () {
    return {
      model_run_info_id: "",
      model_run_infos: [],
      lda_model_run_infos: [
        {
          value: "6694f3a38bc16dee91be5ccf4a64b6d8",
          text: "LDA model with 300 topics trained on all documents.",
        },
        {
          value: "6694f3a38bc16dee91be5ccf4a64b6d9",
          text: "LDA model with 100 topics trained on all documents.",
        },
      ],
      word2vec_model_run_infos: [
        {
          value: "777a9cf47411f6c4932e8941f177f90a",
          text: "Word2Vec model with 300 dimensions trained on all documents.",
        },
        {
          value: "777a9cf47411f6c4932e8941f177f90a",
          text: "Word2Vec model with 100 dimensions trained on all documents.",
        },
      ],
    };
  },
  // methods: {
  //   onSelectItem(event) {
  //     this.$emit("clicked", this.model_run_info_id);
  //   },
  // },
  watch: {
    model_run_info_id: function () {
      this.$emit("modelSelected", this.model_run_info_id);
    },
  },
};
</script>
<style scoped>
.model-select-wrapper {
  margin: 5px;
}
.wbg-model-select {
  border-color: var(--action-color) !important;
  color: var(--action-color) !important;
  border-radius: var(--border-radius-sm) !important;
  /* padding: 0.375rem 0.75rem !important; */
  font-weight: 400 !important;
  font-size: 1rem !important;
}

/* .wbg-model-select .text.default { */
div.default.text {
  color: var(--action-color-hover) !important;
}
</style>