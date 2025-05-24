<script setup>
import {ref, onMounted} from 'vue'
import {initializeMap, setMarker, resetMap} from '@/services/mapService.js'
import {postQuery} from "@/services/apiService.js";

import {reverseGeocode} from '@/services/mapService.js'

const latitude = ref('')
const longitude = ref('')
const queryHistory = ref([])


onMounted(() => {
  initializeMap('map', ({lat, lng}) => {
    latitude.value = lat.toFixed(6)
    longitude.value = lng.toFixed(6)
  })
})

async function saveQuery() {
  try {
    const result = await postQuery(latitude.value, longitude.value)
    if (result && result.timestamp) {
      const locationInfo = await reverseGeocode(latitude.value, longitude.value)
      console.log(locationInfo)
      console.log('Adres bilgisi:', locationInfo.display_name)
      queryHistory.value.unshift({
        lat: latitude.value,
        lon: longitude.value,
        address: locationInfo.display_name || 'Adres bulunamadı',
        timestamp: result.timestamp
      })
    } else {
      alert("⚠️ Sorgu başarılı ama zaman bilgisi yok.")
    }
  } catch (e) {
    alert(`❌ Hata: ${e.message}`)
  }
}

const handleGoToLocation = () => {
  if (latitude.value >= -90 && latitude.value <= 90 && longitude.value <= 90 && longitude.value >= -90) {
    if (latitude.value && longitude.value) {
      setMarker(parseFloat(latitude.value), parseFloat(longitude.value), 10)
      saveQuery()
    } else {
      alert("Between -90 and 90")
    }
  } else {
    alert("Between -90 and 90")
  }
}

</script>

<template>
  <div class="flex min-h-screen bg-transparent bg-gray-100">
    <!-- Inputlar -->
    <div class="w-full md:w-1/4 bg-gray-100 p-4 shadow">
      <form @submit.prevent="saveQuery" class="flex flex-col md:flex-row gap-4">
        <input
            v-model="longitude"
            type="number"
            step="any"
            placeholder="Longitude"
            class="w-28  p-2 border rounded"
        />
        <input
            v-model="latitude"
            type="number"
            step="any"
            placeholder="Latitude"
            class="w-28 p-2 border rounded"
        />
        <button type="button"
                class="w-20 px-4 py-1 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 transition items-center"
                @click="handleGoToLocation">
          Find
        </button>
        <button type="reset"
                class="w-20 px-4 py-1 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 transition items-center"
                @click="resetMap">
          Clear
        </button>
      </form>
      <!-- Sorgu Geçmişi -->
      <div v-if="queryHistory.length"
           class="mt-6 bg-white p-4 rounded shadow text-sm text-gray-700 max-h-screen overflow-y-auto">
        <h3 class="text-base font-semibold mb-2">🔎 Sorgu Geçmişi</h3>
        <ul class="space-y-2">
          <li v-for="(q, index) in queryHistory" :key="index" class="border-b pb-2">
            <p><strong>Time:</strong> {{ q.timestamp }}</p>
            <p><strong>Coordinates:</strong> {{ q.lat }}, {{ q.lon }}</p>
            <span><strong>Address:</strong></span>
            <span
                class="cursor-pointer text-blue-600 hover:underline"
                @click="setMarker(parseFloat(q.lat), parseFloat(q.lon), 7)">
              {{ q.address }}
            </span>
          </li>
        </ul>
      </div>

    </div>

    <!-- Harita -->
    <div id="map" class="flex-grow rounded-3xl bg-gray-100"></div>
  </div>
</template>
