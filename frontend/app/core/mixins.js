import Vue from 'vue'
import { arrayize } from '../utils'

const FormErrors = Vue.extend({
    name: 'FormErrors',
    props: { state: { required: true, type: Object } },
    template: `<v-alert transition="slide-y-transition" v-if="state.any('form')" type="error" :value="true">
  <span v-for="msg in state.all('form')">{{ msg }}<br /></span>
</v-alert>`
})

export const formExtras = {
    install(Vue) {
        Vue.directive('with-form-errors', {
            inserted(el, bindings, vnode) {
                const node = document.createElement('div')
                el.prepend(node)

                new FormErrors({
                    el: node,
                    propsData: { state: vnode.context.$validator.errors }
                })
            }
        }),
            Vue.mixin({
                methods: {
                    resetBackendErrors(errors = this.$validator.errors) {
                        errors.clear('form')
                        errors.clear('server')
                    },
                    handleBackendError(error, errors = this.$validator.errors) {
                        let data = error.response && error.response.data
                        if (!data)
                            return
                        Object.keys(data).forEach(field => {
                            if (field === '__all__')
                                errors.add({
                                    field: '__all__',
                                    scope: 'form',
                                    msg: arrayize(data[ field ]).join(', ')
                                })
                            else
                                errors.add({
                                    field,
                                    scope: 'server',
                                    msg: arrayize(data[ field ]).join(', ')
                                })

                        })
                    }
                }
            })
    }
}
