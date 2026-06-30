class QueueNode:
    def __init__(self, borrower_name, book_id):
        self.borrower_name = borrower_name
        self.book_id = book_id
        self.next = None

class BorrowQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, borrower_name, book_id):
        """Menambahkan pemohon pinjaman baru ke dalam antrean (FIFO)."""
        new_node = QueueNode(borrower_name, book_id)
        if not self.rear:
            self.front = self.rear = new_node
            return
        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        """Memproses antrean paling depan."""
        if not self.front:
            return None
        temp = self.front
        self.front = self.front.next
        if not self.front:
            self.rear = None
        return temp

    def to_list(self):
        """Mendapatkan representasi daftar antrean aktif saat ini."""
        queue_list = []
        curr = self.front
        while curr:
            queue_list.append({"name": curr.borrower_name, "book_id": curr.book_id})
            curr = curr.next
        return queue_list