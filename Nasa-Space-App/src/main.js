import 'bootstrap-icons/font/bootstrap-icons.min.css';

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import App from './App.vue'
import router from './router'
import vueAwesomeSidrebar from 'vue-awesome-sidebar'
import 'vue-awesome-sidebar/dist/vue-awesome-sidebar.css'


const app = createApp(App)

app.use(vueAwesomeSidrebar)
app.use(createPinia())
app.use(router)

app.mount('#app')

