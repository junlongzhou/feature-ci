<template>
    <v-timeline direction="horizontal" size="small" truncate-line="both" class="mb-4" side="end">
        <v-timeline-item v-for="item in props.items" :dot-color="item.color" icon="mdi-check-bold" fill-dot>
            {{item.text}}
        </v-timeline-item>
    </v-timeline>
</template>

<script setup>
const props = defineProps(['items'])
</script>