import Vue from 'vue'
import lodash from 'lodash'
import axios from 'axios'
import vSelect from "vue-select";

import Plotly from 'plotly.js'
import VueLodash from 'vue-lodash'
// import VueAxios from 'vue-axios'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import VueFriendlyIframe from 'vue-friendly-iframe'
import checkView from 'vue-check-view'

import router from './router'
import App from './App.vue'
import config from './config'

// CSS files
// import 'bootstrap/dist/css/bootstrap.css'
import "vue-select/dist/vue-select.css"
import 'vue-search-select/dist/VueSearchSelect.css'

Vue.config.productionTip = false
Vue.prototype.$http = axios
Vue.prototype.$Plotly = Plotly
Vue.prototype.$window = window
Vue.prototype.$config = config

// Set global Cache-Control request header for security.
Vue.prototype.$http.defaults.headers.common["Cache-Control"] = "max-age=0";

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(VueFriendlyIframe)
Vue.use(VueLodash, { lodash: lodash })
// Vue.use(VueAxios, axios)

Vue.use(checkView)
Vue.component("v-select", vSelect)

window.app = new Vue({
    router,
    render: h => h(App),
}).$mount('#app')

// (dev) vscode@82f481d7f9a2:/workspace/app/app_kcp$ npm run serve