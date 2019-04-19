import { App } from 'app'
import Axios from 'axios'
import store from 'app/core/store'

import { LOGOUT } from 'app/modules/Auth/store/types'

Axios.defaults.baseURL = '/api/v1'

Axios.interceptors.request.use(
    config => {
        if (store.state.auth.token)
            config.headers[ 'Authorization' ] = `Bearer ${ store.state.auth.token }`
        return config
    },
    error => Promise.reject(error)
)

Axios.interceptors.response.use(
    response => {
        return response
    },
    error => {
        // request not authorized, sign out user
        if (error.response.status === 401)
            store.dispatch(LOGOUT).then(() => App.$router.replace('/login'))

        // backend not available - bad gateway
        else if (error.response.status === 502)
            App.notify.error('Failed to fetch data. Backend is currently not available (502).')

        // backend not available - gateway timeout
        else if (error.response.status === 504)
            App.notify.error('Failed to fetch data. Backend is currently not available (504).')

        else {
            const data = error.response.data
            const message = data.detail || data.message || data
            if (error.response.status >= 400 && error.response.status < 500)
                App.notify.warn(message)
            else if (error.response.status > 500 && error.response.status)
                App.notify.error(message)

            return Promise.reject(error)
        }

    }
)

export default Axios
