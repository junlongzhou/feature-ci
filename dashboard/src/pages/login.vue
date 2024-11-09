<template>
    <v-container>
        <v-row justify="center" no-gutters>
            <p class="text-center mx-auto mb-3 mt-16">
                <v-avatar color="primary" size="48">
                    <v-icon dark> mdi-lock </v-icon>
                </v-avatar>
            </p>
        </v-row>
        <v-row justify="center" no-gutters>
            <v-card elevation="3" width="450" class="mx-auto">
                <v-card-text>
                    <v-form ref="form" v-model="isValid">
                        <v-text-field v-model="user.username" label="User Name" required></v-text-field>

                        <v-text-field v-model="user.password" label="Password" type="password" required></v-text-field>
                        <v-btn block color="primary" @click="checkAuth"> Log In </v-btn>
                    </v-form>
                    <p class="text-center" v-show="loginResult !== ''">
                        {{ loginResult }}
                    </p>
                </v-card-text>
            </v-card>
        </v-row>
    </v-container>
</template>

<script setup>
import { useUserStore } from '../stores/user.js'
import { storeToRefs } from 'pinia'
import router from '@/router'

const { user, isValid, loginResult } = storeToRefs(useUserStore())
const { login } = useUserStore()

async function checkAuth() {
    await login()
    if (isValid.value === true) {
        router.push('/')
    }
}
</script>
