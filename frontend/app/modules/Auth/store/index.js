import mutations from './mutations'
import actions from './actions'
import getters from './getters'

export default {
    state: {
        user: {},
        token: localStorage.getItem('t')
    },
    mutations,
    actions,
    getters
}
