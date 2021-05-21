<template>
  <div>
    <div
      id="filter-by-access"
      class="sidebar-filter wb-ihsn-sidebar-filter filter-by-year filter-box"
    >
      <h6 class="togglable">
        <i class="fa fa-search pr-2"></i>Filter by Year
        <!-- {{ min_year }} - {{ max_year }} -->
      </h6>
      <div class="sidebar-filter-entries">
        <input type="hidden" />
        <!-- <p class="mt-3 mb-2">Show studies conducted between</p> -->
        <div class="form-group">
          <p class="mt-3 mb-2">from</p>

          <select
            name="from"
            id="from"
            v-model="search_filters.min_year"
            class="form-control"
          >
            <option
              v-for="year_offset in 131"
              :key="'from-' + (2022 - year_offset)"
              :value="2022 - year_offset"
            >
              {{ 2022 - year_offset }}
            </option>
            <option value="1890" selected>1890</option>
          </select>
        </div>
        <!-- <p class="mt-3 mb-2">and</p> -->
        <div class="form-group">
          <p class="mt-3 mb-2">to</p>

          <select
            name="to"
            id="to"
            v-model="search_filters.max_year"
            class="form-control"
          >
            <option
              v-for="year_offset in 132"
              :key="'to-' + (2022 - year_offset)"
              :value="2022 - year_offset"
            >
              {{ 2022 - year_offset }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <div class="sidebar-filter wb-ihsn-sidebar-filter filter-box">
      <h6 v-b-toggle.country-collapse>
        <i class="fa fa-filter pr-2"></i> Country
      </h6>
      <b-collapse id="country-collapse">
        <b-card class="facet-options">
          <b-form-group v-slot="{ ariaDescribedby }">
            <b-form-checkbox-group
              v-model="search_filters.country"
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
              v-model="search_filters.der_country_groups"
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
              v-model="search_filters.der_jdc_tags"
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
              v-model="search_filters.major_doc_type"
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
      <h6 v-b-toggle.adm_region-collapse>
        <i class="fa fa-filter pr-2"></i> Admin region
      </h6>
      <b-collapse id="adm_region-collapse">
        <b-card class="facet-options">
          <b-form-group v-slot="{ ariaDescribedby }">
            <b-form-checkbox-group
              v-model="search_filters.adm_region"
              :options="getFacetOptions('adm_region')"
              :aria-describedby="ariaDescribedby"
              name="adm_region"
              stacked
            ></b-form-checkbox-group>
          </b-form-group>
        </b-card>
      </b-collapse>
    </div>

    <div class="sidebar-filter wb-ihsn-sidebar-filter filter-box">
      <h6 v-b-toggle.geo_region-collapse>
        <i class="fa fa-filter pr-2"></i> Geographic region
      </h6>
      <b-collapse id="geo_region-collapse">
        <b-card class="facet-options">
          <b-form-group v-slot="{ ariaDescribedby }">
            <b-form-checkbox-group
              v-model="search_filters.geo_region"
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
      <h6 v-b-toggle.topics_src-collapse>
        <i class="fa fa-filter pr-2"></i> Topics
      </h6>
      <b-collapse id="topics_src-collapse">
        <b-card class="facet-options">
          <b-form-group v-slot="{ ariaDescribedby }">
            <b-form-checkbox-group
              v-model="search_filters.topics_src"
              :options="getFacetOptions('topics_src')"
              :aria-describedby="ariaDescribedby"
              name="topics_src"
              stacked
            ></b-form-checkbox-group>
          </b-form-group>
        </b-card>
      </b-collapse>
    </div>

    <div class="sidebar-filter wb-ihsn-sidebar-filter filter-box">
      <h6 v-b-toggle.corpus-collapse>
        <i class="fa fa-filter pr-2"></i> Corpus
      </h6>
      <b-collapse id="corpus-collapse">
        <b-card class="facet-options">
          <b-form-group v-slot="{ ariaDescribedby }">
            <b-form-checkbox-group
              v-model="search_filters.corpus"
              :options="getFacetOptions('corpus')"
              :aria-describedby="ariaDescribedby"
              name="corpus"
              stacked
            ></b-form-checkbox-group>
          </b-form-group>
        </b-card>
      </b-collapse>
    </div>

    <div class="sidebar-filter wb-ihsn-sidebar-filter filter-box">
      <h6 v-b-toggle.author-collapse>
        <i class="fa fa-filter pr-2"></i> Author
      </h6>
      <b-collapse id="author-collapse">
        <b-card class="facet-options">
          <b-form-group v-slot="{ ariaDescribedby }">
            <b-form-checkbox-group
              v-model="search_filters.author"
              :options="getFacetOptions('author')"
              :aria-describedby="ariaDescribedby"
              name="author"
              stacked
            ></b-form-checkbox-group>
          </b-form-group>
        </b-card>
      </b-collapse>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchFilter",
  props: {
    filters: {
      type: Object,
      default: function () {
        return {};
      },
    },
    facets: {
      type: Object,
      default: function () {
        return {};
      },
    },
  },
  mounted() {
    window.sf = this;
  },
  methods: {
    setSelectedFilters() {
      this.search_filters = this.filters;

      console.log("setSelectedFilters");
    },
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
      // const for_sorting = ["country", "der_country_groups", "adm_region", "geo_region"]
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
  },
  data() {
    return {
      search_filters: {
        min_year: null,
        max_year: null,
        author: [],
        country: [],
        der_country_groups: [],
        der_jdc_tags: [],
        corpus: [],
        major_doc_type: [],
        adm_region: [],
        geo_region: [],
        topics_src: [],
      },
      update_from_search: false,
      event_queued: false,
    };
  },
  watch: {
    search_filters: {
      deep: true,
      handler() {
        if (this.update_from_search) {
          return;
        }
        console.log("sendingFilterChanged from search_filters...");

        let vm = this;
        vm.$emit("filterChanged", vm.search_filters);

        // if (!this.event_queued) {
        //   setTimeout(() => {
        //     vm.$emit("filterChanged", vm.search_filters);
        //     vm.event_queued = false;
        //   }, 50);

        //   this.event_queued = true;
        // }
      },
    },
    filters: {
      deep: true,
      handler() {
        this.update_from_search = true;
        this.setSelectedFilters();
        setTimeout(() => {
          this.update_from_search = false;
        }, 10);
      },
    },
  },
};
</script>
<style>
.facet-options {
  max-height: 400px;
  overflow-y: scroll;
}
</style>