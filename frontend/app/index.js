import '@babel/polyfill'

// vendor
import Notifications from 'vue-notification'
import Vue from 'vue'
import VueRouter from 'vue-router'
import VeeValidate from 'vee-validate'
import Vuetify from 'vuetify'

// config
import { formExtras } from './core/mixins'
import router from './core/router'
import axios from './core/http'
import store from './core/store'

// layout
import BaseUI from './core/BaseUI'
import 'app/assets/styles/base.styl'


// own components
// load own global components here

Vue.use(VueRouter)
Vue.use(VeeValidate)
Vue.use(Vuetify, { theme: { primary: '#D62D22' } })
Vue.use(formExtras)
Vue.use(Notifications)
Vue.prototype.notify = (...args) => Vue.prototype.$notify(...args)
Vue.prototype.notify.warn = (text) => Vue.prototype.$notify({ text, type: 'warn' })
Vue.prototype.notify.error = (text) => Vue.prototype.$notify({ text, type: 'error', duration:-1 })
Vue.prototype.notify.success = (text) => Vue.prototype.$notify({ text, type: 'success' })


Vue.router = router
Vue.$http = axios

export const App = new Vue({
    router,
    store,
    el: '#app',
    render: h => h(BaseUI)
})
