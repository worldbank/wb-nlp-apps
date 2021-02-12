import Vue from 'vue'
import VueRouter from 'vue-router'
import ExploreNav from '../components/ExploreNav.vue'
import Home from '../components/Home.vue'
import Explore from '../components/Explore.vue'


// EXPLORE components
import Introduction from '../components/explore/Introduction.vue'
import Corpus from '../components/explore/Corpus.vue'
import TopicComposition from '../components/explore/TopicComposition.vue'
import TopicProfiles from '../components/explore/TopicProfiles.vue'
import TopicRelationships from '../components/explore/TopicRelationships.vue'
// import EmbeddingViz from '../components/explore/EmbeddingViz.vue'
import WordEmbeddings from '../components/explore/WordEmbeddings.vue'
import Similarity from '../components/explore/Similarity.vue'

// EXPLORE SUBCATEGORIES components
import Sources from '../components/explore/subcategories/Sources.vue'
import GeographicCoverage from '../components/explore/subcategories/GeographicCoverage.vue'


Vue.use(VueRouter);

const main_routes = [{
    path: "",
    name: "home",
    component: Home,
    props: { page_title: "Home" },
}, ]

const explore_subcategories_routes = [{
        path: "sources",
        name: "sources",
        component: Sources,
        props: { page_title: "Sources" },
    },
    {
        path: "geographic-coverage",
        name: "geographic-coverage",
        component: GeographicCoverage,
        props: { page_title: "Geographic Coverage" },
    },
]

const explore_routes = [{
        path: "",
        name: "explore",
        component: Introduction,
        props: { page_title: "Explore" },
    },
    {
        path: "introduction",
        name: "introduction",
        component: Introduction,
        props: { page_title: "Introduction" },
    },
    {
        path: "corpus",
        name: "corpus",
        component: Corpus,
        props: { page_title: "Corpus" },
    },
    {
        path: "topic-composition",
        name: "topic-composition",
        component: TopicComposition,
        props: { page_title: "Topic Composition" },
    },
    {
        path: "topic-profiles",
        name: "topic-profiles",
        component: TopicProfiles,
        props: { page_title: "Topic Profiles" },
    },
    {
        path: "topic-taxonomy",
        name: "topic-taxonomy",
        component: Introduction,
        props: { page_title: "Topic Taxonomy" },
    },
    {
        path: "topic-relationships",
        name: "topic-relationships",
        component: TopicRelationships,
        props: { page_title: "Topic Relationships" },
    },
    // {
    //     path: "embedding-viz",
    //     name: "embedding viz",
    //     component: EmbeddingViz,
    //     props: { page_title: "Embedding Viz Animation" },
    // },
    {
        path: "word-embeddings",
        name: "word-embeddings",
        component: WordEmbeddings,
        props: { page_title: "Word Embeddings" },
    },
    {
        path: "similarity",
        name: "similarity",
        component: Similarity,
        props: { page_title: "Similarity" },
    },
    {
        path: "monitoring-system",
        name: "monitoring-system",
        component: Introduction,
        props: { page_title: "Monitoring System" },
    },
]

const routes = [{
        path: '',
        component: ExploreNav,
        children: main_routes
    },
    {
        path: '/explore',
        component: Explore,
        children: explore_routes
    },
    {
        path: '/explore/subcategories',
        component: Explore,
        children: explore_subcategories_routes
    },
]

// const routes = explore_routes

const router = new VueRouter({
    mode: 'history',
    routes
})

export default router