import {createApp} from 'vue'
import App from './App.vue'
import {createPinia} from 'pinia'
import router from './router/index.js'
import './assets/style.css'
import {useUserStore} from '@/stores/userStore.js'

const app = createApp(App)

app.use(router)
app.use(createPinia())
const userStore = useUserStore()
userStore.loadUserFromStorage()
app.mount('#app')

