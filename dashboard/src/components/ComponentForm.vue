<template>
    <v-container>
        <v-form>
            <v-text-field v-model="component.repository" label="Repository" variant="outlined"
                :rules="[v => !!v || 'Component repository is required']" required></v-text-field>
            <v-text-field v-model="component.main_branch" label="Main Branch" variant="outlined"
                :rules="[v => !!v || 'Component main branch is required']" required></v-text-field>
            <v-select label="Build" v-model="component.build" @update:modelValue="updateProperties" :items="builds"
                item-value="id" item-title="name" variant="outlined" required></v-select>
            <v-card>
                <v-card-title>
                    Configuration
                </v-card-title>
                <v-card-text>
                    <PropertyForm v-model="component.properties" mode="edit">
                    </PropertyForm>
                </v-card-text>
            </v-card>
        </v-form>
    </v-container>
</template>
<script setup>
import { useBuildsStore } from '@/stores/builds'
import { storeToRefs } from 'pinia'

const component = defineModel()
const { builds, pageSize } = storeToRefs(useBuildsStore())
const { getBuilds } = useBuildsStore()

onMounted(() => {
    pageSize.value = 500
    updateProperties()
})

async function updateProperties() {
    await getBuilds()
    const foundBuild = builds.value.find((build) => build.id === component.value.build)
    if (!foundBuild) {
        foundBuild = builds.value[0]
    }
    let newProperties = []
    foundBuild.property_templates.forEach((property) => {
        const existedProperty = component.value.properties.find((item) => item.name === property.name)
        if (property.kind === 'COMPONENT') {
            if (!property.style.values) {
                property.style.values = property.values
            }
            let defaultValue = ''
            if (existedProperty) {
                defaultValue = existedProperty.value
            } else {
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
    component.value.properties.slice(0)
    component.value.properties = newProperties
}
</script>
