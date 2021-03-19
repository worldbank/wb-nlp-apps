import Vue from 'vue'
import VueRouter from 'vue-router'
import ExploreNav from '../components/ExploreNav.vue'
import Home from '../components/Home.vue'
import Search from '../components/Search.vue'
import Explore from '../components/Explore.vue'
import Methods from '../components/Methods.vue'
import API from '../components/API.vue'
import About from '../components/About.vue'


// EXPLORE components
import Introduction from '../components/explore/Introduction.vue'
import Corpus from '../components/explore/Corpus.vue'
import TopicComposition from '../components/explore/TopicComposition.vue'
import TopicProfiles from '../components/explore/TopicProfiles.vue'
import TopicRelationships from '../components/explore/TopicRelationships.vue'
// import EmbeddingViz from '../components/explore/EmbeddingViz.vue'
// import WordEmbeddings from '../components/explore/WordEmbeddings.vue'
import WordEmbeddings from '../components/explore/WordEmbeddingsGraph.vue'

// import Similarity from '../components/explore/Similarity.vue'
import Similarity from '../components/explore/SimilarityNew.vue'

// EXPLORE SUBCATEGORIES components
import Sources from '../components/explore/subcategories/Sources.vue'
import GeographicCoverage from '../components/explore/subcategories/GeographicCoverage.vue'
import Metadata from '../components/explore/subcategories/Metadata.vue'
import TrainingSubset from '../components/explore/subcategories/TrainingSubset.vue'
import TopicBrowser from '../components/explore/subcategories/TopicBrowser.vue'
import FilterTopicShare from '../components/explore/subcategories/FilterTopicShare.vue'



// METHODS components
import MethodsMethods from '../components/methods/Methods.vue'
import TextAcquisition from '../components/methods/TextAcquisition.vue'
import TextPreparation from '../components/methods/TextPreparation.vue'
import LDATopicModel from '../components/methods/LDATopicModel.vue'
import MethodsWordEmbeddings from '../components/methods/WordEmbeddings.vue'
import TopicClassification from '../components/methods/TopicClassification.vue'
import Cataloguing from '../components/methods/Cataloguing.vue'
import SearchEngine from '../components/methods/SearchEngine.vue'
import Visualizations from '../components/methods/Visualizations.vue'
import DocumentPage from '../components/common/DocumentPage.vue'



Vue.use(VueRouter);

const main_routes = [{
        path: "",
        name: "home",
        component: Home,
        props: { page_title: "Home" },
    },
    {
        path: "search",
        name: "search",
        component: Search,
        props: {
            page_title: "Search",
            share_url: "%2fsearch%2f",
            share_text: "Search"
        },
    },
    {
        path: "content-api",
        name: "content-api",
        component: API,
        props: { page_title: "API" },
    },
    {
        path: "about",
        name: "about",
        component: About,
        props: { page_title: "About" },
    },
]


const explore_subcategories_routes = [
    // CORPUS
    {
        path: "sources-and-volume",
        name: "explore_sources-and-volume",
        component: Sources,
        props: { page_title: "Sources and volume" },
    },
    {
        path: "geographic-coverage",
        name: "explore_geographic-coverage",
        component: GeographicCoverage,
        props: { page_title: "Geographic Coverage" },
    },
    {
        path: "metadata",
        name: "explore_metadata",
        component: Metadata,
        props: { page_title: "Metadata" },
    },
    {
        path: "training-subset",
        name: "explore_training-subset",
        component: TrainingSubset,
        props: { page_title: "Training Subset" },
    },

    // TOPIC COMPOSITION
    {
        path: "topic-browser",
        name: "explore_topic-browser",
        component: TopicBrowser,
        props: { page_title: "Topic Browser" },
    },
    {
        path: "filtering-by-topic-share",
        name: "explore_filtering-by-topic-share",
        component: FilterTopicShare,
        props: {
            page_title: "Filtering by Topic Share",
            share_url: "%2fexplore%2fsubcategories%2ffiltering_by_topic_share%2f",
            share_text: "Filtering%20by%20topic%20share"
        }
    },

    // KNOWLEDGE PAGE SERVICE
    {
        path: "example",
        name: "explore_example",
        component: GeographicCoverage,
        props: { page_title: "Example" },
    },
    {
        path: "instructions",
        name: "explore_instructions",
        component: GeographicCoverage,
        props: { page_title: "Instructions" },
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
        props: { page_title: "Topic Profiles", show_topic_words: false },
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
        props: {
            page_title: "Similarity",
            share_url: "%2fexplore%2fsimilarity%2f",
            share_text: "Similarity"
        },
    },
    {
        path: "knowledge-page-service",
        name: "explore_knowledge-page-service",
        component: Introduction,
        props: { page_title: "Knowledge Page Service" },
    },
]


const methods_routes = [{
        path: "",
        name: "methods",
        component: MethodsMethods,
        props: { page_title: "Methods & Tools" },
    },
    {
        path: "text-acquisition",
        name: "methods_text-acquisition",
        component: TextAcquisition,
        props: { page_title: "Text Acquisition" },
    },
    {
        path: "text-preparation",
        name: "methods_text-preparation",
        component: TextPreparation,
        props: { page_title: "Text Preparation" },
    },
    {
        path: "lda",
        name: "methods_lda",
        component: LDATopicModel,
        props: { page_title: "LDA Topic Model" },
    },
    {
        path: "word-embeddings",
        name: "methods_word-embeddings",
        component: MethodsWordEmbeddings,
        props: { page_title: "Word Embeddings" },
    },
    {
        path: "topic-classification",
        name: "methods_topic-classification",
        component: TopicClassification,
        props: { page_title: "Topic Classification" },
    },
    {
        path: "cataloguing",
        name: "methods_cataloguing",
        component: Cataloguing,
        props: { page_title: "Cataloguing" },
    },
    {
        path: "search-engine",
        name: "methods_search-engine",
        component: SearchEngine,
        props: { page_title: "Search Engine" },
    },
    {
        path: "visualizations",
        name: "methods_visualizations",
        component: Visualizations,
        props: { page_title: "Visualizations" },
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
    {
        path: '/methods',
        component: Methods,
        children: methods_routes
    },
    {
        path: "/document/:doc_id",
        name: "document",
        component: DocumentPage,
    },
]

// const routes = explore_routes

const router = new VueRouter({
    mode: 'history',
    routes: routes,
    // scrollBehavior(to, from, savedPosition) {
    scrollBehavior() {
        // var to = to
        // var from = from
        // var savedPosition = savedPosition
        return { x: 0, y: 0, behavior: 'smooth' };

        // console.log(to);
        // if (to.hash) {
        //     return {
        //         selector: to.hash,
        //         behavior: 'smooth',
        //     }
        // }
    }
})

export default router