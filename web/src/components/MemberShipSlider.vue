<script setup>
import {onMounted} from 'vue'
import {Swiper, SwiperSlide} from 'swiper/vue'
import {Autoplay} from 'swiper/modules'
import 'swiper/css/navigation'
import {usePlanStore} from "@/stores/planStore.js";
import {postUser} from "@/services/apiService.js";
import {useUserStore} from "@/stores/userStore.js";

const userStore = useUserStore()
const planService = usePlanStore()
onMounted(async () => planService.initPlans())

const postPlan = async (plan) => {
  if (!userStore.token) {
    alert("Lütfen abone olmadan önce giriş yapınız.")
    return
  }

  try {
    const response = await postUser('registerPlan', { planId: plan.id })  // plan ID varsa onu gönder
    alert("Abonelik başarıyla oluşturuldu!")
  } catch (error) {
    alert("Abonelik oluşturulurken bir hata oluştu.")
    console.error(error)
  }
}

</script>

<template>
  <Swiper
      v-if="planService.plans.length > 0"
      :modules="[Autoplay]"
      :loop="true"
      :observer="true"
      :observe-parents="true"
      :slides-per-view="Math.min(planService.plans.length, 3)"
      :space-between="20"
      :speed="10000"
      :autoplay="{
  disableOnInteraction: false,
  pauseOnMouseEnter: true,
  delay: 3000,
  }"
      :allow-touch-move="false"
      :breakpoints="{
  768: { slidesPerView: 2 },
  1024: { slidesPerView: 3 }
  }"
      class="pb-8"
  >
    <SwiperSlide v-for="plan in planService.plans" :key="plan.id">
      <div @click="postPlan(plan)"
          class="bg-white shadow-lg rounded-lg p-6 text-center h-full hover:scale-[1.03]">
        <h3 class="text-3xl text-blue-600 font-bold mb-2">{{ plan.name }}</h3>
        <p class="text-2xl font-extrabold text-black mb-4">{{ plan.price }}₺ / ay</p>
        <ul class="text-sm text-gray-600 space-y-3 my-2">
          <li>⏰ Saatlik Sorgu Hakkı: {{ plan.membershipQueryHour }}</li>
          <li>📆 Günlük Sorgu Hakkı: {{ plan.membershipQueryDay }}</li>
        </ul>
        <button class="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 text-center w-20">Abone Ol</button>
      </div>
    </SwiperSlide>
  </Swiper>
</template>

<style scoped>
.swiper {
  padding-bottom: 3rem;
}
</style>
