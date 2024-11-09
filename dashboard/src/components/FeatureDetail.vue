<template>
    <v-container fluid>
        <v-alert :type="alertType" density="compact" theme="dark" :text="alertMessage" v-model="alert" elevation="3"
            closable></v-alert>
        <v-card elevation="3">
            <v-toolbar>
                <template v-slot:prepend>
                    <StatusChip :status="props.feature.status"></StatusChip>
                </template>
                <v-toolbar-title>{{ props.feature.name }}</v-toolbar-title>
                <v-spacer></v-spacer>
                <p class="font-italic text-body-2 text-disabled mr-3">
                    Last updated by {{ props.feature.last_update_author }} at
                    {{ formatDate(props.feature.last_update_date) }}
                </p>
                <v-dialog v-model="dialog" max-width="900px">
                    <template v-slot:activator="{ props }">
                        <v-btn v-show="isEditable && user.token" icon="mdi-pencil" v-bind="props" color="primary"
                            variant="text">
                        </v-btn>
                    </template>
                    <v-card>
                        <v-card-title>
                            <span class="text-h5">Edit feature</span>
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
                    <template v-slot:activator="{ props }">
                        <v-btn v-show="isEditable && user.token" icon="mdi-delete" v-bind="props" color="primary"
                            variant="text">
                        </v-btn>
                    </template>
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
            <v-card-text>
                <LifecycleTimeline :items="lifecycleItems"></LifecycleTimeline>
                <v-card elevation="3">
                    <v-card-text>
                        <v-row dense>
                            <v-col cols="5" class="font-weight-black text-body-2">Description:</v-col>
                            <v-col class="text-body-2">
                                <a :href="props.feature.change_json" target="_blank">{{ props.feature.description }}</a>
                            </v-col>
                        </v-row>
                        <v-row dense v-for="property in props.feature.properties">
                            <v-col cols="5" class="font-weight-black text-body-2">{{ formatName(property.name)
                                }}:</v-col>
                            <v-col class="text-body-2">
                                {{ property.value }}
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
                <v-card elevation="3" class="mt-4">
                    <v-card-text>
                        <v-table density="compact">
                            <thead>
                                <tr>
                                    <th>Repository Name</th>
                                    <th>Source Branch</th>
                                    <th>Main Branch</th>
                                    <th>Properties</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="change in props.feature.changes">
                                    <td><a :href="change.repository" target="blank">{{ change.display_name
                                            }}</a>
                                    </td>
                                    <td>{{ change.source_branch }}</td>
                                    <td>{{ change.target_branch }}</td>
                                    <td>
                                        <!-- <div class="d-flex flex-column">
                                            <h5 class="font-weight-black"
                                                v-for="changeProperty in formatProperties(change.properties)">
                                                {{ formatName(changeProperty.name) }}: {{ changeProperty.value
                                                }}
                                            </h5>
                                        </div> -->
                                    </td>
                                </tr>
                            </tbody>
                        </v-table>
                    </v-card-text>
                </v-card>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" variant="elevated" v-show="isEditable && user.token" @click="approve">
                    Approve
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>
<script setup>
import { computed, ref } from 'vue'
import { useFeaturesStore } from '@/stores/features'
import { storeToRefs } from 'pinia'
import router from '@/router'

const dialog = ref(false)
const dialogDelete = ref(false)
const props = defineProps(['feature'])
const alert = ref(false)
const { alertMessage, alertType, currentFeature, defaultFeature, user } = storeToRefs(useFeaturesStore())
const { updateFeature, deleteFeature, approveFeature, isFeatureEditable } = useFeaturesStore()
const isEditable = computed(() => {
    return isFeatureEditable(props.feature?.status)
})

const lifecycleItems = computed(() =>{
    if(props.feature?.status === 'MERGED'){
        return [
            {text: 'NEW', color: 'green'},
            {text: 'WIP', color: 'green'},
            {text: 'ACTIVE', color: 'green'},
            {text: 'MERGED', color: 'green'}
        ]
    }else if(props.feature?.status === 'ABANDONED'){
        return [
            {text: 'NEW', color: 'green'},
            {text: 'ABANDONED', color: 'green'}
        ]
    }else{
        return [
            {text: 'NEW', color: 'green'},
            {text: 'WIP', color: 'grey'},
            {text: 'ACTIVE', color: 'grey'},
            {text: 'MERGED', color: 'grey'}
        ]
    }
})

async function deleteItemConfirm() {
    await deleteFeature()
    closeDelete()
    alert.value = true
    router.push('/')
}
function close() {
    dialog.value = false
}
function closeDelete() {
    dialogDelete.value = false
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
    await updateFeature()
    close()
    alert.value = true
}

async function approve() {
    await approveFeature()
    alert.value = true
}

function formatName(originName) {
    let splitStr = originName.split('_')
    for (var i = 0; i < splitStr.length; i++) {
        splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1)
    }
    return splitStr.join(' ')
}

function formatProperties(properties) {
    const formatProperties = []
    properties.forEach((item) => {
        if (!item.style.hidden) {
            formatProperties.push(item)
        }
    })
    return formatProperties
}

function formatDate(val) {
    const dateObj = new Date(val)
    if (isNaN(dateObj)) {
        return val
    }
    return `${dateObj.getFullYear()}-${dateObj.getMonth() + 1
        }-${dateObj.getDate()} ${dateObj.getHours()}:${dateObj.getMinutes()}:${dateObj.getSeconds()}`
}
</script>
