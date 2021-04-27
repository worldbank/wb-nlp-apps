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
    parent_model_run_info_id: String,
  },
  mounted() {
    this.model_run_infos = [];

    this.getModelRunInfos();

    // if (this.model_name === "lda") {
    //   this.model_run_infos = this.lda_model_run_infos;
    // } else if (this.model_name === "word2vec") {
    //   this.model_run_infos = this.word2vec_model_run_infos;
    // }

    if (this.parent_model_run_info_id) {
      this.model_run_info_id = this.parent_model_run_info_id;
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
    };
  },
  methods: {
    getModelRunInfos() {
      var url = "";
      if (this.model_name === "word2vec") {
        url = "/nlp/models/get_available_models?model_type=" + this.model_name;
      } else {
        url =
          "/nlp/models/get_available_models?model_type=lda&model_type=mallet";
      }

      this.$http.get(url).then((response) => {
        this.model_run_infos = response.data.map((o) => {
          return {
            value: o.model_run_info_id,
            text: o.description,
            model_run_info_id: o.model_run_info_id,
            model_name: o.model_name,
          };
        });
        this.model_run_info_id = this.model_run_infos[
          this.model_run_infos.length - 1
        ].model_run_info_id;
      });
    },
  },
  watch: {
    model_run_info_id: function () {
      var result = this.model_run_infos.find(
        (obj) => obj.value === this.model_run_info_id
      );

      if (result.model_name === "word2vec") {
        result["url"] = this.$config.nlp_api_url.word2vec;
      } else if (result.model_name === "lda") {
        result["url"] = this.$config.nlp_api_url.lda;
      } else if (result.model_name === "mallet") {
        result["url"] = this.$config.nlp_api_url.mallet;
      }

      this.$emit("modelSelected", result);
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