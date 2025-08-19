import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from api import app

# FastAPI uygulaması için test client'ı
client = TestClient(app)

def test_get_books():
    # Başlangıçta kitap listesi boş olabilir
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Geçerli bir ISBN ile kitap ekle, tekrar eklemeye çalış, sil ve silineni tekrar silmeye çalış
def test_post_and_delete_book():
    isbn = "9780140328721"  # Matilda (örnek)
    # 1. Kitap ekle
    response = client.post("/books", json={"isbn": isbn})
    assert response.status_code == 200
    data = response.json()
    assert data["isbn"] == isbn
    # 2. Aynı ISBN ile tekrar eklemeye çalış (hata beklenir)
    response2 = client.post("/books", json={"isbn": isbn})
    assert response2.status_code == 400
    # 3. Kitabı sil
    del_response = client.delete(f"/books/{isbn}")
    assert del_response.status_code == 200
    assert del_response.json()["message"].startswith("Kitap silindi")
    # 4. Silinmiş kitabı tekrar silmeye çalış (hata beklenir)
    del_response2 = client.delete(f"/books/{isbn}")
    assert del_response2.status_code == 404

# Geçersiz ISBN ile ekleme denemesi
def test_post_invalid_isbn():
    response = client.post("/books", json={"isbn": "0000000000000"})
    assert response.status_code == 404 or response.status_code == 400

# Eksik body ile kitap eklemeye çalış (hata beklenir)
def test_post_missing_body():
    response = client.post("/books", json={})
    assert response.status_code == 422  # Unprocessable Entity
