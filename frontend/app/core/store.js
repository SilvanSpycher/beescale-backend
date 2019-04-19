import Vue from 'vue'
import Vuex, { Store } from 'vuex'

import authModule from 'app/modules/Auth/store'

Vue.use(Vuex)

export default new Store({ modules: { auth: authModule } })
