<script setup>
import {onMounted, ref} from 'vue'
import {
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip
} from 'chart.js'
import {Line} from 'vue-chartjs'
import {useUserStore} from '@/stores/userStore'
import {getRequest} from "@/services/apiService.js";


ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend, Filler)
const props = defineProps({
  isManagement: Boolean,
})
const chartData = ref({
  labels: ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
  datasets: [
    {
      label: 'Number of Queries',
      borderColor: 'rgb(37,99,235)',
      pointBackgroundColor: 'rgb(37,99,235)',
      backgroundColor: 'rgba(38, 198, 218, 0.1)',// rgb(37 99 235
      fill: true,
      tension: 0.4,
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
  ]
})

onMounted(fetchMonthlyStats)

async function fetchMonthlyStats() {
  const userStore = useUserStore()
  const token = userStore.currentUser?.token

  const monthLabels = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
  const queryCountMap = Object.fromEntries(monthLabels.map(m => [m, 0]))
  const userCountMap = Object.fromEntries(monthLabels.map(m => [m, 0]))

  try {
    let queryData = []
    let userData = []

    if (props.isManagement) {
      queryData = await getRequest('adminMonthly')
      userData = await getRequest('adminUsers') // burada kullanıcı sayısı geliyor
    } else {
      queryData = await getRequest('monthly')
    }

    // Sorgu sayıları
    queryData.forEach(item => {
      if (item.month in queryCountMap) {
        queryCountMap[item.month] = item.count
      }
    })

    // Yönetici modunda kullanıcı sayıları
    if (props.isManagement) {
      userData.forEach(item => {
        if (item.month in userCountMap) {
          userCountMap[item.month] = item.count
        }
      })
    }

    // Grafik datası
    chartData.value = {
      labels: monthLabels,
      datasets: [
        {
          label: 'Number of Queries',
          borderColor: 'rgb(37,99,235)',
          pointBackgroundColor: 'rgb(37,99,235)',
          backgroundColor: 'rgba(38, 198, 218, 0.1)',
          fill: true,
          tension: 0.4,
          data: monthLabels.map(month => queryCountMap[month])
        },
        ...(props.isManagement
          ? [{
              label: 'Number of Users',
              borderColor: 'rgb(239, 68, 68)', // kırmızı
              pointBackgroundColor: 'rgb(239, 68, 68)',
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
              fill: true,
              tension: 0.4,
              data: monthLabels.map(month => userCountMap[month])
            }]
          : [])
      ]
    }

  } catch (e) {
    alert('Grafik verisi alınamadı: ' + (e.response?.data?.detail || e.message))
  }
}

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: false,
      ticks: {
        color: '#000000'
      },
      grid: {
        color: '#000000'
      }
    },
    x: {
      ticks: {
        color: '#000000'
      },
      grid: {
        color: '#000000'
      }
    }
  },
  plugins: {
    legend: {
      labels: {
        color: '#000000'
      }
    }
  }
})
</script>

<template>
  <div class="w-full h-96">
    <Line :data="chartData" :options="chartOptions"/>
  </div>
</template>
