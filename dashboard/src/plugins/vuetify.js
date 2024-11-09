/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          primary: "#124191",
          secondary: '#005aff',
          accent: '#edf2f5',
          error: '#e23b3b',
          info: '#00c9ff',
          success: '#37cc73',
          warning: '#f7b737',
          white: '#ffffff',
          orange: 'f47f31',
          teal: '23abb6',
          purple: '7d33f2'
        }
      }
    }
  },
})
