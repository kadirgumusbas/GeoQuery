<script setup>
import PerformanceChart from '@/components/charts/PerformanceChart.vue'
import {onMounted, ref} from 'vue'
import {getRequest} from '@/services/apiService'
import MapModal from "@/components/MapModal.vue";

const geoData = ref([])

onMounted(async () => {
  geoData.value = await getRequest('pquery')
})

const showModal = ref(false);
const selectedCoords = ref({lat: 0, lng: 0})

function openModal(lat, lng) {
  selectedCoords.value = {lat, lng}
  showModal.value = true
}


</script>

<template>
  <div class="pt-14 rounded-lg shadow h-screen flex flex-col">
    <h2 class="text-black text-xl font-semibold mb-4">Queries</h2>

    <!-- Grafik kısmı -->
    <div class="md:h-1/2 w-full">
      <PerformanceChart/>
    </div>

    <!-- Scrollable Geo verileri -->
    <div class="h-1/2 w-1/2 overflow-y-auto p-4 space-y-4 border border-gray-200">
      <div
          v-for="item in geoData"
          :key="item.query_time"
          class="cursor-pointer bg-white border border-gray-200 shadow-md rounded-md p-4 hover:bg-blue-50 transition"
          @click="openModal(item.lat, item.lng)"
      >
        <p class="text-sm text-gray-800 font-semibold">📍 Location: {{ item.lat }}, {{ item.lng }}</p>
        <p class="text-sm text-gray-700">💳 Membership: {{ item.membership_plan }}</p>
        <p class="text-sm text-gray-600">⏰ Time: {{ new Date(item.query_time).toLocaleString() }}</p>
      </div>
    </div>
  </div>
  <MapModal :visible="showModal" @close="showModal = false" :lat="selectedCoords.lat" :lng="selectedCoords.lng"/>
</template>

