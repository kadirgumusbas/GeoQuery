import {createRouter, createWebHistory} from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import QueryPage from "@/pages/QueryPage.vue";
import ManagementPage from "@/pages/ManagementPage.vue";
import ProfilePage from "@/pages/ProfilePage.vue";


const routes = [
    {path: '/', component: HomePage},
    {path: '/query', component: QueryPage},
    {path: '/management', component: ManagementPage},
    {path: '/profile/:username', component: ProfilePage},
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
