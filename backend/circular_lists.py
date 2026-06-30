# --- CIRCULAR SINGLY LINKED LIST (CSLL) ---
class CSLLNode:
    def __init__(self, title):
        self.title = title
        self.next = None

class CircularSinglyLinkedList:
    def __init__(self):
        self.head = None

    def add_favorite(self, title):
        """Menambahkan judul buku ke daftar circular list favorit."""
        new_node = CSLLNode(title)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            return
        curr = self.head
        while curr.next != self.head:
            curr = curr.next
        curr.next = new_node
        new_node.next = self.head

    def to_list(self):
        """Mengonversi isi sirkular tunggal ke list python untuk visualisasi."""
        if not self.head:
            return []
        res = []
        curr = self.head
        while True:
            res.append(curr.title)
            curr = curr.next
            if curr == self.head:
                break
        return res


# --- CIRCULAR DOUBLE LINKED LIST (CDLL) ---
class CDLLNode:
    def __init__(self, title):
        self.title = title
        self.next = None
        self.prev = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_recommendation(self, title):
        """Menambahkan rekomendasi buku ke sistem carousel sirkular ganda."""
        new_node = CDLLNode(title)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            new_node.prev = self.head
            return
        tail = self.head.prev
        tail.next = new_node
        new_node.prev = tail
        new_node.next = self.head
        self.head.prev = new_node

    def to_list(self):
        if not self.head:
            return []
        res = []
        curr = self.head
        while True:
            res.append(curr.title)
            curr = curr.next
            if curr == self.head:
                break
        return res