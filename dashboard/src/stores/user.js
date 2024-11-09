// Utilities
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
    const user = localStorage.getItem('fci-user') ? ref(JSON.parse(localStorage.getItem('fci-user'))) : ref({ username: '', password: '', token: '', id: 0 })
    const loginResult = ref('')
    const isValid = ref(true)
    const endpoint = '/api/v1/auth/'

    async function login() {
        const response = await fetch(endpoint, {
            method: 'post',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(user.value),
        })
        const json = await response.json()
        if (json.token && json.id) {
            user.value.token = json.token
            user.value.id = json.id
            isValid.value = true
            loginResult.value = ''
            localStorage.setItem('fci-user', JSON.stringify(json))
        } else {
            loginResult.value = 'Username or password invalid.'
            isValid.value = false
        }
    }

    function logout() {
        user.value.id = 0
        user.value.token = ''
        user.value.username = ''
        user.value.password = ''
        localStorage.removeItem('fci-user')
    }

    return { user, isValid, loginResult, login, logout }
})
