import VueRouter from 'vue-router'

import routes from 'app/routes'
import { name } from '@/../package.json'
import store from 'app/core/store'

const router = new VueRouter({
    routes,
    linkActiveClass: 'is-active'
})

router.beforeEach((to, from, next) => {
    /* eslint-disable-next-line no-console */
    if (__DEV__) console.info('Route change (from -> to):', from.name, from.params, '-->', to.name, to.params)

    const env = __TEST__ ? '[test] ' : __PROD__ ? '' : '[local] '
    let suffix
    try {
        suffix = to.meta.label ? ` - ${ typeof to.meta.label === 'function' ? to.meta.label() : to.meta.label }` : ''
    } catch (e) {
        suffix = ''
    }
    document.title = `${ env }${ name }${ suffix }`

    // check authentication
    if (to.matched.some(route => route.meta.auth) && !store.getters.isAuthenticated)
        next('/login')
    else
        next()
})

export default router
