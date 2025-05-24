<script setup>
import {initializeMap, setMarker, resetMap} from "@/services/mapService.js";
import {nextTick, ref, watch} from 'vue'

import {onMounted} from "vue";

const props = defineProps({
  visible: Boolean,
  lat: Number,
  lng: Number
})

const emit = defineEmits(['close'])
const close = () => emit('close')

watch(
    () => props.visible,
    (newVal) => {
      if (newVal) {
        nextTick(() => {
          initializeMap('map')
          setMarker(props.lat, props.lng, 4)
        })
      }
    },
)

</script>


<template>
  <div
      v-if="visible"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="close"
  >
    <div
        class="bg-white rounded-lg shadow-lg w-full max-w-2xl h-[500px] p-4 flex flex-col relative"
    >
      <!-- Kapatma butonu -->
      <button
          @click="close"
          class="absolute top-2 right-2 p-1 text-black hover:text-black transition-colors"
          style="background: transparent; border: none;"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
             fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
             width="24" height="24" stroke-width="2">
          <path d="M10 10l4 4m0 -4l-4 4"></path>
          <path d="M12 3c7.2 0 9 1.8 9 9s-1.8 9 -9 9s-9 -1.8 -9 -9s1.8 -9 9 -9z"></path>
        </svg>
      </button>

      <!-- Başlık -->
      <h2 class="text-xl font-semibold mb-4 text-center">
        Koordinatlar: {{ props.lat }}, {{ props.lng }}
      </h2>

      <!-- Harita alanı -->
      <div id="map" class="flex-grow rounded border"/>
    </div>
  </div>
</template>

<style scoped>
#map {
  width: 100%;
  height: 100%;
  min-height: 350px;
  border-radius: 8px;
}
</style>