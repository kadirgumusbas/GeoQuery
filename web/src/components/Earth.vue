<template>
  <div class="earth-container">
    <div id="controls">
    </div>
    <div ref="container" class="globe-container"></div>
  </div>
</template>

<script>
import {ref, onMounted, onBeforeUnmount} from 'vue'
import * as THREE from 'three'

export default {
  name: 'EarthGlobe',
  setup() {
    const container = ref(null)
    const isAutoRotating = ref(true)
    let scene, camera, renderer, earth
    let animationFrameId

    const init = () => {
      // Sahne oluşturma
      scene = new THREE.Scene()
      scene.background = new THREE.Color(0xffffff)

      // Kamera oluşturma
      camera = new THREE.PerspectiveCamera(
          75,
          400 / 400, // Sabit boyut oranı
          0.1,
          1000
      )
      camera.position.z = 20

      // Renderer oluşturma
      renderer = new THREE.WebGLRenderer({antialias: true})
      renderer.setSize(900, 900) // Sabit boyut
      container.value.appendChild(renderer.domElement)

      // Dünya geometrisi
      const geometry = new THREE.SphereGeometry(7, 64, 64)
      const textureLoader = new THREE.TextureLoader()
      const texture = textureLoader.load(
          'https://threejs.org/examples/textures/planets/earth_atmos_2048.jpg'
      )
      const material = new THREE.MeshPhongMaterial({
        map: texture,
        specular: new THREE.Color(0x333333),
        shininess: 15,
        emissive: new THREE.Color(0x112244), // Bu satır emissive özelliğini tanımlıyor
        emissiveIntensity: 0.2, // Bu satır emissive yoğunluğunu belirliyor
      })

      earth = new THREE.Mesh(geometry, material)
      scene.add(earth)
      // Türkiye tarafını göstermek için dünya modelini döndür
      earth.rotation.y = -THREE.MathUtils.degToRad(125)
      earth.rotation.x = -THREE.MathUtils.degToRad(-30)
      // Işıklandırma
      const light = new THREE.DirectionalLight(0xffffff, 1)
      light.position.set(5, 3, 5)
      scene.add(light)
      const ambientLight = new THREE.AmbientLight(0x404040)
      scene.add(ambientLight)

      // Mouse kontrolleri
      let mouseDown = false
      let previousMousePosition = {x: 0, y: 0}

      const onMouseDown = (e) => {
        mouseDown = true
        previousMousePosition = {
          x: e.clientX,
          y: e.clientY
        }
      }

      const onMouseUp = () => {
        mouseDown = false
      }

      const onMouseMove = (e) => {
        if (mouseDown) {
          const deltaMove = {
            x: e.clientX - previousMousePosition.x,
            y: e.clientY - previousMousePosition.y
          }

          earth.rotation.y += deltaMove.x * 0.005
          earth.rotation.x += deltaMove.y * 0.005

          previousMousePosition = {
            x: e.clientX,
            y: e.clientY
          }
        }
      }

      // Event listener'ları ekleme
      renderer.domElement.addEventListener('mousedown', onMouseDown)
      renderer.domElement.addEventListener('mouseup', onMouseUp)
      renderer.domElement.addEventListener('mousemove', onMouseMove)

      // Cleanup fonksiyonu
      onBeforeUnmount(() => {
        renderer.domElement.removeEventListener('mousedown', onMouseDown)
        renderer.domElement.removeEventListener('mouseup', onMouseUp)
        renderer.domElement.removeEventListener('mousemove', onMouseMove)
        cancelAnimationFrame(animationFrameId)
        renderer.dispose()
      })
    }

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate)
      //
      // if (isAutoRotating.value) {
      //   earth.rotation.y += 0.003
      // }

      renderer.render(scene, camera)
    }

    const toggleRotation = () => {
      isAutoRotating.value = !isAutoRotating.value
    }

    onMounted(() => {
      init()
      animate()
    })

    return {
      container,
      isAutoRotating,
      toggleRotation
    }
  }
}
</script>

<style scoped>
.earth-container {
  display: flex;
  justify-content: center;
  background: transparent;
}

.globe-container {
  width: 900px;
  height: 900px;
  border-radius: 10px;
  overflow: hidden;
  background: transparent;
}

</style>