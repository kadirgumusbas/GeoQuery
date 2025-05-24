# GeoQuery 🌍

GeoQuery, konuma dayalı sorgulamalar yapmanıza olanak tanıyan, kullanıcı ve üyelik sistemi entegre, modern bir Vue 3 + Django REST API tabanlı web uygulamasıdır.
![image](https://github.com/user-attachments/assets/8e816f38-342a-4a2d-b8a8-14c38231478a)
![image](https://github.com/user-attachments/assets/b8e56a7e-1b51-4459-b4ff-754176031d63)
![image](https://github.com/user-attachments/assets/b337eb61-d168-443e-8eb9-2289d0be7147)
![image](https://github.com/user-attachments/assets/11ca5f94-b8ca-44c1-b76f-b5bbcf014104)
![image](https://github.com/user-attachments/assets/7a29e051-1253-411c-a979-08043f2cfec8)
![image](https://github.com/user-attachments/assets/37292127-e6c4-4c84-b27b-f5077fd7e77d)
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

cd frontend
npm install
npm run dev
```

🧑‍💻 Geliştirici
Kadir Gümüşbaş

Proje türü: Web teknolojileri staj projesi

Amaç: Vue ve Django REST Framework ile modern bir konum tabanlı üyelik sistemi geliştirmek
