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
        name: "explore_sources",
        component: Sources,
        props: { page_title: "Sources" },
    },
    {
        path: "geographic-coverage",
        name: "explore_geographic-coverage",
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
        name: "explore_introduction",
        component: Introduction,
        props: { page_title: "Introduction" },
    },
    {
        path: "corpus",
        name: "explore_corpus",
        component: Corpus,
        props: { page_title: "Corpus" },
    },
    {
        path: "topic-composition",
        name: "explore_topic-composition",
        component: TopicComposition,
        props: { page_title: "Topic Composition" },
    },
    {
        path: "topic-profiles",
        name: "explore_topic-profiles",
        component: TopicProfiles,
        props: { page_title: "Topic Profiles" },
    },
    {
        path: "topic-taxonomy",
        name: "explore_topic-taxonomy",
        component: Introduction,
        props: { page_title: "Topic Taxonomy" },
    },
    {
        path: "topic-relationships",
        name: "explore_topic-relationships",
        component: TopicRelationships,
        props: { page_title: "Topic Relationships" },
    },
    // {
    //     path: "embedding-viz",
    //     name: "explore_embedding viz",
    //     component: EmbeddingViz,
    //     props: { page_title: "Embedding Viz Animation" },
    // },
    {
        path: "word-embeddings",
        name: "explore_word-embeddings",
        component: WordEmbeddings,
        props: { page_title: "Word Embeddings" },
    },
    {
        path: "similarity",
        name: "explore_similarity",
        component: Similarity,
        props: { page_title: "Similarity" },
    },
    {
        path: "monitoring-system",
        name: "explore_monitoring-system",
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
    routes: routes
})

export default router