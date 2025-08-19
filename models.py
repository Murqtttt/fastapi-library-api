import json
from typing import List, Optional

# Her bir kitabı temsil eden sınıf
class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title  # Kitabın adı
        self.author = author  # Yazar adı
        self.isbn = isbn  # ISBN numarası (benzersiz)

    def __str__(self):
        # Kitap bilgilerini okunaklı şekilde döndürür
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

# Kütüphaneyi ve kitap işlemlerini yöneten sınıf
class Library:
    def __init__(self, filename: str = "library.json"):
        self.filename = filename  # Kitapların kaydedileceği dosya adı
        self.books: List[Book] = []  # Kitap listesi
        self.load_books()  # Başlangıçta dosyadan kitapları yükle

    def add_book(self, book: Book):
        # Yeni bir kitap ekler ve kaydeder
        self.books.append(book)
        self.save_books()

    def remove_book(self, isbn: str):
        # ISBN numarasına göre kitabı siler ve kaydeder
        self.books = [b for b in self.books if b.isbn != isbn]
        self.save_books()

    def list_books(self) -> List[Book]:
        # Tüm kitapları döndürür
        return self.books

    def find_book(self, isbn: str) -> Optional[Book]:
        # ISBN ile kitap arar, bulursa Book nesnesini döndürür
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def load_books(self):
        # Uygulama başlarken kitapları dosyadan yükler
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = [Book(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            # Dosya yoksa veya bozuksa boş listeyle başla
            self.books = []

    def save_books(self):
        # Kitap listesini dosyaya kaydeder
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([book.__dict__ for book in self.books], f, ensure_ascii=False, indent=2)
