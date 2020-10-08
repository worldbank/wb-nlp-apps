import Vue from 'vue'
import VueRouter from 'vue-router'
import ContentPanel from '../components/ContentPanel.vue'

Vue.use(VueRouter);

const routes = [
    {
        path: "/",
        name: "content",
        component: ContentPanel,
        props: { msg: "Introduction" },
    },
]

const router = new VueRouter({
    mode: 'history',
    routes
})

export default router