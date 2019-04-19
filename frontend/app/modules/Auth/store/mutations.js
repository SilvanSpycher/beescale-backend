import { REMOVE_TOKEN, REMOVE_USER, SET_USER, UPDATE_TOKEN } from './types'

export default {
    [ SET_USER ](state, user) {
        state.user = user
    },

    [ REMOVE_USER ](state) {
        state.user = {}
    },

    [ UPDATE_TOKEN ](state, token) {
        localStorage.setItem('t', token)
        state.token = token
    },

    [ REMOVE_TOKEN ](state) {
        localStorage.removeItem('t')
        state.token = null
    }
}
