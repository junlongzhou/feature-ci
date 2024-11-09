<template>
    <v-container fluid>
        <v-card class="elevation-2">
            <v-card-title>
                <v-alert :type="alertType" density="compact" theme="dark" :text="alertMessage" v-model="alert"
                    elevation="3" closable></v-alert>
            </v-card-title>
            <v-data-table-server fixed-header :headers="headers" :items="components"
                :sort-by="[{ key: 'id', order: 'asc' }]" v-model:items-per-page="pageSize" v-model:page="pageNumber"
                :items-length="total" :items-per-page-options="[10, 15, 20]" @update:options="getComponents">
                <template v-slot:top>
                    <v-toolbar color="white" v-if="user.token">
                        <v-spacer></v-spacer>
                        <v-dialog v-model="dialog" max-width="900px">
                            <template v-slot:activator="{ props }">
                                <v-btn prepend-icon="mdi-plus" class="mr-3" v-bind="props" color="primary"
                                    variant="elevated">
                                    New
                                </v-btn>
                            </template>
                            <v-card>
                                <v-card-title>
                                    <span class="text-h5">{{ formTitle }}</span>
                                </v-card-title>

                                <v-card-text>
                                    <ComponentForm v-model="currentComponent"></ComponentForm>
                                </v-card-text>

                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="primary" variant="elevated" @click="close">
                                        Cancel
                                    </v-btn>
                                    <v-btn color="primary" variant="elevated" @click="save">
                                        Save
                                    </v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                        <v-dialog v-model="dialogDelete" max-width="500px">
                            <v-card>
                                <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Cancel</v-btn>
                                    <v-btn color="blue-darken-1" variant="text" @click="deleteItemConfirm">OK</v-btn>
                                    <v-spacer></v-spacer>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </v-toolbar>
                </template>
                <template v-slot:item.actions="{ item }" v-if="user.token">
                    <v-icon class="me-2" size="small" @click="editItem(item)">
                        mdi-pencil
                    </v-icon>
                    <v-icon size="small" @click="deleteItem(item)">
                        mdi-delete
                    </v-icon>
                </template>
                <template v-slot:no-data>
                    <v-btn color="primary" @click="getComponents">
                        Reset
                    </v-btn>
                </template>
            </v-data-table-server>
        </v-card>
    </v-container>
</template>

<script setup>
import { computed, nextTick, ref, watch, onMounted } from 'vue'
import { useComponentsStore } from '@/stores/components'

import { storeToRefs } from 'pinia'

const dialog = ref(false)
const dialogDelete = ref(false)
const headers = ref([
    { title: 'Id', key: 'id' },
    { title: 'Repository', key: 'repository' },
    { title: 'Main branch', key: 'main_branch'},
    { title: 'Actions', key: 'actions', sortable: false },
])
const editedIndex = ref(-1)
const formTitle = computed(() => {
    return editedIndex.value === -1 ? 'New Component' : 'Edit Component'
})
const alert = ref(false)
const { build, currentComponent, defaultComponent, components, user, pageNumber, pageSize, total, alertMessage,
    alertType } = storeToRefs(useComponentsStore())
const { getComponents, createComponent, updateComponent, deleteComponent } = useComponentsStore()

function editItem(item) {
    editedIndex.value = components.value.indexOf(item)
    currentComponent.value = Object.assign({}, item)
    dialog.value = true
}
function deleteItem(item) {
    editedIndex.value = components.value.indexOf(item)
    currentComponent.value = Object.assign({}, item)
    dialogDelete.value = true
}
async function deleteItemConfirm() {
    await deleteComponent()
    components.value.splice(editedIndex.value, 1)
    closeDelete()
    alert.value = true
}
function close() {
    dialog.value = false
    nextTick(() => {
        currentComponent.value = Object.assign({}, defaultComponent.value)
        editedIndex.value = -1
    })
}
function closeDelete() {
    dialogDelete.value = false
    nextTick(() => {
        currentComponent.value = Object.assign({}, defaultComponent.value)
        editedIndex.value = -1
    })
}
async function save() {
    currentComponent.value.properties.forEach((property) => {
        if(Array.isArray(property.value)){
            property.value = property.value.join(',')
        }
    })
    if (editedIndex.value > -1) {
        await updateComponent()
        Object.assign(components.value[editedIndex.value], currentComponent.value)
    } else {
        await createComponent()
        components.value.push(currentComponent.value)
    }
    close()
    alert.value = true
}
watch(dialog, val => {
    val || close()
})
watch(dialogDelete, val => {
    val || closeDelete()
})
onMounted(() => {
    pageSize.value = 10
    pageNumber.value = 1
    build.value = 0
    getComponents()
})
</script>
