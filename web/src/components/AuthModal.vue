<script setup>
import { ref } from 'vue'
import {registerService, loginService} from "@/services/userService.js";
import {useUserStore} from "@/stores/userStore.js";


const props = defineProps({
  visible: Boolean,
  mode: String // 'login' veya 'register'
})
const emit = defineEmits(['close'])
const close = () => emit('close')
const form = ref({
  username: '',
  name: '',
  surname: '',
  email: '',
  password: '',
  confirmPassword: '',
  phone: '',
})
const userStore = useUserStore()

async function userService() {
  try {
    let result
    if (props.mode === 'login') {
      result = await loginService(form.value)
      if (result) {
        userStore.setUser(result)
      }
    } else {
      result = await registerService(form.value)
      if (result) {
        alert(`${result.message}\nWelcome GeoQuery\n${result.username}\nYou can log in from the login section.`)
      }
    }
    close()
  } catch (error) {
    // errors şimdi { username: [...], email: [...] } objesi
    const messages = Object.values(error).flat()
    alert(messages.join('\n'))
  }
}

</script>

<template>
  <div
      v-if="visible"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="close"
  >
    <div class="bg-white relative rounded-lg shadow-lg w-[90%] max-w-md p-6">
      <!-- Kapatma butonu -->
      <button
          @click="close"
          class="absolute top-2 right-2 p-1 text-black hover:text-black transition-colors"
          style="background: transparent; border: none;"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
             fill="none" stroke="currentColor"
             stroke-linecap="round" stroke-linejoin="round"
             width="24" height="24" stroke-width="2">
          <path d="M10 10l4 4m0 -4l-4 4"></path>
          <path d="M12 3c7.2 0 9 1.8 9 9s-1.8 9 -9 9s-9 -1.8 -9 -9s1.8 -9 9 -9z"></path>
        </svg>
      </button>

      <!-- Başlık -->
      <h2 class="text-xl font-semibold mb-4 text-center">
        {{ mode === 'login' ? 'Login' : 'Register' }}
      </h2>
      <form @submit.prevent="userService">
        <input v-model="form.username" type="text" placeholder="Username" class="w-full mb-3 p-2 border rounded"/>
        <input v-model="form.password" type="password" placeholder="Password" class="w-full mb-3 p-2 border rounded"/>
        <div v-if="mode === 'register'">
          <input v-model="form.confirmPassword" type="password" placeholder="Confirm Password"
                 class="w-full mb-3 p-2 border rounded"/>
          <div class="w-full">
            <div>
              <input v-model="form.name" type="text" placeholder="Name" class="w-1/2 mb-3 p-2 border rounded"/>
              <input v-model="form.surname" type="text" placeholder="Surname" class="w-1/2 mb-3 p-2 border rounded"/>
            </div>
          </div>
          <input v-model="form.email" type="email" placeholder="Email" class="w-full mb-3 p-2 border rounded"/>
          <input v-model="form.phone" type="number" placeholder="Phone" class="w-full mb-3 p-2 border rounded"/>
        </div>
        <div v-if="mode === 'register'">
          <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Register
          </button>
        </div>
        <div v-else>
          <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"

          >
            Login
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

