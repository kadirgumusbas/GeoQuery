<script setup>
import 'swiper/css'
import MemberShipSlider from "@/components/MemberShipSlider.vue";
import Earth from "@/components/Earth.vue";

</script>

<template>
  <!-- 1. Tanıtım Bölümü -->
  <section class="flex flex-col h-screen md:flex-row items-center justify-between px-8 py-12">
    <div class="md:w-1/2">
      <h1 class="text-3xl font-bold mb-4">GeoQuery ile harita bazlı sorgular çok kolay!</h1>
      <p class="text-gray-600">Koordinat gir, haritayı kullan, geçmişini yönet.</p>
    </div>
    <div class="md:w-1/2">
      <!-- örnek görsel -->
      <Earth />
    </div>
  </section>

  <!-- 2. Slider Bölümü -->
  <section class="bg-gray-50 py-8">
    <h2 class="text-2xl font-semibold text-center mb-6">Üyelik Planları</h2>
    <div class="px-4">
      <MemberShipSlider />
    </div>
  </section>

</template>

<style scoped>
.hero-section {
  background-image: url('@/assets/background-image.jpg'); /* Görseli assets klasörüne koyduğunu varsayıyoruz */
  background-size: cover;
  background-position: center;
}
</style>
