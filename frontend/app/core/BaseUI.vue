<template>
    <v-app id="root" :class="env">
        <notifications position="bottom right" />
        <v-navigation-drawer v-model="drawer" temporary absolute color="primary">
            <v-list class="grow">
                <v-list-tile
                    v-for="link in links"
                    :key="link.label"
                    :to="link.to"
                >
                    <v-list-tile-action>
                        <v-icon>{{ link.icon }}</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-title v-text="link.label" />
                </v-list-tile>
            </v-list>
        </v-navigation-drawer>

        <v-toolbar v-if="isAuthenticated" app fixed
                   clipped-left
                   color="primary">
            <v-toolbar-side-icon @click.stop="drawer = !drawer" />
            <v-toolbar-title>{{ appName }}</v-toolbar-title>
            <v-spacer />
            <v-toolbar-items>
                <v-btn flat @click.prevent="attemptLogout">Logout</v-btn>
            </v-toolbar-items>
        </v-toolbar>

        <v-content>
            <v-container fluid fill-height>
                <v-layout>
                    <v-flex>
                        <v-fade-transition mode="out-in">
                            <router-view />
                        </v-fade-transition>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-content>

        <v-footer app fixed dark color="primary">
            <span style="padding:10px">v{{ version }} &copy; 2018</span>
        </v-footer>
    </v-app>
</template>

<script>
    import { mapActions, mapGetters } from 'vuex'

    import { LOGOUT } from 'app/modules/Auth/store/types'

    import { name, version } from '@/../package.json'


    export default {
        data: () => ({
            drawer: false,
            version,
            env: __TEST__ ? 'test' : __PROD__ ? 'production' : 'local',
            appName: name,
            links: [
                {
                    label: 'Home',
                    icon: 'home',
                    to: '/'
                },
                {
                    label: 'Test 1',
                    icon: 'theaters',
                    to: '/test1'
                },
                {
                    label: 'Test 2',
                    icon: 'content_paste',
                    to: '/test2'
                }
            ]
        }),
        computed: { ...mapGetters([ 'isAuthenticated' ]) },
        methods: {
            ...mapActions({ logout: LOGOUT }),
            attemptLogout() {
                this.logout()
                this.$router.replace('/login')
            }
        }
    }
</script>
