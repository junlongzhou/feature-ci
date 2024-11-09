<template>
    <FeatureDetail :feature="currentFeature"></FeatureDetail>
</template>

<script setup>
import { onMounted } from 'vue'
import { useFeaturesStore } from '@/stores/features'
import { storeToRefs } from 'pinia'
import router from '@/router'

const { currentFeature } = storeToRefs(useFeaturesStore())
const { getFeature } = useFeaturesStore()

onMounted(async () =>{
    if(router.currentRoute && router.currentRoute.value.params.id){
        await getFeature(router.currentRoute.value.params.id)
    }
})
</script>
