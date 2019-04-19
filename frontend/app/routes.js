// import your module routes here, i.e.
// import MyModuleRoutes from 'MyModule/routes'

export default [
    {
        name: 'login',
        path: '/login',
        component: () => import('app/modules/Auth/Login.vue'),
        meta: { auth: false }
    },
    {
        name: 'index',
        path: '/',
        component: () => import('app/modules/Auth/Index.vue'),
        meta: { auth: true }
    }
].concat(
    // register your module routes here, i.e.
    // ...MyModuleRoutes
    {
        path: '*',
        component: { render: h => h('h1', null, 'Route not found') }
    }
)
