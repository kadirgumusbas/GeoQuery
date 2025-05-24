import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'

let map = null
let marker = null

export function initializeMap(containerId, onClickCallback = null) {
    map = new maplibregl.Map({
        container: containerId,
        style: 'https://api.maptiler.com/maps/streets/style.json?key=A1FGISe61qfemUr129Fx',
        center: [0, 0],
        zoom: 2
    })

    map.on('click', (e) => {
        const lat = e.lngLat.lat
        const lng = e.lngLat.lng

        // Marker'ı güncelle
        if (marker)
            marker.remove()

        marker = new maplibregl.Marker().setLngLat([lng, lat]).addTo(map)
        map.flyTo({
            center: [lng, lat],
            zoom: 10
        })

        // Harici callback çağır (örneğin component'e lat/lng gönder)
        if (onClickCallback) {
            onClickCallback({lat, lng})
        }
    })
}

export function resetMap() {
    if (marker)
        marker.remove()
    map.flyTo({
        center: [0, 0],
        zoom: 2
    })
}

export function setMarker(lat, lng, zoom = 10) {
    if (!map) return

    // Eski markerı kaldır
    if (marker) marker.remove()

    // Yeni marker ekle
    marker = new maplibregl.Marker().setLngLat([lng, lat]).addTo(map)

    // Haritayı konuma götür
    map.flyTo({
        center: [lng, lat],
        zoom: zoom
    })
}

export async function reverseGeocode(lat, lon) {
  const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`)
  if (!response.ok) {
    throw new Error('Ters geokodlama başarısız')
  }
  return await response.json()
}
