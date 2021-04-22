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

          <select name="from" id="from" v-model="min_year" class="form-control">
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

          <select name="to" id="to" v-model="max_year" class="form-control">
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
              v-model="country"
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
              v-model="der_country_groups"
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
      <h6 v-b-toggle.major_doc_type-collapse>
        <i class="fa fa-filter pr-2"></i> Document type
      </h6>
      <b-collapse id="major_doc_type-collapse">
        <b-card class="facet-options">
          <b-form-group v-slot="{ ariaDescribedby }">
            <b-form-checkbox-group
              v-model="major_doc_type"
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
              v-model="adm_region"
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
              v-model="geo_region"
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
              v-model="topics_src"
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
              v-model="corpus"
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
              v-model="author"
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
      this.min_year = this.filters.min_year;
      this.max_year = this.filters.max_year;
      this.author = this.filters.author || [];

      this.country = this.filters.country || [];
      this.der_country_groups = this.filters.der_country_groups || [];

      this.corpus = this.filters.corpus || [];
      this.major_doc_type = this.filters.major_doc_type || [];
      this.adm_region = this.filters.adm_region || [];
      this.geo_region = this.filters.geo_region || [];
      this.topics_src = this.filters.topics_src || [];
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
    getFacetOptions(facet_name) {
      return this.facets["_filter_" + facet_name][facet_name].buckets.map(
        (o) => {
          return {
            text:
              this.processCountryGroupKey(facet_name, o["key"]) +
              "(" +
              o["doc_count"] +
              ")",
            value: o["key"],
          };
        }
      );
    },
  },
  data() {
    return {
      min_year: null,
      max_year: null,
      author: [],
      country: [],
      der_country_groups: [],
      corpus: [],
      major_doc_type: [],
      adm_region: [],
      geo_region: [],
      topics_src: [],
    };
  },
  watch: {
    $data: {
      deep: true,

      handler() {
        this.$emit("filterChanged", this.$data);
      },
    },
    filters: {
      deep: true,
      handler() {
        this.setSelectedFilters();
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