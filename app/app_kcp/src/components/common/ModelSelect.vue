<template>
  <div>
    <b-form-select
      v-model="model_run_info_id"
      :options="model_run_infos"
    ></b-form-select>
  </div>
</template>

<script>
export default {
  name: "ModelSelect",
  props: {
    model_name: String,
  },
  data: function () {
    return {
      model_run_info_id: "",
      model_run_infos: [
        {
          value: "6694f3a38bc16dee91be5ccf4a64b6d8",
          text: "LDA model with 300 topics trained on all documents.",
        },
        {
          value: "6694f3a38bc16dee91be5ccf4a64b6d9",
          text: "LDA model with 100 topics trained on all documents.",
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