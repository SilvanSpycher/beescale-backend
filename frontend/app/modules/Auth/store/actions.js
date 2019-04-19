import {
    GET_USER_PROFILE,
    LOGIN,
    LOGOUT,
    REFRESH_TOKEN,
    REMOVE_TOKEN,
    REMOVE_USER,
    SET_USER,
    UPDATE_TOKEN
} from './types'
import authService from 'app/modules/Auth/service'
import { App } from 'app'

import JWTDecode from 'jwt-decode'

export default {
    [ LOGIN ]({ commit }, payload) {
        return authService.authenticate(payload).then(res => {
            commit(UPDATE_TOKEN, res.data.token)
        })
    },
    [ LOGOUT ]({ commit }) {
        commit(REMOVE_TOKEN)
        commit(REMOVE_USER)
    },
    [ REFRESH_TOKEN ]({ commit, state }) {
        const payload = { token: state.token }

        return authService.refreshToken(payload).then(res => {
            if (res && res.data) commit(UPDATE_TOKEN, res.data.token)
        })
    },
    [ GET_USER_PROFILE ]({ commit, state }, userId = JWTDecode(state.token).user_id) {
        // if (userId === null)
        //     userId = JWTDecode(state.token).user_id

        return authService.getProfile(userId).then(res => {
            if (res && res.data)
                commit(SET_USER, res.data)
            else
                App.notify.error('Error while loading user profile!')
        })
    }
}
