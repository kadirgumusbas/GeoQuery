<script setup>
import { links } from '@/constants/social_links.js'
</script>
<template>
  <footer class="bg-gray-100 text-center text-sm text-gray-600 py-6 shadow-inner">
    <div class="flex flex-col md:flex-row justify-center items-center gap-6 mb-3">
      <a
          v-for="link in links"
          :key="link.name"
          :href="link.url"
          target="_blank"
          :class="[link.color, 'transition']">
        <i :class="[link.icon, 'text-xl']"></i> {{ link.name }}
      </a>
    </div>
    <p class="text-xs text-gray-500">&copy; 2025 GeoQuery | Bu proje <strong>N2Mobil</strong> için hazırlanmıştır.</p>
  </footer>
</template>
<style scoped>

</style>
