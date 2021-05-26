<template>
  <div class="container-wrapper">
    <Banner />
    <!-- <header class="blog-header wbg-internal-header">
      <div class="container">
        <div class="col-12 mb-2">
          <div id="breadcrumbs">
            <router-link to="/">Home</router-link>
            <span class="wbg-breadcrumb-separator">/</span>
            <router-link to="/search">Search</router-link>
          </div>
        </div>
        <div class="col-12">
          <i class="fas fa-search fa-2x" aria-hidden="true"></i>
          <h1>Search</h1>
          <p></p>
        </div>
      </div>
    </header> -->

    <div class="container flowing">
      <div class="row">
        <div class="col-12 col-md-12 mb-2">
          <div class="row justify-content-center">
            <div class="col-12 col-md-9 col-lg-8">
              <div
                class="input-group wbg-input-group mb-3 mt-3"
                style="display: flex"
              >
                <input
                  v-model="query"
                  type="text"
                  class="form-control wbg-search-text pl-4 input-height-auto"
                  :placeholder="uploaded_file ? '' : 'Enter your keywords...'"
                  aria-label="Field for search"
                  aria-describedby="basic-addon2"
                  v-on:keyup.enter="sendSearch()"
                />
                <div v-if="hasUploadedFile" class="wbg-uploaded-file">
                  <div class="truncated-title">
                    {{ this.uploaded_file.name }}
                  </div>
                  <i
                    class="fas fa-times fa-sm ml-2"
                    @click="removeFile"
                    aria-hidden="true"
                  ></i>
                </div>
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
                      name="file-input"
                      :value="file_input"
                      :disabled="hasUploadedFile"
                      id="file-input"
                      class="file-input__input"
                      data-toggle="tooltip"
                      data-placement="bottom"
                      title="Upload a PDF or TXT document to search"
                      accept=".txt,.doc,.docx,.pdf"
                    />
                    <i
                      title="Delete query"
                      v-show="(query && query.length > 0) || file_input"
                      @click="clearSearchInput"
                      style="
                        position: relative;
                        margin-left: -50px;
                        margin-right: 10px;
                        padding-right: 10px;
                        padding-left: 20px;
                        z-index: 999;
                      "
                      class="fas fa-times fa-sm"
                    />
                    <label class="file-input__label" for="file-input"
                      ><i
                        class="fas fa-file-upload fa-lg"
                        :style="hasUploadedFile ? 'color: gray' : ''"
                      ></i
                    ></label>
                  </div>
                </div>
                <div class="input-group-append">
                  <button
                    @click="sendSearch()"
                    class="btn btn-primary wbg-search-button pr-4 pl-4"
                    type="button"
                  >
                    Search
                  </button>
                </div>
              </div>
            </div>

            <div class="col-12 col-md-12 text-center">
              <span v-if="suggestions.length > 0" class="keyword-suggestions">
                <span class="suggestions">Suggestions:</span>
                <span
                  @click="searchSuggestion(word)"
                  v-for="word in suggestions"
                  :key="'suggest_' + word"
                  class="suggestion"
                  ><u>{{ word.replace(/_/g, " ") }}</u>
                </span>
                <br />
                <br />
              </span>
            </div>

            <p v-if="uploaded_file && uploaded_file.size > 2000000">
              <span style="color: red"
                >File size is large: ~{{
                  Math.round(uploaded_file.size / 1000000)
                }}
                MB. Results may take some time to render...</span
              >
            </p>

            <div class="col-12 col-md-12 text-center">
              <div class="form-check form-check-inline">
                <input
                  class="form-check-input"
                  type="radio"
                  name="inlineRadioOptions"
                  id="inlineRadio1"
                  value="keyword"
                  :checked="!uploaded_file"
                  v-model="search_type"
                  :disabled="uploaded_file"
                  @change="resetFrom"
                />
                <label class="form-check-label" for="inlineRadio1"
                  >Keyword search</label
                >
              </div>
              <div class="form-check form-check-inline">
                <input
                  class="form-check-input"
                  type="radio"
                  name="inlineRadioOptions"
                  id="inlineRadio2"
                  value="semantic"
                  v-model="search_type"
                  @change="resetFrom"
                />
                <label class="form-check-label" for="inlineRadio2"
                  >Semantic search</label
                >
              </div>
            </div>
            <div class="col-12 text-center mt-3">
              <small
                >You can also try
                <router-link to="explore/subcategories/filtering-by-topic-share"
                  >filtering by topic composition</router-link
                ></small
              >
            </div>
          </div>
          <hr />
        </div>
        <a id="results"></a>
        <aside class="col-sm-3" id="blog-sidebar-static">
          <!-- <SearchFilter
            v-if="facets"
            :filters="selected_facets"
            :facets="facets"
            @filterChanged="setFilters"
          /> -->

          <div>
            <div
              id="filter-by-access"
              class="sidebar-filter wb-ihsn-sidebar-filter filter-by-year filter-box"
            >
              <h6 class="togglable">
                <i class="fa fa-search pr-2"></i>Filter by Year
              </h6>
              <div class="sidebar-filter-entries">
                <input type="hidden" />

                <b-row>
                  <b-col cols="6"
                    ><span>From</span>
                    <select
                      name="from"
                      id="from"
                      v-model="selected_facets.min_year"
                      class="form-control"
                    >
                      <option
                        v-for="year_offset in curr_year - start_year"
                        :key="
                          'from-' +
                          ((selected_facets.max_year || curr_year + 1) -
                            year_offset)
                        "
                        :value="
                          (selected_facets.max_year || curr_year + 1) -
                          year_offset
                        "
                      >
                        {{
                          (selected_facets.max_year || curr_year + 1) -
                          year_offset
                        }}
                      </option>
                      <option :value="start_year" selected>
                        {{ start_year }}
                      </option>
                    </select></b-col
                  >
                  <b-col cols="6"
                    ><span>To</span>
                    <select
                      name="to"
                      id="to"
                      v-model="selected_facets.max_year"
                      class="form-control"
                    >
                      <option
                        v-for="year_offset in selected_facets.min_year
                          ? curr_year + 1 - selected_facets.min_year
                          : curr_year - start_year + 1"
                        :key="'to-' + (curr_year + 1 - year_offset)"
                        :value="curr_year + 1 - year_offset"
                      >
                        {{ curr_year + 1 - year_offset }}
                      </option>
                    </select>
                  </b-col>
                </b-row>
              </div>
            </div>

            <div class="sidebar-filter wb-ihsn-sidebar-filter filter-box">
              <h6 v-b-toggle.geo_region-collapse>
                <i class="fa fa-filter pr-2"></i> Geographic region
              </h6>
              <b-collapse id="geo_region-collapse">
                <b-card class="facet-options">
                  <b-form-group v-slot="{ ariaDescribedby }">
                    <b-form-checkbox-group
                      v-model="selected_facets.geo_region"
                      :options="getFacetOptions('geo_region')"
                      :aria-describedby="ariaDescribedby"
                      name="geo_region"
                      stacked
                    ></b-form-checkbox-group>
                  </b-form-group>
                </b-card>
              </b-collapse>
            </div>

            <div class="sidebar-filter wb-ihsn-sidebar-filter filter-box">
              <h6 v-b-toggle.country-collapse>
                <i class="fa fa-filter pr-2"></i> Country
              </h6>
              <b-collapse id="country-collapse">
                <b-card class="facet-options">
                  <b-form-group v-slot="{ ariaDescribedby }">
                    <b-form-checkbox-group
                      v-model="selected_facets.country"
                      :options="getFacetOptions('country')"
                      :aria-describedby="ariaDescribedby"
                      name="country"
                      stacked
                    ></b-form-checkbox-group>
                  </b-form-group>
                </b-card>
              </b-collapse>
            </div>

            <div class="sidebar-filter wb-ihsn-sidebar-filter filter-box">
              <h6 v-b-toggle.der_country_groups-collapse>
                <i class="fa fa-filter pr-2"></i> Country group
              </h6>
              <b-collapse id="der_country_groups-collapse">
                <b-card class="facet-options">
                  <b-form-group v-slot="{ ariaDescribedby }">
                    <b-form-checkbox-group
                      v-model="selected_facets.der_country_groups"
                      :options="getFacetOptions('der_country_groups')"
                      :aria-describedby="ariaDescribedby"
                      name="der_country_groups"
                      stacked
                    ></b-form-checkbox-group>
                  </b-form-group>
                </b-card>
              </b-collapse>
            </div>

            <div class="sidebar-filter wb-ihsn-sidebar-filter filter-box">
              <h6 v-b-toggle.der_jdc_tags-collapse>
                <i class="fa fa-filter pr-2"></i> JDC tags
              </h6>
              <b-collapse id="der_jdc_tags-collapse">
                <b-card class="facet-options">
                  <b-form-group v-slot="{ ariaDescribedby }">
                    <b-form-checkbox-group
                      v-model="selected_facets.der_jdc_tags"
                      :options="getFacetOptions('der_jdc_tags')"
                      :aria-describedby="ariaDescribedby"
                      name="der_jdc_tags"
                      stacked
                    ></b-form-checkbox-group>
                  </b-form-group>
                </b-card>
              </b-collapse>
            </div>

            <div class="sidebar-filter wb-ihsn-sidebar-filter filter-box">
              <h6 v-b-toggle.major_doc_type-collapse>
                <i class="fa fa-filter pr-2"></i> Document type
              </h6>
              <b-collapse id="major_doc_type-collapse">
                <b-card class="facet-options">
                  <b-form-group v-slot="{ ariaDescribedby }">
                    <b-form-checkbox-group
                      v-model="selected_facets.major_doc_type"
                      :options="getFacetOptions('major_doc_type')"
                      :aria-describedby="ariaDescribedby"
                      name="major_doc_type"
                      stacked
                    ></b-form-checkbox-group>
                  </b-form-group>
                </b-card>
              </b-collapse>
            </div>

            <div class="sidebar-filter wb-ihsn-sidebar-filter filter-box">
              <h6 v-b-toggle.corpus-collapse>
                <i class="fa fa-filter pr-2"></i> Source
              </h6>
              <b-collapse id="corpus-collapse">
                <b-card class="facet-options">
                  <b-form-group v-slot="{ ariaDescribedby }">
                    <b-form-checkbox-group
                      v-model="selected_facets.corpus"
                      :options="getFacetOptions('corpus')"
                      :aria-describedby="ariaDescribedby"
                      name="corpus"
                      stacked
                    ></b-form-checkbox-group>
                  </b-form-group>
                </b-card>
              </b-collapse>
            </div>
          </div>
        </aside>
        <div class="col-sm-9 blog-main">
          <article class="blog-post">
            <header></header>

            <div class="nada-pagination" v-show="hits.length > 0">
              <div
                class="row mt-3 mb-3 d-flex justify-content-lg-between align-items-center"
              >
                <div class="col-12 col-md-3 col-lg-4 mb-3 mb-md-0 small">
                  Showing <b>{{ start }}-{{ end }}</b> of
                  <b>{{ total.message }}</b> studies
                </div>
                <div
                  class="filter-action-bar d-flex col-12 col-md-9 col-lg-8 justify-content-lg-end"
                >
                  <a
                    title="Get API link"
                    v-b-modal.modal-lg
                    href="javascript:void(0);"
                    class="btn btn btn-outline-success btn-sm wbg-button ml-2"
                    ><i class="fab fa-searchengin"></i
                  ></a>
                  <b-modal id="modal-lg" size="lg" title="API link"
                    ><a :href="this.api_link" target="_blank"
                      ><span
                        style="font-family: 'Courier New', Courier, monospace"
                        >{{ api_link }}</span
                      ></a
                    >
                    <template #modal-footer>
                      <div v-if="navigator.clipboard" class="w-100">
                        <b-button
                          variant="primary"
                          size="sm"
                          class="float-right"
                          @click="copyText"
                        >
                          Copy to clipboard
                        </b-button>
                      </div>
                    </template>
                  </b-modal>
                </div>
              </div>
            </div>
            <div
              v-if="!isSelectedFacetsEmpty()"
              class="active-filters-container"
            >
              <div class="active-filters">
                <span
                  v-if="selected_facets.min_year && selected_facets.max_year"
                  class="badge badge-default wb-badge-close remove-filter years"
                  data-type="years"
                  data-value="0"
                  >between {{ selected_facets.min_year }}-{{
                    selected_facets.max_year
                  }}
                  <i @click="resetYears" class="fa fa-close"></i
                ></span>

                <span
                  v-if="
                    selected_facets.geo_region &&
                    selected_facets.geo_region.length > 0
                  "
                >
                  <span
                    v-for="fgeo_region in selected_facets.geo_region"
                    :key="'country-' + fgeo_region"
                    class="badge badge-default wb-badge-close remove-filter active-facets"
                    data-type="geo_region"
                    :data-value="fgeo_region"
                    >Geo region: {{ fgeo_region }}
                    <i
                      @click="resetGeoRegion(fgeo_region)"
                      class="fa fa-close"
                    ></i
                  ></span>
                </span>

                <span
                  v-if="
                    selected_facets.country &&
                    selected_facets.country.length > 0
                  "
                >
                  <span
                    v-for="fcountry in selected_facets.country"
                    :key="'country-' + fcountry"
                    class="badge badge-default wb-badge-close remove-filter active-facets"
                    data-type="country"
                    :data-value="fcountry"
                    >Country: {{ fcountry }}
                    <i @click="resetCountry(fcountry)" class="fa fa-close"></i
                  ></span>
                </span>

                <span
                  v-if="
                    selected_facets.der_country_groups &&
                    selected_facets.der_country_groups.length > 0
                  "
                >
                  <span
                    v-for="fder_country_groups in selected_facets.der_country_groups"
                    :key="'country-' + fder_country_groups"
                    class="badge badge-default wb-badge-close remove-filter active-facets"
                    data-type="der_country_groups"
                    :data-value="fder_country_groups"
                    >Country group: {{ fder_country_groups }}
                    <i
                      @click="resetDerCountryGroups(fder_country_groups)"
                      class="fa fa-close"
                    ></i
                  ></span>
                </span>

                <span
                  v-if="
                    selected_facets.der_jdc_tags &&
                    selected_facets.der_jdc_tags.length > 0
                  "
                >
                  <span
                    v-for="fder_jdc_tags in selected_facets.der_jdc_tags"
                    :key="'country-' + fder_jdc_tags"
                    class="badge badge-default wb-badge-close remove-filter active-facets"
                    data-type="der_jdc_tags"
                    :data-value="fder_jdc_tags"
                    >JDC tag: {{ fder_jdc_tags }}
                    <i
                      @click="resetDerJDCTags(fder_jdc_tags)"
                      class="fa fa-close"
                    ></i
                  ></span>
                </span>

                <span
                  v-if="
                    selected_facets.major_doc_type &&
                    selected_facets.major_doc_type.length > 0
                  "
                >
                  <span
                    v-for="fmajor_doc_type in selected_facets.major_doc_type"
                    :key="'country-' + fmajor_doc_type"
                    class="badge badge-default wb-badge-close remove-filter active-facets"
                    data-type="major_doc_type"
                    :data-value="fmajor_doc_type"
                    >Type: {{ fmajor_doc_type }}
                    <i
                      @click="resetMajorDocType(fmajor_doc_type)"
                      class="fa fa-close"
                    ></i
                  ></span>
                </span>

                <span
                  v-if="
                    selected_facets.corpus && selected_facets.corpus.length > 0
                  "
                >
                  <span
                    v-for="fcorpus in selected_facets.corpus"
                    :key="'country-' + fcorpus"
                    class="badge badge-default wb-badge-close remove-filter active-facets"
                    data-type="corpus"
                    :data-value="fcorpus"
                    >Source: {{ fcorpus }}
                    <i @click="resetCorpus(fcorpus)" class="fa fa-close"></i
                  ></span>
                </span>
                <div>
                  <a
                    @click="resetFilters"
                    href="javascript:void(0);"
                    class="btn-reset-search btn btn-outline-primary btn-sm"
                    >Reset filters</a
                  >
                </div>
              </div>
            </div>

            <SearchResultLoading
              :loading="loading && results_handler.length === 0"
              :size="curr_size"
            />
            <div v-if="results_handler.length > 0">
              <div v-for="idx in Array(curr_size).keys()" :key="'div-' + idx">
                <SearchResultCard
                  v-if="results_handler[idx]"
                  :result="results_handler[idx]"
                  :match="match_stats[idx]"
                  :highlights="highlights[idx]"
                  v-bind:key="'src' + idx"
                  :loading="loading"
                />
              </div>

              <!-- <SearchResultCard
                v-for="(result, idx, key) in hits"
                :result="result"
                :match="match_stats[idx]"
                :highlights="highlights[idx]"
                v-bind:key="result.id + key"
              /> -->
            </div>
            <Pagination
              @pageNumReceived="sendSearch"
              @currSizeSet="setCurrSize"
              :num_pages="num_pages"
              :curr_page_num="curr_page_num"
              :has_hits="hits.length > 0 && !no_more_hits"
              :page_sizes="page_sizes"
              :page_window="page_window"
              :next="next"
              :next_override="next_override"
            />
            <hr />
            <PageFooter :url="share_url" :share_text="share_text" />
          </article>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
// import qs from "qs";
import $ from "jquery";
import saveState from "vue-save-state";
import Banner from "./Banner";

import SearchResultCard from "./common/SearchResultCard";
import SearchResultLoading from "./common/SearchResultLoading";
import Pagination from "./common/Pagination";
import PageFooter from "./common/PageFooter";
window.onbeforeunload = function () {
  localStorage.clear();
};

export default {
  name: "Search",
  props: {
    share_url: String,
    share_text: String,
  },
  components: {
    SearchResultCard,
    SearchResultLoading,
    Pagination,
    PageFooter,
    Banner,
  },
  mixins: [saveState],
  mounted() {
    window.vm = this;
    // this.flowSideBar();

    this.routeChangeSearch();
  },
  computed: {
    hasUploadedFile() {
      if (this.uploaded_file !== null) {
        if (this.uploaded_file.name !== undefined) {
          return true;
        }
      }
      return false;
    },
    suggestionBody() {
      const body = {
        model_id: this.$config.default_model.word2vec.model_id,
        raw_text: this.query,
        topn_words: this.suggestion_count,
      };
      return body;
    },

    searchParams() {
      const params = new URLSearchParams();
      params.append("model_id", this.$config.default_model.word2vec.model_id);
      params.append("query", this.query);
      if (this.selected_facets.min_year) {
        params.append("min_year", this.selected_facets.min_year);
      }
      if (this.selected_facets.max_year) {
        params.append("max_year", this.selected_facets.max_year);
      }
      if (this.selected_facets.country) {
        this.selected_facets.country.map((v) => params.append("country", v));
      }
      if (this.selected_facets.der_country_groups) {
        this.selected_facets.der_country_groups.map((v) =>
          params.append("der_country_groups", v)
        );
      }
      if (this.selected_facets.der_jdc_tags) {
        this.selected_facets.der_jdc_tags.map((v) =>
          params.append("der_jdc_tags", v)
        );
      }

      if (this.selected_facets.corpus) {
        this.selected_facets.corpus.map((v) => params.append("corpus", v));
      }

      if (this.selected_facets.major_doc_type) {
        this.selected_facets.major_doc_type.map((v) =>
          params.append("major_doc_type", v)
        );
      }
      if (this.selected_facets.geo_region) {
        this.selected_facets.geo_region.map((v) =>
          params.append("geo_region", v)
        );
      }

      params.append("from_result", this.from_result);
      params.append("size", this.curr_size);
      return params;
    },
    fileParams() {
      const formData = new FormData();
      formData.append("model_id", this.$config.default_model.word2vec.model_id);
      formData.append("file", this.uploaded_file);
      formData.append("from_result", this.from_result);
      formData.append("size", this.curr_size);
      return formData;
    },
    no_more_hits() {
      var next_from = this.curr_page_num * this.curr_size;

      var no_more_hits = false;
      if (next_from > this.total.value) {
        no_more_hits = true;
      }

      return no_more_hits;
    },
  },
  data: function () {
    return {
      // min_year: null,
      // max_year: null,
      curr_year: new Date().getUTCFullYear(),
      start_year: 1890,

      navigator: window.navigator,
      search_type: "keyword",
      keyword_search_api_url: this.$config.search_url.keyword,
      semantic_search_api_url: this.$config.search_url.semantic,
      file_search_api_url: this.$config.search_url.file,
      suggestion_api_url:
        this.$config.nlp_api_url.word2vec + "/get_similar_words",
      page_sizes: this.$config.pagination.page_sizes,
      suggestions: [],
      suggestion_anchor: "",
      suggestion_count: 6,
      start: 0,
      end: 0,
      next: 0,
      page_window: this.$config.pagination.page_window,
      curr_page_num: 0,
      curr_size: this.$config.pagination.size,
      num_pages: 0,
      next_override: false,

      results_handler: [],

      query: "",
      from_result: 0,
      hits: [],
      highlights: [],

      facets: null,
      selected_facets: {},
      // country: [],
      // corpus: [],
      // major_doc_type: [],
      // geo_region: [],

      api_link: "",

      match_stats: [],
      total: Object,
      errored: false,
      loading: false,
      uploaded_file: null,
      file_input: null,
      query_cache: "",

      cache_count: this.$config.pagination.page_window,

      prevent_route_change_search: false,

      search_cache: {},
      from_cache: false,
      prevent_default: false,
    };
  },
  methods: {
    // SEARCH FILTER METHODS

    processCountryGroupKey(facet_name, key) {
      if (facet_name !== "der_country_groups") {
        return key;
      }

      if (key.includes("_")) {
        return key
          .split("_")
          .filter((x) => x.length > 0)
          .map((x) => x.charAt(0).toUpperCase() + x.slice(1))
          .join(" ");
      } else if (key.length > 8) {
        return key.charAt(0).toUpperCase() + key.slice(1);
      } else {
        return key.toUpperCase();
      }
    },
    processJDCTagsKey(facet_name, key) {
      if (facet_name !== "der_jdc_tags") {
        return key;
      }

      if (key.includes("_")) {
        return key
          .split("_")
          .filter((x) => x.length > 0)
          .join(" ");
      } else if (key === "unhcr") {
        return "UNHCR";
      } else {
        return key;
      }
    },
    processFacetKey(facet_name, key) {
      if (facet_name === "der_jdc_tags") {
        return this.processJDCTagsKey(facet_name, key);
      } else if (facet_name === "der_country_groups") {
        return this.processCountryGroupKey(facet_name, key);
      } else {
        return key;
      }
    },
    getFacetOptions(facet_name) {
      // const for_sorting = ["country", "der_country_groups", "geo_region"]
      var options = this.facets["_filter_" + facet_name][
        facet_name
      ].buckets.map((o) => {
        return {
          text:
            this.processFacetKey(facet_name, o["key"]) +
            " (" +
            o["doc_count"] +
            ")",
          value: o["key"],
        };
      });

      return options.sort((a, b) => a.text.localeCompare(b.text));
    },

    // SEARCH METHODS
    getNextSearchParams(from) {
      const sp = new URLSearchParams(this.searchParams.entries());
      sp.set("from_result", from);
      return sp;
    },
    resetYears() {
      this.selected_facets.min_year = null;
      this.selected_facets.max_year = null;
    },

    resetCountry(country) {
      this.selected_facets.country = this.selected_facets.country.filter(
        (o) => o !== country
      );
    },
    resetDerCountryGroups(der_country_groups) {
      this.selected_facets.der_country_groups = this.selected_facets.der_country_groups.filter(
        (o) => o !== der_country_groups
      );
    },
    resetDerJDCTags(der_jdc_tags) {
      this.selected_facets.der_jdc_tags = this.selected_facets.der_jdc_tags.filter(
        (o) => o !== der_jdc_tags
      );
    },
    resetMajorDocType(major_doc_type) {
      this.selected_facets.major_doc_type = this.selected_facets.major_doc_type.filter(
        (o) => o !== major_doc_type
      );
    },
    resetGeoRegion(geo_region) {
      this.selected_facets.geo_region = this.selected_facets.geo_region.filter(
        (o) => o !== geo_region
      );
    },
    resetCorpus(corpus) {
      this.selected_facets.corpus = this.selected_facets.corpus.filter(
        (o) => o !== corpus
      );
    },
    resetFilters() {
      var selected_facets = JSON.parse(JSON.stringify(this.selected_facets));
      Object.keys(selected_facets).forEach(
        (k) =>
          (selected_facets[k] =
            k === "min_year" || k === "max_year" ? null : [])
      );

      this.selected_facets = selected_facets;
    },
    isSelectedFacetsEmpty() {
      return Object.values(this.selected_facets).every(
        (value) => (value || []).length === 0
      );
    },
    keywordSearchBody() {
      const body = {};
      body["country"] = this.selected_facets.country;
      body["der_country_groups"] = this.selected_facets.der_country_groups;
      body["der_jdc_tags"] = this.selected_facets.der_jdc_tags;
      body["corpus"] = this.selected_facets.corpus;
      body["major_doc_type"] = this.selected_facets.major_doc_type;
      body["geo_region"] = this.selected_facets.geo_region;

      return body;
    },
    fileUpload(event) {
      this.uploaded_file = event.target.files[0];
      this.query_cache = this.query;
      this.query = "";
      this.search_type = "semantic";
      this.suggestion_anchor = "";
      this.suggestions = [];
    },
    clearSearchInput() {
      this.query_cache = "";
      this.removeFile();
    },
    removeFile() {
      this.uploaded_file = null;
      this.file_input = null;
      this.query = this.query_cache;
    },
    getSaveStateConfig() {
      return {
        cacheKey: "searchPage",
      };
    },
    resetFrom: function () {
      this.from_result = 0;
    },
    copyText() {
      this.navigator.clipboard.writeText(this.api_link);
    },
    getSuggestions: function () {
      if (!this.query) {
        return;
      }
      if (this.query === this.suggestion_anchor) {
        return;
      }
      this.suggestions = [];

      this.$http
        .post(this.suggestion_api_url, this.suggestionBody)
        .then((response) => {
          this.suggestions = response.data
            .map((o) => {
              if (
                o.score < 0.99 &&
                o.word.replaceAll("_", " ") !== this.query
              ) {
                return o.word;
              }
            })
            .filter((word) => word)
            .slice(0, this.suggestion_count - 1);
          this.suggestion_anchor = this.query;
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
        });
    },
    searchSuggestion: function (word) {
      this.query = word;
      this.sendSearch();
    },
    updateRoute() {
      return (
        this.$route.query.search_text !== this.query ||
        this.$route.query.search_type !== this.search_type
      );
    },
    sendSearch: function (page_num = 1) {
      this.prevent_route_change_search = true;
      this.prevent_default = false;
      this.curr_page_num = page_num;
      var from = (page_num - 1) * this.curr_size;

      this.hits = [];
      this.match_stats = [];
      this.highlights = [];
      this.next_override = true;

      if (this.search_type == "keyword") {
        this.next_override = false;
        this.getSuggestions();
        this.sendKeywordSearch(from);
      } else if (this.search_type == "semantic") {
        if (this.uploaded_file != null) {
          this.sendFileSearch(from);
        } else {
          this.getSuggestions();
          this.sendSemanticSearch(from);
        }
      } else {
        return;
      }

      if (this.updateRoute()) {
        this.$router.replace({
          name: "search",
          query: {
            search_text: this.query,
            search_type: this.search_type,
            // page: this.curr_page_num,
          },
        });
      }
    },
    sendKeywordSearch: function (from = 0, ignore_empty_query = false) {
      if (!this.query) {
        if (!ignore_empty_query) {
          return;
        }
      }
      if (from > this.total.value) {
        return;
      }
      this.query = this.query.replaceAll("_", " ");

      this.getCachedOrFetchData(from, false, false);
    },
    sendSemanticSearch: function (from = 0) {
      this.facets = null;
      this.selected_facets = {};
      if (!this.query) {
        return;
      }
      // if (from > this.total.value) {
      //   return;
      // }

      this.getCachedOrFetchData(from, false, false);
    },
    sendFileSearch: function (from = 0) {
      this.from_result = from;
      this.loading = true;

      this.$http
        .post(this.file_search_api_url, this.fileParams)
        .then((response) => {
          this.hits = response.data.hits;
          this.match_stats = response.data.result;
          this.total = response.data.total;
          this.next = this.curr_page_num + 1;
          this.start = this.from_result + 1;
          this.end = this.from_result + this.hits.length;
          this.num_pages = Math.floor(this.total.value / this.curr_size);
          if (this.total.value % this.curr_size > 0) {
            this.num_pages += 1;
          }

          const is_first = this.results_handler.length === 0;

          for (var i = 0; i < this.curr_size; i++) {
            if (is_first) {
              this.results_handler.push(this.hits[i]);
            } else {
              this.results_handler[i] = this.hits[i];
            }
          }
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
          this.loading = false;
        })
        .finally(() => (this.loading = false));
    },
    setCurrSize: function (size) {
      this.curr_size = size;
      this.sendSearch();
    },
    flowSideBar: function () {
      $(function () {
        var $sidebar = $("#blog-sidebar"),
          $window = $(window),
          offset = $sidebar.offset(),
          topPadding = 15;

        $window.scroll(function () {
          if (($window.scrollTop() > offset.top) & ($(window).width() > 768)) {
            $sidebar.stop().animate(
              {
                marginTop: $window.scrollTop() - offset.top + topPadding,
              },
              { easing: "ease", duration: 0 }
            );
          } else {
            $sidebar.stop().animate({
              marginTop: 0,
            });
          }
        });
      });
    },
    routeChangeSearch() {
      if (this.prevent_route_change_search) {
        return;
      }
      if (!this.loading && !this.prevent_default) {
        if (this.$route.query.search_type !== undefined) {
          this.search_type = this.$route.query.search_type;

          if (this.$route.query.search_text !== undefined) {
            this.query = this.$route.query.search_text;

            var page_num = 1;
            if (this.$route.query.page !== undefined) {
              page_num = Number(this.$route.query.page);
            }

            if (this.$route.params.uploaded_file) {
              this.uploaded_file = this.$route.params.uploaded_file;
            }
            this.sendSearch(page_num);
          }
        } else {
          this.defaultKeywordSearch();
        }
      }
    },
    getCachedOrFetchData: function (
      from = 0,
      ignore_empty_query = false,
      for_cache = false
    ) {
      // :from is in the unit of actual result count

      var search_cache_key = null;

      let searchParams = null;
      let params = null;
      const is_keyword_search = this.search_type === "keyword";

      const api_url = is_keyword_search
        ? this.keyword_search_api_url
        : this.semantic_search_api_url;

      if (!for_cache) {
        this.from_result = from;
        this.loading = true;

        searchParams = this.searchParams;
        params = { params: searchParams };

        search_cache_key =
          this.search_type + "::" + searchParams.toLocaleString();
        const cached = this.search_cache[search_cache_key];
        console.log(cached);

        if (cached) {
          this.prevent_default = true;
          this.from_cache = true;

          this.hits = cached.hits;
          this.match_stats = cached.result;
          this.total = cached.total;

          if (is_keyword_search) {
            this.highlights = cached.highlights;
            this.facets = cached.facets;
            // this.selected_facets = cached.filters;
          }

          this.next = this.curr_page_num + 1;
          this.start = this.from_result + 1;
          this.end = this.from_result + this.hits.length;
          this.num_pages = Math.floor(this.total.value / this.curr_size);
          if (this.total.value % this.curr_size > 0) {
            this.num_pages += 1;
          }

          const is_first = this.results_handler.length === 0;

          for (var i = 0; i < this.curr_size; i++) {
            if (is_first) {
              this.results_handler.push(this.hits[i]);
            } else {
              this.results_handler[i] = this.hits[i];
            }
          }

          this.api_link =
            location.origin + api_url + "?" + searchParams.toLocaleString();

          let vm = this;
          setTimeout(() => {
            vm.loading = false;
          }, 10);
          // this.loading = false;

          this.fetchForCache(this.next, ignore_empty_query, this.cache_count);

          return;
        }
        this.from_cache = false;
      } else {
        searchParams = this.getNextSearchParams(from);
        params = { params: searchParams };

        search_cache_key =
          this.search_type + "::" + searchParams.toLocaleString();
        const cached = this.search_cache[search_cache_key];

        if (cached) {
          return;
        }
      }

      this.$http
        .get(api_url, params)
        .then((response) => {
          if (!for_cache) {
            this.hits = response.data.hits;
            this.match_stats = response.data.result;
            this.total = response.data.total;

            if (is_keyword_search) {
              this.highlights = response.data.highlights;
              this.facets = response.data.facets;
              // this.selected_facets = response.data.filters;
            }

            this.search_cache[search_cache_key] = {
              key: search_cache_key,
              hits: response.data.hits,
              result: response.data.result,
              total: response.data.total,
            };

            if (is_keyword_search) {
              this.search_cache[search_cache_key].highlights =
                response.data.highlights;
              this.search_cache[search_cache_key].facets = response.data.facets;
              this.search_cache[search_cache_key].filters =
                response.data.filters;
            }

            this.next = this.curr_page_num + 1;
            this.start = this.from_result + 1;
            this.end = this.from_result + this.hits.length;

            this.num_pages = Math.floor(this.total.value / this.curr_size);
            if (this.total.value % this.curr_size > 0) {
              this.num_pages += 1;
            }

            const is_first = this.results_handler.length === 0;

            for (var i = 0; i < this.curr_size; i++) {
              if (is_first) {
                this.results_handler.push(this.hits[i]);
              } else {
                this.results_handler[i] = this.hits[i];
              }
            }

            this.api_link =
              location.origin + api_url + "?" + searchParams.toLocaleString();

            this.loading = false;

            this.fetchForCache(this.next, ignore_empty_query, this.cache_count);

            // this.getCachedOrFetchData(
            //   (this.next - 1) * this.curr_size,
            //   ignore_empty_query,
            //   true
            // );
          } else {
            this.search_cache[search_cache_key] = {
              key: search_cache_key,
              hits: response.data.hits,
              result: response.data.result,
              total: response.data.total,
            };

            if (is_keyword_search) {
              this.search_cache[search_cache_key].highlights =
                response.data.highlights;
              this.search_cache[search_cache_key].facets = response.data.facets;
              this.search_cache[search_cache_key].filters =
                response.data.filters;
            }
          }
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
          this.loading = false;
        })
        .finally(() => (this.loading = false));
    },
    fetchForCache(next, ignore_empty_query, cache_count = 1) {
      for (var i = next; i < next + cache_count; i++) {
        this.getCachedOrFetchData(
          (i - 1) * this.curr_size,
          ignore_empty_query,
          true
        );
      }
    },
    defaultKeywordSearch() {
      if (!this.loading && !this.prevent_default) {
        this.sendKeywordSearch(0, true);
      }
    },
  },
  watch: {
    search_type: function () {
      this.sendSearch();
    },

    selected_facets: {
      deep: true,
      handler() {
        this.prevent_default = false;
        this.defaultKeywordSearch();
      },
    },
    $route() {
      this.routeChangeSearch();
      window.location.hash = "#results";
    },
  },
};

// allowDefaultSearch
//
</script>

<style scoped>
@import "../../node_modules/bootstrap-vue/dist/bootstrap-vue.css";

u {
  border-bottom: 1px dotted;
  text-decoration: none;
}

.content-row {
  min-height: 50vh;
}
/* @media (min-width: 1200px) {
  .flowing {
    max-width: 1200px;
  }
} */

.wbg-internal-header {
  padding-top: 1rem;
  padding-bottom: 1rem;
}

/*
.blog-main {
  margin: 0;
  padding-left: 1rem;
}

.blog-sidebar {
  margin-left: -2rem;
  padding: 0;
} */

.truncated-title {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1; /* number of lines to show */
  -webkit-box-orient: vertical;
}
.active-filters-container {
  margin: 20px 0 30px;
  border-radius: 3px;
  position: relative;
}
.active-filters-container .active-filters {
  background: #f3f3f3;
  overflow: auto;
  color: white;
  clear: both;
  padding: 10px;
}
.active-filters-container .active-filters .years {
  background-color: #787878;
}

.active-filters-container .active-filters .active-facets {
  background-color: #787878;
}

.active-filters-container .wb-badge-close {
  padding: 10px 10px;
  margin: 2px 4px 2px 0;
  position: relative;
  padding-right: 10px;
  cursor: pointer;
  transition: opacity 0.35s;
}
.btn-outline-primary {
  color: #0071bc;
}
.keyword-suggestions {
  width: 100%;
  margin-left: 15px;
  padding: 5px;
  padding-bottom: 25px;
}
.suggestions {
  margin-right: 10px;
}
.suggestion {
  color: #0062cc;
  margin-right: 10px;
  cursor: pointer;
}
.fa-times:hover {
  color: red;
}

/* .tab-link-format {
  margin: 8px;
  background-color: transparent !important;
  padding-top: 5px !important;
  border: 0px !important;
} */

.nav-link {
  margin-top: 0px !important;
  margin: 10px;
  background-color: transparent !important;
  border: 0px !important;
  padding: 0px;
}

/* .container-wrapper {
  margin-top: 20px;
} */

.fa-no-margin {
  margin: 0px;
}

.input-height-auto {
  height: auto;
}
</style>