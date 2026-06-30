class BSTNode:
    def __init__(self, book_id, title):
        self.book_id = book_id
        self.title = title
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, book_id, title):
        """Menyisipkan indeks ID Buku ke struktur pohon biner secara terurut."""
        self.root = self._insert_recursive(self.root, book_id, title)

    def _insert_recursive(self, node, book_id, title):
        if not node:
            return BSTNode(book_id, title)
        if book_id < node.book_id:
            node.left = self._insert_recursive(node.left, book_id, title)
        elif book_id > node.book_id:
            node.right = self._insert_recursive(node.right, book_id, title)
        return node

    def get_inorder(self):
        """Menghasilkan representasi Tree secara In-Order Traversal."""
        res = []
        self._inorder_recursive(self.root, res)
        return res

    def _inorder_recursive(self, node, res):
        if node:
            self._inorder_recursive(node.left, res)
            res.append(f"ID: {node.book_id} -> {node.title}")
            self._inorder_recursive(node.right, res)