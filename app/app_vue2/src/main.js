import Vue from 'vue'
import VueLodash from 'vue-lodash'
import lodash from 'lodash'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import router from './router'
import App from './App.vue'

// CSS files
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)


// Install VueLodash
Vue.use(VueLodash, { lodash: lodash })

window.app = new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
