<template>
    <v-container fluid>
        <v-card class="elevation-2">
            <v-card-title>
                <v-alert :type="alertType" density="compact" theme="dark" :text="alertMessage" v-model="alert"
                    elevation="3" closable></v-alert>
            </v-card-title>
            <v-data-table-server fixed-header :headers="headers" :items="builds"
                :sort-by="[{ key: 'id', order: 'asc' }]" v-model:items-per-page="pageSize" v-model:page="pageNumber"
                :items-length="total" :items-per-page-options="[10, 15, 20]" @update:options="getBuilds">
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
                                    <BuildForm v-model="currentBuild"></BuildForm>
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
                    <v-btn color="primary" @click="getBuilds">
                        Reset
                    </v-btn>
                </template>
            </v-data-table-server>
        </v-card>
    </v-container>
</template>

<script setup>
import { computed, nextTick, ref, watch, onMounted } from 'vue'
import { useBuildsStore } from '@/stores/builds'
import { storeToRefs } from 'pinia'

const dialog = ref(false)
const dialogDelete = ref(false)
const headers = ref([
    { title: 'Id', key: 'id' },
    { title: 'Name', key: 'name' },
    { title: 'Product', key: 'product' },
    { title: 'Actions', key: 'actions', sortable: false },
])
const editedIndex = ref(-1)
const formTitle = computed(() => {
    return editedIndex.value === -1 ? 'New Build' : 'Edit Build'
})
const alert = ref(false)
const { currentBuild, defaultBuild, builds, user, pageNumber, pageSize, total, alertMessage,
    alertType } = storeToRefs(useBuildsStore())
const { getBuilds, createBuild, updateBuild, deleteBuild } = useBuildsStore()

function editItem(item) {
    editedIndex.value = builds.value.indexOf(item)
    currentBuild.value = Object.assign({}, item)
    dialog.value = true
}
function deleteItem(item) {
    editedIndex.value = builds.value.indexOf(item)
    currentBuild.value = Object.assign({}, item)
    dialogDelete.value = true
}
async function deleteItemConfirm() {
    await deleteBuild()
    builds.value.splice(editedIndex.value, 1)
    closeDelete()
    alert.value = true
}
function close() {
    dialog.value = false
    nextTick(() => {
        currentBuild.value = Object.assign({}, defaultBuild.value)
        editedIndex.value = -1
    })
}
function closeDelete() {
    dialogDelete.value = false
    nextTick(() => {
        currentBuild.value = Object.assign({}, defaultBuild.value)
        editedIndex.value = -1
    })
}
async function save() {
    if (editedIndex.value > -1) {
        await updateBuild()
        Object.assign(builds.value[editedIndex.value], currentBuild.value)
    } else {
        await createBuild()
        builds.value.push(currentBuild.value)
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
    getBuilds()
})
</script>
