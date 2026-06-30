class SLLNode:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.next = None

class SingleLinkedList:
    def __init__(self):
        self.head = None

    def insert_book(self, book_id, title, author):
        """Menambahkan buku baru ke dalam inventaris perpustakaan (di akhir list)."""
        new_node = SLLNode(book_id, title, author)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def delete_book(self, book_id):
        """Menghapus buku berdasarkan ID Buku."""
        curr = self.head
        prev = None
        while curr:
            if curr.book_id == book_id:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                return True
            prev = prev
            prev = curr
            curr = curr.next
        return False

    def to_list(self):
        """Konversi linked list menjadi standard Python list untuk keperluan algoritma."""
        books = []
        curr = self.head
        while curr:
            books.append({"id": curr.book_id, "title": curr.title, "author": curr.author})
            curr = curr.next
        return books