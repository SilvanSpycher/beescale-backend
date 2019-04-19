<template>
    <v-container fluid fill-height>
        <v-layout>
            <v-flex xs12 sm8 md4>
                <pre>{{ user }}</pre>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import { mapActions, mapState } from 'vuex'

    import { GET_USER_PROFILE } from './store/types'

    export default {
        computed: { ...mapState({ user: state => state.auth.user }) },
        mounted() {
            this.getProfile()
        },
        methods: { ...mapActions({ getProfile: GET_USER_PROFILE }) }
    }
</script>
