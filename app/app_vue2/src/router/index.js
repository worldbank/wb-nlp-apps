import Vue from 'vue'
import VueRouter from 'vue-router'
import ContentPanel from '../components/ContentPanel.vue'

Vue.use(VueRouter);

const routes = [
    {
        path: "/introduction",
        name: "introduction",
        component: ContentPanel,
        props: { msg: "Introduction" },
    },
    {
        path: "/corpus",
        name: "corpus",
        component: ContentPanel,
        props: { msg: "Corpus" },
    },
    {
        path: "/topic composition",
        name: "topic composition",
        component: ContentPanel,
        props: { msg: "Topic Composition" },
    },
]

const router = new VueRouter({
    mode: 'history',
    routes
})

export default router