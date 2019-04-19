<template>
    <v-container fluid fill-height>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md4>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Log into django-api-vue</v-toolbar-title>
                        <v-spacer />
                    </v-toolbar>
                    <v-form v-with-form-errors @submit.prevent="attemptLogin">
                        <v-card-text>
                            <v-text-field v-model="loginData.username"
                                          required
                                          label="Login"
                                          prepend-icon="person"
                                          :error-messages="errors.collect('username')"
                                          data-vv-name="username"
                            />
                            <v-text-field v-model="loginData.password"
                                          v-validate="'required'"
                                          required
                                          label="Password"
                                          prepend-icon="lock"
                                          type="password"
                                          :error-messages="errors.collect('password')"
                                          data-vv-name="password" />
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer />
                            <v-btn color="primary" type="submit">Login</v-btn>
                        </v-card-actions>
                    </v-form>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import { mapActions, mapGetters } from 'vuex'

    import { LOGIN } from './store/types'

    export default {
        data: () => ({
            loginData: {
                username: '',
                password: ''
            }
        }),
        computed: { ...mapGetters([ 'isAuthenticated' ]) },
        methods: {
            ...mapActions({ login: LOGIN }),
            async attemptLogin() {
                this.resetBackendErrors()
                if (!await this.$validator.validateAll())
                    return

                this.login(this.loginData)
                    .then(() => {
                        if (this.isAuthenticated)
                            this.$router.replace('/')
                    })
                    .catch(err => this.handleBackendError(err))
            }
        }
    }
</script>
