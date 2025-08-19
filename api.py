from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import Book, Library
import httpx

# FastAPI uygulaması başlatılıyor
app = FastAPI(title="Kütüphane API")
library = Library()  # Kütüphane nesnesi (JSON dosyasına kaydeder)

# API'ye gelen ISBN verisi için Pydantic modeli
class ISBNRequest(BaseModel):
    isbn: str  # Kullanıcıdan sadece ISBN beklenir

# API'den dönen kitap verisi için Pydantic modeli
class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str

# Tüm kitapları JSON olarak döndüren endpoint
@app.get("/books", response_model=list[BookResponse])
def get_books():
    # Kütüphanedeki tüm kitapları döndür
    return [BookResponse(title=b.title, author=b.author, isbn=b.isbn) for b in library.list_books()]

# ISBN ile kitap ekleyen endpoint
@app.post("/books", response_model=BookResponse)
def add_book(isbn_req: ISBNRequest):
    isbn = isbn_req.isbn
    if library.find_book(isbn):
        # Aynı ISBN ile kitap varsa hata döndür
        raise HTTPException(status_code=400, detail="Bu ISBN ile bir kitap zaten var!")
    url = f"https://openlibrary.org/isbn/{isbn}.json"
    try:
        response = httpx.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            title = data.get("title", "Başlık bulunamadı")
            author = "Bilinmiyor"
            # Yazar bilgisini almak için ek istek
            if "authors" in data and data["authors"]:
                author_key = data["authors"][0]["key"]
                author_url = f"https://openlibrary.org{author_key}.json"
                author_resp = httpx.get(author_url, timeout=10)
                if author_resp.status_code == 200:
                    author = author_resp.json().get("name", "Bilinmiyor")
            book = Book(title, author, isbn)
            library.add_book(book)
            return BookResponse(title=title, author=author, isbn=isbn)
        elif response.status_code == 404:
            # Geçersiz ISBN
            raise HTTPException(status_code=404, detail="Bu ISBN ile kitap bulunamadı.")
        else:
            # API'den beklenmeyen bir cevap
            raise HTTPException(status_code=500, detail="API'den beklenmeyen bir cevap alındı.")
    except httpx.RequestError:
        # İnternet yoksa veya API'ye ulaşılamıyorsa
        raise HTTPException(status_code=503, detail="İnternet bağlantısı yok veya API'ye ulaşılamıyor.")

# ISBN ile kitap silen endpoint
@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    if not library.find_book(isbn):
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    library.remove_book(isbn)
    return {"message": f"Kitap silindi: {isbn}"}
