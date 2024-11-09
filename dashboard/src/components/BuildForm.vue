<template>
    <v-container>
        <v-form>
            <v-text-field v-model="build.name" label="Name" variant="outlined"
                :rules="[v => !!v || 'Build name is required']" required></v-text-field>
            <v-text-field v-model="build.product" label="Product" variant="outlined"
                :rules="[v => !!v || 'Build product is required']" required></v-text-field>
            <v-card variant="outlined">
                <v-toolbar color="white">
                    <v-toolbar-title>Configuration</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn prepend-icon="mdi-plus" class="mr-3" color="primary" variant="elevated"
                        @click="addPropertyTemplate">
                        New
                    </v-btn>
                </v-toolbar>
                <v-card-text>
                    <v-container>
                        <v-row v-for="property_template in build.property_templates" no-gutters>
                            <v-col class="ml-1">
                                <v-select density="compact" label="Kind" v-model="property_template.kind"
                                    :items="['COMPONENT', 'FEATURE']" variant="outlined" required></v-select>
                            </v-col>
                            <v-col class="ml-1">
                                <v-select density="compact" label="Widget" v-model="property_template.style.widget"
                                    :items="['select', 'select_multiple', 'text']" variant="outlined"
                                    required></v-select>
                            </v-col>
                            <v-col class="ml-1">
                                <v-text-field density="compact" v-model="property_template.name" label="Config name"
                                    variant="outlined" :rules="[v => !!v || 'Config name is required']"
                                    required></v-text-field>
                            </v-col>
                            <v-col class="ml-1">
                                <v-text-field density="compact" v-model="property_template.values" label="Config Value"
                                    variant="outlined" :rules="[v => !!v || 'Config values are required']"
                                    @update:modelValue="updateConfigValues(property_template)" required></v-text-field>
                            </v-col>
                            <v-col class="ml-1">
                                <v-checkbox density="compact" v-model="property_template.style.read_only"
                                    label="Read Only" variant="outlined" required></v-checkbox>
                            </v-col>
                            <v-col class="ml-1">
                                <v-checkbox density="compact" v-model="property_template.style.hidden"
                                    label="Hidden" variant="outlined" required></v-checkbox>
                            </v-col>
                            <v-col class="ml-1 my-2">
                                <v-icon @click="removeProperty(property_template)">
                                    mdi-delete
                                </v-icon>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
            </v-card>
        </v-form>
    </v-container>
</template>
<script setup>
const build = defineModel()

function addPropertyTemplate() {
    build.value.property_templates.push({
        name: '',
        values: '',
        style: {
            widget: 'select',
            read_only: false,
            values: ''
        }
    })
}

function updateConfigValues(property_templates) {
    property_templates.style.values = property_templates.values
}

function removeProperty(property_template){
    const deleteIndex = build.value.property_templates.indexOf(property_template)
    if(deleteIndex> -1){
        build.value.property_templates.splice(deleteIndex, 1)
    }
}
</script>
