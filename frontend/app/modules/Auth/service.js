import axios from 'axios'

export default {
    authenticate(payload) {
        return axios.post(`/token/auth/`, payload)
    },
    refreshToken(payload) {
        return axios.post(`/token/refresh/`, payload)
    },
    getProfile(id) {
        return axios.get(`/users/${ id }/`)
    }
}
