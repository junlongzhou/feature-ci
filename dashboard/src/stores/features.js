// Utilities
import { defineStore, storeToRefs } from 'pinia'
import { ref } from 'vue'
import { useUserStore } from './user'

export const useFeaturesStore = defineStore('features', () => {
    const features = ref([])
    const endStatus = ['wip', 'abandoned', 'merged']
    const { user } = storeToRefs(useUserStore())
    const alertMessage = ref('')
    const alertType = ref('success')
    const currentFeature = ref({
        name: '',
        description: '',
        changes: [],
        build: null,
        last_update_author: null,
        properties: []
    })
    const defaultFeature = ref({
        name: '',
        description: '',
        changes: [],
        build: null,
        last_update_author: null,
        properties: []
    })
    const pageSize = ref(10)
    const pageNumber = ref(1)
    const total = ref(0)
    const endpoint = '/api/v1/features/'

    async function getFeatures() {
        const response = await fetch(`${endpoint}?page=${pageNumber.value}&page_size=${pageSize.value}`, { method: 'GET' })
        const data = await response.json();
        features.value = data.results
        total.value = data.count
    }

    async function getFeature(id) {
        const response = await fetch(`${endpoint}${id}/`)
        currentFeature.value = await response.json()
    }

    async function createFeature() {
        if (user.value.token) {
            currentFeature.value.last_update_author = user.value.id
            const response = await fetch(endpoint, {
                method: 'post',
                body: JSON.stringify(currentFeature.value),
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
                alertMessage.value = `Create successfully for feature: ${data.name}`
                Object.assign(currentFeature.value, data)
            }
        }
    }

    async function updateFeature() {
        if (user.value.token) {
            currentFeature.value.last_update_author = user.value.id
            const response = await fetch(`${endpoint}${currentFeature.value.id}/`, {
                method: 'put',
                body: JSON.stringify(currentFeature.value),
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
                Object.assign(currentFeature.value, data)
                alertType.value = 'success'
                alertMessage.value = `Updated successfully for feature: ${data.name}`
            }
        }
    }

    async function deleteFeature() {
        if (user.value.token) {
            const response = await fetch(`${endpoint}${currentFeature.value.id}/`, {
                method: 'PATCH',
                headers: {
                    "Authorization": `Token ${user.value.token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ action: "abandon" })
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

    async function approveFeature() {
        if (user.value.token) {
            const response = await fetch(`${endpoint}${currentFeature.value.id}/`, {
                headers: {
                    "Authorization": `Token ${user.value.token}`,
                    "Content-Type": "application/json"
                },
                method: 'PATCH',
                body: JSON.stringify({ action: "approve" })
            })
            if (!response.ok) {
                alertType.value = 'error'
                alertMessage.value = response.body
            } else {
                const data = await response.json()
                Object.assign(currentFeature.value, data)
                alertType.value = 'success'
                alertMessage.value = 'Approved successfully'
            }
        }
    }

    function isFeatureEditable(status){
        return !endStatus.includes(status?.toLowerCase())
    }

    return {
        defaultFeature, endStatus, currentFeature, features, user, pageSize, pageNumber, total, alertMessage, alertType,
        getFeatures, createFeature, updateFeature, deleteFeature, approveFeature, getFeature, isFeatureEditable
    }
})
