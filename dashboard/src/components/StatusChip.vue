<template>
    <v-chip variant="flat" density="compact" dark :color="color">
        {{props.status}}
    </v-chip>
</template>
<script setup>
import { computed } from 'vue'

const props =defineProps(['status'])
const colorsMap = new Map([
    ['ACTIVE', 'primary'],
    ['WIP', 'brown'],
    ['MERGED', 'green'],
    ['ABANDONED', 'grey']
])
const color = computed(() =>{
    return colorsMap.has(props.status) ? colorsMap.get(props.status) : 'info'
})
</script>
