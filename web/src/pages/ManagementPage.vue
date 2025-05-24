<script setup>

import PerformanceChart from "@/components/charts/PerformanceChart.vue";
import {computed, ref, onMounted} from "vue";
import {getRequest} from "@/services/apiService.js";

const userData = ref()
const sortKey = ref('username')
const sortAsc = ref(true)

const sortedUsers = computed(() => {
  if (!userData.value) return []
  return [...userData.value].sort((a, b) => {
    const aVal = a[sortKey.value]
    const bVal = b[sortKey.value]

    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return sortAsc.value ? aVal - bVal : bVal - aVal
    }

    const aStr = aVal?.toString().toLowerCase() || ''
    const bStr = bVal?.toString().toLowerCase() || ''

    if (aStr < bStr) return sortAsc.value ? -1 : 1
    if (aStr > bStr) return sortAsc.value ? 1 : -1
    return 0
  })
})

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value
  } else {
    sortKey.value = key
    sortAsc.value = true
  }
}

onMounted(async () => {
  userData.value = await getRequest('adminUser')
})


</script>

<template>
  <div class="pt-14 rounded-lg shadow min-h-screen flex flex-col overflow-hidden">
    <h2 class="text-black text-xl font-semibold mb-4">Queries</h2>

    <div class="flex flex-1 overflow-hidden">
      <!-- Sol taraf: Grafik -->
      <div class="w-1/2 h-full p-4">
        <PerformanceChart :is-management="true"/>
      </div>

      <!-- Sağ taraf: Tablo -->
      <div class="w-1/2 h-full p-4">
        <div class="overflow-y-auto max-h-[calc(100vh-6rem)] border rounded">
          <table class="min-w-full bg-white border border-gray-300 rounded text-sm text-left">
            <thead class="bg-gray-100 sticky top-0">
            <tr>
              <th v-for="header in ['username', 'name', 'surname', 'email', 'totalQueries', 'membership']"
                  :key="header"
                  @click="sortBy(header)"
                  class="overflow-y-auto max-h-screen p-2 border-b border-gray-300 cursor-pointer hover:bg-gray-200 transition">
                {{ header.charAt(0).toUpperCase() + header.slice(1) }}
                <span v-if="sortKey === header">{{ sortAsc ? '▲' : '▼' }}</span>
              </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="user in sortedUsers" :key="user.username" class="hover:bg-blue-50 transition">
              <td class="p-2 border-b">{{ user.username }}</td>
              <td class="p-2 border-b">{{ user.name }}</td>
              <td class="p-2 border-b">{{ user.surname }}</td>
              <td class="p-2 border-b">{{ user.email }}</td>
              <td class="p-2 border-b">{{ user.totalQueries }}</td>
              <td class="p-2 border-b">{{ user.membership }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>

</style>