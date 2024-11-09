// Utilities
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useUserStore } from './user'
import { storeToRefs } from 'pinia'

export const useComponentsStore = defineStore('components', () => {
    const { user } = storeToRefs(useUserStore())
    const components = ref([])
    const build = ref(0)
    const query = ref('')
    const endpoint = '/api/v1/components/'
    const currentComponent = ref({
        repository: '',
        build: 0,
        properties: []
    })
    const defaultComponent = ref({
        repository: '',
        build: 0,
        properties: []
    })
    const alertMessage = ref('')
    const alertType = ref('success')
    const pageSize = ref(10)
    const pageNumber = ref(1)
    const total = ref(0)

    async function getComponents() {
        const queryStr = query.value ? `&repository__contains=${query.value}`: ''
        const buildQuery = build.value ? `&build=${build.value}` : ''
        const response = await fetch(`${endpoint}?page=${pageNumber.value}&page_size=${pageSize.value}${queryStr}${buildQuery}`)
        if (response.ok) {
            const data = await response.json()
            components.value = data.results
            total.value = data.count
        }
    }

    async function createComponent() {
        if (user.value.token) {
            const response = await fetch(endpoint, {
                method: 'post',
                body: JSON.stringify(currentComponent.value),
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
                alertMessage.value = `Create successfully for component: ${data.repository}`
                Object.assign(currentComponent.value, data)
            }
        }
    }

    async function updateComponent() {
        if (user.value.token) {
            const response = await fetch(`${endpoint}${currentComponent.value.id}/`, {
                method: 'put',
                body: JSON.stringify(currentComponent.value),
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
                Object.assign(currentComponent.value, data)
                alertType.value = 'success'
                alertMessage.value = `Updated successfully for component: ${data.repository}`
            }
        }
    }

    async function deleteComponent() {
        if (user.value.token) {
            const response = await fetch(`${endpoint}${currentComponent.value.id}/`, {
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

    return { components, currentComponent, defaultComponent, alertType, 
        alertMessage, user, build, query, pageNumber, pageSize, total, 
        getComponents, createComponent, updateComponent, deleteComponent }
})
