# Python Kütüphane Uygulaması

Bu proje, Python 202 Bootcamp kapsamında OOP, harici API kullanımı ve FastAPI ile kendi API'nizi yazmayı birleştirir. Terminal uygulamasından başlayıp, harici veriyle zenginleştirip, son aşamada bir web servisine dönüştürülür.

## Proje Aşamaları

### 1. OOP ile Terminalde Kütüphane
- Kitap ekleme, silme, arama ve listeleme işlemleri
- Veriler `library.json` dosyasında saklanır
- Tüm işlemler nesne yönelimli olarak `Book` ve `Library` sınıfları ile yapılır

### 2. Harici API ile Veri Zenginleştirme
- Kitap eklerken sadece ISBN girilir, başlık ve yazar bilgisi otomatik olarak Open Library API'den çekilir
- Hatalı ISBN veya bağlantı sorununda kullanıcı bilgilendirilir

### 3. FastAPI ile Kendi API'niz
- Tüm kütüphane işlemleri bir web servisi olarak sunulur
- `/books` endpoint'leri ile kitap ekleme, silme ve listeleme yapılabilir
- API dokümantasyonu için `/docs` adresi kullanılabilir

---

## Kurulum

1. Reponunuzu klonlayın:

```bash
git clone <repo-adresiniz>
cd library
```

2. Sanal ortam oluşturun ve aktif edin (isteğe bağlı):

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows için
```

3. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

---

## Kullanım

### Terminal Uygulaması (Aşama 1-2)

```bash
python main.py
```

- Kitap eklerken sadece ISBN girmeniz yeterli, başlık ve yazar otomatik gelir.


### API Sunucusu (Aşama 3)

```bash
uvicorn api:app --reload
# veya sanal ortamda:
& .venv\Scripts\uvicorn.exe api:app --reload
```

- Tarayıcıda [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) adresine giderek interaktif API dokümantasyonunu kullanabilirsiniz.

### Docker ile Çalıştırma

1. Docker yüklü olmalı.
2. Proje klasöründe terminal açıp aşağıdaki komutları çalıştırın:

```bash
docker build -t kutuphane-api .
docker run -p 8000:8000 kutuphane-api
```

- Sonra tarayıcıda [http://localhost:8000/docs](http://localhost:8000/docs) adresine gidin.

> Not: Eğer `uvicorn` hatası alırsanız, Dockerfile zaten güncellenmiştir. Her şey çalışır durumda olmalı.

#### API Endpoint'leri

- `GET /books` : Tüm kitapları listeler
- `POST /books` : ISBN ile kitap ekler. Body örneği: `{ "isbn": "978-0321765723" }`
- `DELETE /books/{isbn}` : Belirtilen ISBN'e sahip kitabı siler

---

## Testler

- Terminal uygulaması için:

```bash
pytest test_main.py
```

- API için:

```bash
pytest test_api.py
```

---

## Katkı ve Geliştirme

- Kodda bolca açıklama notlar bulacaksınız.
- İleri seviye için SQLite, PUT ile güncelleme veya web arayüzü ekleyebilirsiniz.
