<template>
    <v-container>
        <v-form>
            <v-text-field v-model="feature.name" label="Name" variant="outlined"
                :rules="[v => !!v || 'Feature name is required']" required></v-text-field>
            <v-textarea v-model="feature.description" required label="Description" variant="outlined"
                :rules="[v => !!v || 'Feature description is required']"></v-textarea>
            <v-select label="Build" v-model="feature.build" item-value="id" item-title="name" :items="builds"
                variant="outlined" @update:modelValue="updateBuild" @update:focused="updateBuild" required></v-select>
            <PropertyForm v-model="feature.properties"></PropertyForm>
            <FeatureChangeForm ref="changesFormRef" v-model="feature.changes" :branch="feature.name"></FeatureChangeForm>
        </v-form>
    </v-container>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useBuildsStore } from '@/stores/builds'
import { useComponentsStore } from '@/stores/components';

const feature = defineModel()
const { builds } = storeToRefs(useBuildsStore())
const { getBuilds } = useBuildsStore()
const { build } = storeToRefs(useComponentsStore())
const { getComponents } = useComponentsStore()
const changesFormRef = ref(null)

async function updateBuild(){
    if(feature.value && feature.value.build){
        build.value = feature.value.build
        await getComponents()
        changesFormRef.value.refresh()
        updateFeatureProperties(feature.value.build)
    }
}

function updateFeatureProperties(build){
    const foundBuild = builds.value.find((item) => item.id === build)
    if(foundBuild){
        let newProperties = []
        foundBuild.property_templates.forEach((property) => {
            const existedProperty = feature.value.properties.find((item) => item.name === property.name)
            if(property.kind === 'FEATURE'){
                if(!property.style.values){
                    property.style.values = property.values
                }
                let defaultValue = ''
                if(existedProperty){
                    defaultValue = existedProperty.value
                }else{
                    const splits = property.values.split(',')
                    defaultValue = splits ? splits[0] : property.values
                }
                newProperties.push({
                    name: property.name,
                    value: defaultValue,
                    style: property.style
                })
            }
        })
        feature.value.properties.slice(0)
        feature.value.properties = newProperties
    }
}

onMounted(async () => {
    await getBuilds()
    await updateBuild()
})
</script>
