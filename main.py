import httpx
from models import Book, Library

# Ana uygulama fonksiyonu
def main():
    library = Library()  # Kütüphane nesnesi oluşturuluyor
    while True:
        print("\n--- Kütüphane Uygulaması ---")
        print("1. Kitap Ekle (ISBN ile)")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")
        secim = input("Seçiminiz: ")  # Kullanıcıdan seçim al

        if secim == "1":
            # Artık sadece ISBN soruluyor, diğer bilgiler API'den çekilecek
            isbn = input("Eklemek istediğiniz kitabın ISBN numarası: ")
            if library.find_book(isbn):
                print("Bu ISBN ile bir kitap zaten var!")
            else:
                # Open Library API'den kitap bilgisi çekiliyor
                url = f"https://openlibrary.org/isbn/{isbn}.json"
                try:
                    response = httpx.get(url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        title = data.get("title", "Başlık bulunamadı")
                        # Yazar bilgisini almak için authors alanı kontrol ediliyor
                        author = "Bilinmiyor"
                        if "authors" in data and data["authors"]:
                            # Yazarın adı için ek bir istek gerekebilir
                            author_key = data["authors"][0]["key"]
                            author_url = f"https://openlibrary.org{author_key}.json"
                            author_resp = httpx.get(author_url, timeout=10)
                            if author_resp.status_code == 200:
                                author = author_resp.json().get("name", "Bilinmiyor")
                        book = Book(title, author, isbn)
                        library.add_book(book)
                        print(f"Kitap eklendi: {book}")
                    elif response.status_code == 404:
                        print("Bu ISBN ile kitap bulunamadı.")
                    else:
                        print("API'den beklenmeyen bir cevap alındı.")
                except httpx.RequestError:
                    print("İnternet bağlantısı yok veya API'ye ulaşılamıyor.")

        elif secim == "2":
            # Kitap silme işlemi
            isbn = input("Silinecek kitabın ISBN'i: ")
            if library.find_book(isbn):
                library.remove_book(isbn)
                print("Kitap silindi.")
            else:
                print("Kitap bulunamadı.")

        elif secim == "3":
            # Tüm kitapları listele
            books = library.list_books()
            if not books:
                print("Kütüphane boş.")
            else:
                for book in books:
                    print(book)

        elif secim == "4":
            # Kitap arama işlemi
            isbn = input("Aranacak kitabın ISBN'i: ")
            book = library.find_book(isbn)
            if book:
                print(book)
            else:
                print("Kitap bulunamadı.")

        elif secim == "5":
            # Programdan çıkış
            print("Çıkılıyor...")
            break

        else:
            print("Geçersiz seçim! Lütfen 1-5 arasında bir değer girin.")

# Program doğrudan çalıştırıldığında ana fonksiyonu başlat
if __name__ == "__main__":
    main()
