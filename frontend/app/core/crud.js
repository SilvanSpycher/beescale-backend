import Axios from 'axios'
import { App } from 'app'

export default class CRUDService {
    constructor(endpoint, prefix='') {
        if (!endpoint)
            throw new Error('No endpoint specified')

        this.url = `${prefix}/${endpoint}/`
        this.$http = Axios
    }

    getObjectURL(id) {
        return `${this.url}${id}/`
    }

    // extraParams is for curried functions
    list(params, extraParams = {}) {
        return this.$http.get(this.url, { params: { ...params, ...extraParams } })
    }

    get(id, params) {
        return (!id)
            ? Promise.reject('Missing id.')
            : this.$http.get(this.getObjectURL(id), { params })
    }

    save(record, params = {}) {
        return (record.id)
            ? this.$http.patch(this.getObjectURL(record.id), record, { params })
                .then((response) => {

                    App.notify.success('Saved successfully.')
                    return response
                })
            : this.$http.post(this.url, record, { params })
                .then((response) => {
                    App.notify.success('Saved successfully.')
                    return response
                })
    }

    remove(id) {
        return (!id)
            ? Promise.reject('Missing id.')
            : this.$http.delete(this.getObjectURL(id))
                .then((response) => {
                    App.notify.warning('Record deleted.')
                    return response
                })
    }
}
