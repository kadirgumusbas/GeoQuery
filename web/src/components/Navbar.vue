<script setup>
import {computed, onMounted, onUnmounted, ref, watch} from 'vue'
import AuthModal from "@/components/AuthModal.vue";
import {useUserStore} from "@/stores/userStore.js";
import {getRequest} from "@/services/apiService.js";
import {useRoute} from "vue-router";

const route = useRoute();
const isQueryPage = computed(() => {
  return route.path === '/query' || route.path === '/query/'
})
const isAdmin = ref(false)
const isVisible = ref(true)
let lastScrollY = window.scrollY
const handleScroll = () => {
  if (!isQueryPage.value) {
    const currentScrollY = window.scrollY
    currentScrollY > lastScrollY ? isVisible.value = false : isVisible.value = true
    lastScrollY = currentScrollY
  }
}
const planName = ref('FREE')
const showModal = ref(false)
const modalMode = ref('login') // 'login' veya 'register'
const userStore = useUserStore()
const username = computed(() => userStore.username)

const openModal = (mode) => {
  modalMode.value = mode
  showModal.value = true
}

onMounted(async () => {
  if (userStore.token) {
    const res = await getRequest('userPlan')
    planName.value = res.planName
  }
})

onMounted(async () => {
  const res = await getRequest('isAdmin')
  if (res) {
    isAdmin.value = res
  }
})

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const handleLogout = () => {
  userStore.logout()
  isAdmin.value = false
}

watch(() => userStore.username, async (newUsername) => {
  if (newUsername) {
    isAdmin.value = await getRequest('isAdmin')
  } else {
    isAdmin.value = false
  }
})

</script>

<template>
  <nav
      class="top-0 left-0 w-full bg-white shadow z-50 transition-transform duration-300"
      :class="{ 'fixed -translate-y-full': !isVisible }"
  >
    <div class="max-w-7xl mx-auto px-4 py-2 flex justify-between items-center">
      <div class="flex items-center space-x-6">
        <router-link to="/">
          <h1 class="text-xl font-bold text-blue-600">GeoQuery</h1></router-link>
        <router-link to="/" class="text-blue-600 hover:underline">Home</router-link>
        <router-link to="/query" class="text-blue-600 hover:underline">Query</router-link>
        <div v-if="isAdmin">
          <router-link to="/management" class="text-blue-600 hover:underline">Management</router-link>
        </div>
      </div>
      <div v-if="username">
        <div class="space-x-4">
          <router-link :to="`/profile/${username}`">
            <button
                class="w-20 px-4 py-1 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 transition">Profile
            </button>
          </router-link>
          <router-link to="/">
            <button
                @click="handleLogout()"
                class="w-20 px-4 py-1 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 transition">Çıkış
            </button>
          </router-link>
          <span class="text-blue-600"><strong>{{ planName }}</strong></span>
        </div>
      </div>
      <div v-else>
        <div class="space-x-4">
          <button @click="openModal('login')"
                  class="px-4 py-1 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 transition">Login
          </button>
          <button @click="openModal('register')"
                  class="px-4 py-1 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 transition">Register
          </button>
        </div>
      </div>
    </div>
  </nav>
  <AuthModal :visible="showModal" :mode="modalMode" @close="showModal = false"/>
</template>

<style scoped>
</style>
