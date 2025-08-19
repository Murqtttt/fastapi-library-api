import pytest
from models import Book, Library
import os
# Kitap ekleme ve arama fonksiyonunu test eder
def test_add_and_find_book(tmp_path):
    test_file = tmp_path / "test_library.json"  # Geçici test dosyası
    lib = Library(str(test_file))
    book = Book("Test", "Yazar", "1234")
    lib.add_book(book)
    # Eklenen kitabı bulabiliyor muyuz?
    assert lib.find_book("1234").title == "Test"

# Kitap silme fonksiyonunu test eder
def test_remove_book(tmp_path):
    test_file = tmp_path / "test_library.json"
    lib = Library(str(test_file))
    book = Book("Test", "Yazar", "1234")
    lib.add_book(book)
    lib.remove_book("1234")
    # Silinen kitap bulunamamalı
    assert lib.find_book("1234") is None

# Kitap listeleme fonksiyonunu test eder
def test_list_books(tmp_path):
    test_file = tmp_path / "test_library.json"
    lib = Library(str(test_file))
    lib.add_book(Book("A", "B", "1"))
    lib.add_book(Book("C", "D", "2"))
    books = lib.list_books()
    # İki kitap ekledik, ikisi de listede olmalı
    assert len(books) == 2
    assert books[0].title == "A"
    assert books[1].isbn == "2"
