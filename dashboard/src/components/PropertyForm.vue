<template>
    <template v-for="(property, index) in properties">
        <v-text-field :density="props.density" :class="[spaceClass, (property.style.hidden && props.mode === 'default') ? 'd-none': '' ]" v-if="property.style.widget === 'text'"
            v-model="property.value" :key="index" :label="property.name" variant="outlined"
            :readonly="property.style.read_only"></v-text-field>
        <v-select :density="props.density" :class="[spaceClass, (property.style.hidden && props.mode === 'default') ? 'd-none': '' ]" v-else v-model="property.value"
            :items="property.style.values.split(',')" :label="property.name" variant="outlined"
            :multiple="property.style.widget === 'select_multiple'" item-title="" item-value="value"
            :readonly="property.style.read_only && props.mode === 'default'" chips></v-select>
    </template>
</template>

<script setup>
import { onMounted } from 'vue';

const properties = defineModel()
const props = defineProps({
    density: {
        type: String,
        default: 'default'
    },
    spaceClass: {
        type: String,
        default: ''
    },
    mode: {
        type: String,
        default: 'default'
    }
})

onMounted(() => {
    if (properties.value) {
        properties.value.forEach((item) => {
            if (item.style.widget === 'select_multiple') {
                item.value = item.value.split(',')
            }
        })
    }
})
</script>
