# Python tabanlı bir imajdan başla
FROM python:3.11-slim

# Çalışma dizinini oluştur ve ayarla
WORKDIR /app

# Gerekli dosyaları kopyala
COPY . /app

# Bağımlılıkları yükle
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 8000 portunu aç
EXPOSE 8000

# Uygulamayı başlat
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
