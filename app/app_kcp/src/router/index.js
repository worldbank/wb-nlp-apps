import Vue from 'vue'
import VueRouter from 'vue-router'
import ExploreNav from '../components/ExploreNav.vue'
import Home from '../components/Home.vue'

import Introduction from '../components/pages/Introduction.vue'
import TopicComposition from '../components/pages/TopicComposition.vue'
import TopicProfiles from '../components/pages/TopicProfiles.vue'
import TopicRelationships from '../components/pages/TopicRelationships.vue'
// import EmbeddingViz from '../components/pages/EmbeddingViz.vue'
import WordEmbeddings from '../components/pages/WordEmbeddings.vue'
import Similarity from '../components/pages/Similarity.vue'


Vue.use(VueRouter);

const explore_routes = [{
        path: "",
        name: "home",
        component: Home,
        props: { page_title: "Home" },
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
        component: Introduction,
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
        children: explore_routes
    },
    {
        path: '/explore',
        component: ExploreNav,
        children: explore_routes
    },
]

// const routes = explore_routes

const router = new VueRouter({
    mode: 'history',
    routes
})

export default router