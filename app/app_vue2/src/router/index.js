import Vue from 'vue'
import VueRouter from 'vue-router'
import ExploreNav from '../components/ExploreNav.vue'

import ContentPanel from '../components/ContentPanel.vue'
import Introduction from '../components/pages/Introduction.vue'
import TopicComposition from '../components/pages/TopicComposition.vue'
import TopicProfiles from '../components/pages/TopicProfiles.vue'
import WordEmbeddings from '../components/pages/WordEmbeddings.vue'
import Similarity from '../components/pages/Similarity.vue'


Vue.use(VueRouter);

const explore_routes = [
    {
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
        component: ContentPanel,
        props: { page_title: "Corpus" },
    },
    {
        path: "topic-composition",
        name: "topic composition",
        component: TopicComposition,
        props: { page_title: "Topic Composition" },
    },
    {
        path: "topic-profiles",
        name: "topic profiles",
        component: TopicProfiles,
        props: { page_title: "Topic Profiles" },
    },
    {
        path: "topic-taxonomy",
        name: "topic taxonomy",
        component: ContentPanel,
        props: { page_title: "Topic Taxonomy" },
    },
    {
        path: "topic-relationships",
        name: "topic relationships",
        component: ContentPanel,
        props: { page_title: "Topic Relationships" },
    },
    {
        path: "word-embeddings",
        name: "word embeddings",
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
        name: "monitoring system",
        component: ContentPanel,
        props: { page_title: "Monitoring System" },
    },
]

const routes = [
    {
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