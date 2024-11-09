// Utilities
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useUserStore } from './user'
import { storeToRefs } from 'pinia'


export const useBuildsStore = defineStore('builds', () => {
    const { user } = storeToRefs(useUserStore())
    const builds = ref([])
    const currentBuild = ref({
        name: '',
        product: '',
        property_templates: []
    })
    const defaultBuild = ref({
        name: '',
        product: '',
        property_templates: []
    })
    const alertMessage = ref('')
    const alertType = ref('success')
    const pageSize = ref(10)
    const pageNumber = ref(1)
    const total = ref(0)
    const endpoint = '/api/v1/builds/'

    async function getBuilds() {
        const response = await fetch(`${endpoint}?page=${pageNumber.value}&page_size=${pageSize.value}`)
        const data = await response.json()
        builds.value = data.results
        total.value = data.count
    }

    async function getBuild(id) {
        const response = await fetch(`${endpoint}${id}/`)
        const data = await response.json()
        currentBuild.value = data
    }

    async function createBuild() {
        if (user.value.token) {
            const response = await fetch(endpoint, {
                method: 'post',
                body: JSON.stringify(currentBuild.value),
                headers: {
                    "Authorization": `Token ${user.value.token}`,
                    "Content-Type": "application/json"
                }
            })
            if (!response.ok) {
                alertType.value = 'error'
                alertMessage.value = response.body
            } else {
                const data = await response.json()
                alertType.value = 'success'
                alertMessage.value = `Create successfully for build: ${data.name}`
                Object.assign(currentBuild.value, data)
            }
        }
    }

    async function updateBuild() {
        if (user.value.token) {
            const response = await fetch(`${endpoint}${currentBuild.value.id}/`, {
                method: 'put',
                body: JSON.stringify(currentBuild.value),
                headers: {
                    "Authorization": `Token ${user.value.token}`,
                    "Content-Type": "application/json"
                }
            })
            if (!response.ok) {
                alertType.value = 'error'
                alertMessage.value = response.body
            } else {
                const data = await response.json()
                Object.assign(currentBuild.value, data)
                alertType.value = 'success'
                alertMessage.value = `Updated successfully for build: ${data.name}`
            }
        }
    }

    async function deleteBuild() {
        if (user.value.token) {
            const response = await fetch(`${endpoint}${currentBuild.value.id}/`, {
                method: 'delete',
                headers: {
                    "Authorization": `Token ${user.value.token}`
                }
            })
            if (!response.ok) {
                alertType.value = 'error'
                alertMessage.value = response.body
            } else {
                alertType.value = 'success'
                alertMessage.value = 'Removed successfully'
            }
        }
    }

    return {
        user, currentBuild, defaultBuild, builds, alertMessage, alertType,
        pageSize, pageNumber, total, getBuilds, createBuild, updateBuild, deleteBuild, getBuild
    }
})
