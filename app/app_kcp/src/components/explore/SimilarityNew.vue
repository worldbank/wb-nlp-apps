<template>
  <div>
    <header>
      <h1 class="blog-post-title mb-3" dir="auto">
        <a
          href="https://mtt-wb21h.netlify.app/explore/subcategories/filtering_by_topic_share/"
          >{{ page_title }}</a
        >
      </h1>
    </header>
    <div>
      <article class="blog-post">
        <h2>Heading two</h2>
        <p class="lead">
          Describe how we measure similarity between documents. Then provide the
          possibility to copy a document, or provide the URL of a TXT, DOC or
          PDF document (from our own catalog or external). The system should
          return (i) a list of N closest matches, and (ii) the topic composition
          for LDA model X.
        </p>
        <p>
          Describe how we measure similarity between documents. Then provide the
          possibility to copy a document, or provide the URL of a TXT, DOC or
          PDF document (from our own catalog or external). The system should
          return (i) a list of N closest matches, and (ii) the topic composition
          for LDA model X.
        </p>
        <div class="d-md-flex">
          <!-- <div class="dropdown mr-3 mr-3 mb-3 mb-md-0">
            <button
              class="btn btn-outline-secondary wbg-button dropdown-toggle"
              type="button"
              id="dropdownMenuButton"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Word2vec Model ALL_50
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
              <a
                class="dropdown-item"
                href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                >Action</a
              >
              <a
                class="dropdown-item"
                href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                >Another action</a
              >
              <a
                class="dropdown-item"
                href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                >Something else here</a
              >
            </div>
          </div>
          <div class="dropdown">
            <button
              class="btn btn-outline-secondary wbg-button dropdown-toggle"
              type="button"
              id="dropdownMenuButton"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              LDA Model ALL_50
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
              <a
                class="dropdown-item"
                href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                >Action</a
              >
              <a
                class="dropdown-item"
                href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                >Another action</a
              >
              <a
                class="dropdown-item"
                href="https://mtt-wb21h.netlify.app/explore/similarity/#"
                >Something else here</a
              >
            </div>
          </div> -->
        </div>
        <div class="row">
          <div class="col-6 fluid">
            <MLModelSelect
              @modelSelected="onModelSelectWord2Vec"
              :model_name="'word2vec'"
              placeholder="Choose a word embedding model..."
            />
          </div>
          <div class="col-6 fluid">
            <MLModelSelect
              @modelSelected="onModelSelectLDA"
              :model_name="'lda'"
              placeholder="Choose a topic model..."
            />
          </div>
        </div>

        <br />

        <center>
          <b-form-group label="" v-slot="{ ariaDescribedby }">
            <b-form-radio-group
              id="radio-group-1"
              v-model="selectedInput"
              :options="uploadOptions"
              :aria-describedby="ariaDescribedby"
              name="radio-options"
            ></b-form-radio-group>
          </b-form-group>
        </center>

        <form class="mt-4">
          <div
            v-if="selectedInput == 'file_upload'"
            class="input-group wbg-input-group mb-3 mt-3"
            style="display: flex"
            @click="$refs.simFile.click()"
          >
            <input
              type="text"
              class="form-control wbg-search-text pl-4"
              aria-describedby="basic-addon2"
              disabled
            />
            <div>
              <div
                id="submit_file"
                data-toggle="tooltip"
                data-placement="bottom"
                title="Upload a PDF or TXT document to search"
              >
                <div class="file-input">
                  <input
                    @change="fileUpload"
                    type="file"
                    ref="simFile"
                    name="file-input-similarity"
                    :value="file_input"
                    :disabled="hasUploadedFile"
                    id="file-input-similarity"
                    class="file-input__input"
                    data-toggle="tooltip"
                    data-placement="bottom"
                    title="Upload a PDF or TXT document to search"
                    accept=".txt,.doc,.docx,.pdf"
                  />
                  <label
                    class="file-input__label file-input__label__similarity"
                    for="file-input-similarity"
                    ><i
                      class="fas fa-file-upload fa-lg"
                      :style="hasUploadedFile ? 'color: gray' : ''"
                    ></i
                  ></label>
                </div>
              </div>
            </div>
            <div
              v-if="hasUploadedFile"
              v-show="hasUploadedFile"
              class="wbg-uploaded-file wbg-uploaded-file__similarity"
            >
              {{ this.uploaded_file.name }}
              <i
                class="fas fa-times fa-sm ml-2"
                @click="removeFile"
                aria-hidden="true"
              ></i>
            </div>
          </div>

          <label
            v-if="selectedInput == 'url_upload'"
            class="sr-only"
            for="inlineFormInputGroup"
            >Enter URL of PDF or TXT file</label
          >
          <div v-if="selectedInput == 'url_upload'" class="input-group mb-2">
            <div class="input-group-prepend">
              <div class="input-group-text">
                <i class="fas fa-link fa-md" aria-hidden="true"></i>
              </div>
            </div>

            <input
              type="text"
              class="form-control"
              id="inlineFormInputGroup"
              placeholder="Enter URL of file"
              v-model="url"
            />
          </div>
          <br />
          <b-button
            class="btn btn-primary wbg-button"
            @click="sendSearch()"
            :disabled="!stateReady"
            :variant="stateReady ? 'primary' : 'secondary'"
            >Find similar documents</b-button
          >
        </form>
        <br />
        <a name="results"></a>
        <h3 class="mt-4 mb-3">Comparison of results</h3>

        <b-tabs v-model="tabIndex" content-class="mt-3">
          <b-tab title="Embedding model" active>
            <SearchResultLoading :loading="loading" :size="size" />
            <div v-show="model_option.hits.length > 0">
              <div v-if="!loading">
                <SearchResultCard
                  v-for="result in model_option.hits"
                  :result="result"
                  v-bind:key="'word2vec_' + result.id"
                />
              </div>

              <Pagination
                @pageNumReceived="sendSearch"
                :num_pages="model_option.num_pages"
                :curr_page_num="model_option.curr_page_num"
                :has_hits="has_hits"
                :page_sizes="page_sizes"
                :page_window="page_window"
                :next="model_option.next"
                :next_override="next_override"
              /></div
          ></b-tab>
          <b-tab title="Topic model">
            <SearchResultLoading :loading="loading" :size="size" />
            <div v-show="model_option.hits.length > 0">
              <div v-if="!loading">
                <SearchResultCard
                  v-for="result in model_option.hits"
                  :result="result"
                  v-bind:key="'lda_' + result.id"
                />
              </div>

              <Pagination
                @pageNumReceived="sendSearch"
                :num_pages="model_option.num_pages"
                :curr_page_num="model_option.curr_page_num"
                :has_hits="has_hits"
                :page_sizes="page_sizes"
                :page_window="page_window"
                :next="model_option.next"
                :next_override="next_override"
              /></div
          ></b-tab>
        </b-tabs>

        <hr />
        <PageFooter :url="share_url" :share_text="share_text" />
      </article>
    </div>
  </div>
</template>

<script>
import MLModelSelect from "../common/MLModelSelect";
import SearchResultLoading from "../common/SearchResultLoading";
import SearchResultCard from "../common/SearchResultCard";
import Pagination from "../common/Pagination";

import PageFooter from "../common/PageFooter";

export default {
  name: "SimilarityNew",
  props: {
    page_title: String,
    share_url: String,
    share_text: String,
  },
  components: {
    PageFooter,
    MLModelSelect,
    SearchResultLoading,
    SearchResultCard,
    Pagination,
  },
  mounted() {
    window.vm = this;
  },
  data() {
    return {
      // common
      tabIndex: 0,
      page_sizes: [10, 25, 50, 100],
      page_window: 2,
      curr_size: 10,
      size: 10,
      next_override: true,
      model_name: {
        word2vec: "word2vec",
        lda: "lda",
      },
      model_options: {
        lda: {
          upload_nlp_api_url: "/nlp/search/lda/file",
          url_nlp_api_url: "/nlp/search/lda/url",
          model_run_info_id: "",
          model_id: null,
          curr_page_num: 1,
          next: 0,
          num_pages: 0,
          from_result: 0,
          hits: [],
          total: Object,
        },
        word2vec: {
          upload_nlp_api_url: "/nlp/search/word2vec/file",
          url_nlp_api_url: "/nlp/search/word2vec/url",
          model_run_info_id: "",
          model_id: null,
          curr_page_num: 1,
          next: 0,
          num_pages: 0,
          from_result: 0,
          hits: [],
          total: Object,
        },
      },

      errored: false,
      loading: false,

      url: "",
      uploaded_file: null,
      file_input: null,
      url_cache: "",
      selectedInput: "file_upload",
      uploadOptions: [
        {
          html: "<strong>Upload PDF or TXT file</strong>",
          value: "file_upload",
        },
        {
          html: "<strong>Input URL to PDF or TXT file</strong>",
          value: "url_upload",
        },
      ],
    };
  },
  computed: {
    stateReady() {
      if (this.model_options[this.model_name.word2vec].model_id !== null) {
        if (this.model_options[this.model_name.lda].model_id !== null) {
          if (this.url !== "" || this.uploaded_file !== null) return true;
        }
      }
      return false;
    },
    apiUrl() {
      if (this.selectedInput === "file_upload") {
        return this.model_option.upload_nlp_api_url;
      } else {
        return this.model_option.url_nlp_api_url;
      }
    },
    model_option() {
      return this.model_options[this.selectedModel];
    },
    apiParams() {
      const formData = new FormData();
      formData.append("model_id", this.model_option.model_id); // "777a9cf47411f6c4932e8941f177f90a");

      if (this.selectedInput === "file_upload") {
        formData.append("file", this.uploaded_file);
      } else {
        formData.append("url", this.url);
      }
      formData.append("from_result", this.model_option.from_result);
      formData.append("size", this.curr_size);
      return formData;
    },
    selectedModel() {
      if (this.tabIndex === 0) {
        return this.model_name.word2vec;
      } else if (this.tabIndex === 1) {
        return this.model_name.lda;
      } else {
        return null;
      }
    },
    hasUploadedFile() {
      if (this.uploaded_file !== null) {
        if (this.uploaded_file.name !== undefined) {
          return true;
        }
      }
      return false;
    },
    no_more_hits() {
      var next_from = this.model_option.curr_page_num * this.curr_size;

      var no_more_hits = false;
      if (next_from > this.model_option.total.value) {
        no_more_hits = true;
      }

      return no_more_hits;
    },
    has_hits() {
      return this.model_option.hits.length > 0 && !this.no_more_hits;
    },
    // word2vec_no_more_hits() {
    //   var next_from = this.word2vec_curr_page_num * this.curr_size;

    //   var no_more_hits = false;
    //   if (next_from > this.word2vec_total.value) {
    //     no_more_hits = true;
    //   }

    //   return no_more_hits;
    // },
    // lda_no_more_hits() {
    //   var next_from = this.lda_curr_page_num * this.curr_size;

    //   var no_more_hits = false;
    //   if (next_from > this.lda_total.value) {
    //     no_more_hits = true;
    //   }

    //   return no_more_hits;
    // },
  },
  methods: {
    onModelSelectWord2Vec(model_run_info_id) {
      console.log(model_run_info_id);
      this.model_options[this.model_name.word2vec].model_id = model_run_info_id;
    },
    onModelSelectLDA(model_run_info_id) {
      console.log(model_run_info_id);
      this.model_options[this.model_name.lda].model_id = model_run_info_id;
      // this.getModelTopics();
      // this.getTopicRanges();
    },
    sendSearch: function (page_num = 1) {
      console.log(page_num);
      console.log(this.selectedModel);
      // var model_option = this.model_options[this.selectedModel];

      this.loading = true;
      this.model_options[this.selectedModel].curr_page_num = page_num;
      var from = (page_num - 1) * this.size;

      if (
        from > this.model_options[this.selectedModel].total.value &&
        !this.next_override
      ) {
        return;
      }
      // this.model_options[this.selectedModel].hits = [];
      this.model_options[this.selectedModel].from_result = from;

      this.$http
        .post(this.apiUrl, this.apiParams)
        .then((response) => {
          this.model_options[this.selectedModel].hits = response.data.hits;
          this.model_options[this.selectedModel].total = response.data.total;
          this.model_options[this.selectedModel].next =
            this.model_options[this.selectedModel].curr_page_num + 1;
          this.model_options[this.selectedModel].num_pages = Math.floor(
            this.model_options[this.selectedModel].total.value / this.size
          );
          if (
            this.model_options[this.selectedModel].total.value % this.size >
            0
          ) {
            this.model_options[this.selectedModel].num_pages += 1;
          }
        })
        .finally(() => (this.loading = false));
    },
    fileUpload(event) {
      this.uploaded_file = event.target.files[0];
      this.url_cache = this.url;
      this.url = "";
    },
    removeFile() {
      this.uploaded_file = null;
      this.file_input = null;
      this.url = this.url_cache;
    },
    // updateUploadState() {
    //   if (this.selectedInput !== "file_upload") {
    //     this.removeFile();
    //     this.hasUploadedFile;
    //   }
    // },
  },

  watch: {
    selectedModel: function () {
      if (this.stateReady) {
        this.sendSearch(this.model_option.curr_page_num);
      }
    },
    // $data: {
    //   handler: function (val, oldVal) {
    //     console.log(val, oldVal);
    //   },
    //   deep: true,
    // },
    // "model_option.hits": function (val) {
    //   console.log(val);
    // },
    // "model_options.word2vec": function () {
    //   return;
    // },
    // "model_options.lda": function () {
    //   return;
    // },
  },
  // watch: {

  // selectedInput: function () {
  //   if (this.selectedInput !== "file_upload") {
  //     this.removeFile();
  //     // this.hasUploadedFile;
  //   }
  // },
  // },
};
</script>
<style scoped>
.file-input__label__similarity {
  /* border-right: 1px;
  border-right-color: rgb(206, 212, 218);
  border-right-style: solid; */
  border: 0px;
  border-top: 0px;
  border-bottom: 0px;
  /* margin-left: 10px; */
}
.wbg-uploaded-file__similarity {
  position: absolute; /*relative;*/
  max-width: 90%;
  /* margin-left: 10px; */
  max-height: 100%;
  margin-top: 1px;
}
</style>
