# GeoQuery 🌍

GeoQuery, konuma dayalı sorgulamalar yapmanıza olanak tanıyan, kullanıcı ve üyelik sistemi entegre, modern bir Vue 3 + Django REST API tabanlı web uygulamasıdır.

---

## 🚀 Özellikler

### 🔐 Kimlik Doğrulama
- JWT tabanlı kullanıcı kayıt ve giriş sistemi
- Kullanıcı bilgileri `Pinia` store ve `localStorage` ile yönetilir

### 🧾 Üyelik Sistemi
- Üyelik planları: FREE, PREMIUM vb.
- Planlar Swiper ile slider olarak gösterilir
- Üyelik planları backend'den fiyatlarına göre sıralanarak çekilir
- Her kullanıcı planına göre sorgu hakkı alır (saatlik/günlük)

### 📍 Harita Tabanlı Sorgulama
- Kullanıcı koordinat girerek ya da haritadan seçerek sorgu yapabilir
- `MapLibre` ile harita gösterimi, marker yerleştirme
- `Nominatim` kullanılarak reverse geocode yapılır ve adres bilgisi alınır
- Her sorgu `Query` modeli ile kaydedilir

### 📊 Dashboard & Grafikler
- Kullanıcılar aylık toplam sorgularını görebilir
- Admin panelinde tüm kullanıcıların aylık sorgu verileri gösterilir
- `Chart.js` ile çizilmiş interaktif `Line` grafikleri

### 🛠️ Admin Panel
- Admin kullanıcıları filtreleyip listeleyebilir
- Her kullanıcı için toplam sorgu sayısı ve üyelik bilgisi görünür
- Kullanıcıların sorgu geçmişi harita üzerinden izlenebilir
- Kullanıcı tablosu sıralanabilir (`Username`, `Name`, `Queries` vb.)

---

## 🛠️ Teknolojiler

### Frontend
- [Vue 3](https://vuejs.org/)
- [Pinia](https://pinia.vuejs.org/) (state management)
- [Vue Router](https://router.vuejs.org/)
- [Swiper](https://swiperjs.com/) (üyelik slider)
- [Chart.js + vue-chartjs](https://vue-chartjs.org/) (grafikler)
- [MapLibre GL JS](https://maplibre.org/) (açık kaynak harita)

### Backend
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- JWT kimlik doğrulama
- Özel `Query`, `Membership`, `Geo`, `QuerySum` modelleri
- Admin filtreleme, sorgu limitleri kontrolü, kullanıcı plan yönetimi

---

## 📦 Kurulum

### Backend

```bash
cd backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
