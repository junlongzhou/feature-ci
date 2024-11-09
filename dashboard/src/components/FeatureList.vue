<template>
    <v-container fluid>
        <v-card class="elevation-2">
            <v-card-title>
                <v-alert :type="alertType" density="compact" theme="dark" :text="alertMessage" v-model="alert"
                    elevation="3" closable></v-alert>
            </v-card-title>
            <v-data-table-server fixed-header :headers="headers" :items="features"
                :sort-by="[{ key: 'id', order: 'asc' }]" v-model:items-per-page="pageSize" v-model:page="pageNumber"
                :items-length="total" :items-per-page-options="[10, 15, 20]" @update:options="getFeatures">
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
                                    <FeatureForm v-model="currentFeature"></FeatureForm>
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
                <template v-slot:item.name="{ item }">
                    <a :href="`/features/${item.id}/`">{{item.name}}</a>
                </template>
                <template v-slot:item.status="{ item }">
                    <StatusChip :status="item.status"></StatusChip>
                </template>
                <template v-slot:item.actions="{ item }" v-if="user.token">
                    <v-icon v-show="isEditable(item)" class="me-2" size="small" @click="editItem(item)">
                        mdi-pencil
                    </v-icon>
                    <v-icon v-show="isEditable(item)" size="small" @click="deleteItem(item)">
                        mdi-delete
                    </v-icon>
                </template>
                <template v-slot:no-data>
                    <v-btn color="primary" @click="getFeatures">
                        Reset
                    </v-btn>
                </template>
            </v-data-table-server>
        </v-card>
    </v-container>
</template>

<script setup>
import { computed, nextTick, ref, watch, onMounted } from 'vue'
import { useFeaturesStore } from '@/stores/features'
import { storeToRefs } from 'pinia'
import StatusChip from './StatusChip.vue';

const dialog = ref(false)
const dialogDelete = ref(false)
const headers = ref([
    {
        title: 'Feature ID',
        align: 'start',
        key: 'id',
        sortable: true
    },
    { title: 'Name', key: 'name' },
    { title: 'Status', key: 'status', align: 'center' },
    { title: 'Owner', key: 'last_update_author' },
    { title: 'Updated', key: 'last_update_date' },
    { title: 'Actions', key: 'actions', sortable: false },
])
const editedIndex = ref(-1)
const formTitle = computed(() => {
    return editedIndex.value === -1 ? 'New Feature' : 'Edit Feature'
})

const alert = ref(false)
const { features, currentFeature, defaultFeature, user, pageNumber,
    pageSize, total, alertMessage, alertType
} = storeToRefs(useFeaturesStore())
const { getFeatures, createFeature, updateFeature, deleteFeature, isFeatureEditable } = useFeaturesStore()

function editItem(item) {
    editedIndex.value = features.value.indexOf(item)
    currentFeature.value = Object.assign({}, item)
    dialog.value = true
}
function deleteItem(item) {
    editedIndex.value = features.value.indexOf(item)
    currentFeature.value = Object.assign({}, item)
    dialogDelete.value = true
}
async function deleteItemConfirm() {
    await deleteFeature()
    features.value.splice(editedIndex.value, 1)
    closeDelete()
    alert.value = true
}
function close() {
    dialog.value = false
    nextTick(() => {
        currentFeature.value = Object.assign({}, defaultFeature.value)
        editedIndex.value = -1
    })
}
function closeDelete() {
    dialogDelete.value = false
    nextTick(() => {
        currentFeature.value = Object.assign({}, defaultFeature.value)
        editedIndex.value = -1
    })
}
async function save() {
    currentFeature.value.properties.forEach((property) => {
        if (Array.isArray(property.value)) {
            property.value = property.value.join(',')
        }
    })
    currentFeature.value.changes.forEach((change) => {
        change.properties.forEach((property) => {
            if (Array.isArray(property.value)) {
                property.value = property.value.join(',')
            }
        })
    })
    if (editedIndex.value > -1) {
        await updateFeature()
        Object.assign(features.value[editedIndex.value], currentFeature.value)
    } else {
        await createFeature()
        features.value.push(currentFeature.value)
    }
    close()
    alert.value = true
}

function isEditable(item) {
    const itemIndex = features.value.indexOf(item)
    if (itemIndex != -1) {
        return isFeatureEditable(features.value[itemIndex].status)
    }
    return true
}

watch(dialog, val => {
    val || close()
})
watch(dialogDelete, val => {
    val || closeDelete()
})
onMounted(() => {
    getFeatures()
    currentFeature.value = Object.assign({}, defaultFeature.value)
    editedIndex.value = -1
})
</script>
