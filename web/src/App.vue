<script setup>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import {useRoute} from "vue-router";
import {computed} from "vue";

const route = useRoute()

const url = computed(() => {
  return route.path === '/'
})

</script>
<template>
  <Navbar/>
  <div class="min-h-screen flex flex-col pt-13">
    <main class="flex-grow">
      <router-view/>
    </main>
    <div v-if="url">
      <Footer/>
    </div>
  </div>
</template>

<style scoped>


</style>
