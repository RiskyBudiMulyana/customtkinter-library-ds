class DLLNode:
    def __init__(self, log_text):
        self.log_text = log_text
        self.next = None
        self.prev = None

class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append_log(self, log_text):
        """Mencatat riwayat aktivitas baru di akhir list."""
        new_node = DLLNode(log_text)
        if not self.head:
            self.head = self.tail = new_node
            return
        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def to_list_forward(self):
        """Mengambil log urutan waktu terlama ke terbaru."""
        logs = []
        curr = self.head
        while curr:
            logs.append(curr.log_text)
            curr = curr.next
        return logs