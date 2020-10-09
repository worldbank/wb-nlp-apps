import Vue from 'vue'
import lodash from 'lodash'
import axios from 'axios'

import VueLodash from 'vue-lodash'
// import VueAxios from 'vue-axios'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import VueFriendlyIframe from 'vue-friendly-iframe'

import router from './router'
import App from './App.vue'

// CSS files
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false
Vue.prototype.$http = axios

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(VueFriendlyIframe)
Vue.use(VueLodash, { lodash: lodash })
// Vue.use(VueAxios, axios)

window.app = new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
