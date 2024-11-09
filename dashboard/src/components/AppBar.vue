<template>
    <v-app-bar dark color="primary" density="compact" elevation="0" class="position-fixed">
        <v-app-bar-title>FCI Dashboard</v-app-bar-title>
        <v-spacer></v-spacer>
        <v-btn icon class="mx-2">
            <v-icon @click.stop="drawer = !drawer">mdi-dots-vertical</v-icon>
        </v-btn>
        <v-divider vertical class="mx-2"></v-divider>
        <v-btn v-if="user.token" append-icon="mdi-account-circle" @click="handleUser">
            {{ user.username }}
        </v-btn>
        <v-btn v-else variant="outlined" append-icon="mdi-login" @click="handleUser">
            Login
        </v-btn>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" location="right" temporary>
        <v-list-item :title="user.username">
            <template v-slot:prepend>
                <v-avatar color="primary">
                    <v-icon icon="mdi-account-circle"></v-icon>
                </v-avatar>
            </template>
        </v-list-item>
        <v-divider></v-divider>
        <v-list color="primary" density="compact" nav>
            <v-list-item prepend-icon="mdi-apps" title="Features" value="features" @click="toPage('/')">
            </v-list-item>
            <v-list-item prepend-icon="mdi-list-box" title="Builds" value="builds"
                @click="toPage('/management/builds')">
            </v-list-item>
            <v-list-item prepend-icon="mdi-source-repository" title="Components" value="components"
                @click="toPage('/management/components')">
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>
<script setup>
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'
import router from '@/router'

const { user } = storeToRefs(useUserStore())
const { logout } = useUserStore()
const drawer = ref(false)

function handleUser() {
    if (user.value.token) {
        logout()
    } else {
        router.push('/login')
    }
}
function toPage(pagePath) {
    router.push(pagePath)
}
</script>
