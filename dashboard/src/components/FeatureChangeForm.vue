<template>
    <v-card variant="outlined">
        <v-card-text>
            <v-container>
                <v-row>
                    <v-autocomplete label="Components" v-model="selectedComponents" item-value="id"
                        item-title="display_name" :items="components" variant="outlined"
                        @update:modelValue="updateComponents" @update:search="searchComponents" multiple chips
                        @update:focused="updateComponents"></v-autocomplete>
                </v-row>
                <v-row v-for="change in changes" class="my-3">
                    <v-card width="850px">
                        <v-card-title>
                            {{ findComponent(change.component)?.display_name }}
                        </v-card-title>
                        <v-card-text>
                            <v-container>
                                <v-row>
                                    <v-text-field class="mx-1" density="compact" v-model="change.source_branch"
                                        label="Source Branch" variant="outlined"></v-text-field>
                                    <v-text-field class="mx-1" density="compact" v-model="change.target_branch"
                                        label="Target Branch" variant="outlined"></v-text-field>
                                    <PropertyForm :spaceClass="'mx-1'" density="compact" v-model="change.properties">
                                    </PropertyForm>
                                </v-row>
                            </v-container>
                        </v-card-text>
                    </v-card>
                </v-row>
            </v-container>
        </v-card-text>
    </v-card>
</template>

<script setup>
import { useComponentsStore } from '@/stores/components'
import { storeToRefs } from 'pinia'
import { ref, onMounted } from 'vue';

const changes = defineModel()
const props = defineProps(['branch'])
const selectedComponents = ref([])
const { components, query, pageSize } = storeToRefs(useComponentsStore())
const { getComponents } = useComponentsStore()

onMounted(() => {
    pageSize.value = 500
    if (changes.value) {
        changes.value.forEach((item) => {
            if(findComponent(item.component)){
                selectedComponents.value.push(item.component)
            }
        })
    }
})

defineExpose({
    refresh: () => {
        selectedComponents.value.splice(0)
        if (changes.value) {
            changes.value.forEach((item) => {
                if(findComponent(item.component)){
                    selectedComponents.value.push(item.component)
                }
            })
            updateComponents()
        }
    }
})

function updateComponents() {
    if (changes.value) {
        changes.value.splice(0)
    }
    selectedComponents.value.forEach((item) => {
        const foundComponent = findComponent(item)
        if (foundComponent) {
            changes.value.push({
                component: item,
                source_branch: props.branch,
                target_branch: foundComponent?.main_branch ? foundComponent.main_branch : 'master',
                properties: foundComponent.properties ? foundComponent.properties : []
            })
        }
    })
}

async function searchComponents(search) {
    query.value = search
    await getComponents()
}

function findComponent(componentId) {
    return components.value.find((item) => item.id === componentId)
}
</script>
