import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import customtkinter as ctk

# Import modules dari layer backend dan middleware murni
from backend.sll import SingleLinkedList
from backend.queue_fifo import BorrowQueue
from backend.dll import DoubleLinkedList
from backend.circular_lists import CircularSinglyLinkedList, CircularDoublyLinkedList
from backend.bst import BinarySearchTree
from middleware.search_engine import SearchEngine
from middleware.sort_engine import SortEngine

# Mengatur tema global CustomTkinter
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")  

class DigitalLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Manajemen Perpustakaan Digital")
        self.root.geometry("1150x780")
        
        # Inisialisasi Seluruh Mesin Struktur Data Murni
        self.inventory = SingleLinkedList()
        self.borrow_queue = BorrowQueue()
        self.activity_log = DoubleLinkedList()
        self.favorites = CircularSinglyLinkedList()
        self.recommendations = CircularDoublyLinkedList()
        self.tree_index = BinarySearchTree()

        # State tambahan untuk menampung data buku yang sedang dipinjam
        self.borrowed_books_list = [] 

        self.db_filename = "library_state.json"
        self.load_state_from_json()

        # Mempersiapkan Komponen Layout Antarmuka Modern
        self.setup_modern_gui()
        self.refresh_all_views()

    def save_state_to_json(self):
        state_data = {
            "inventory": self.inventory.to_list(),
            "queue": self.borrow_queue.to_list(),
            "logs": self.activity_log.to_list_forward(),
            "favorites": self.favorites.to_list(),
            "recommendations": self.recommendations.to_list(),
            "borrowed_books": self.borrowed_books_list
        }
        with open(self.db_filename, 'w') as f:
            json.dump(state_data, f, indent=4)

    def load_state_from_json(self):
        if os.path.exists(self.db_filename):
            try:
                with open(self.db_filename, 'r') as f:
                    data = json.load(f)
                    for item in data.get("inventory", []):
                        self.inventory.insert_book(item["id"], item["title"], item["author"])
                        self.tree_index.insert(item["id"], item["title"])
                    for item in data.get("queue", []):
                        self.borrow_queue.enqueue(item["name"], item["book_id"])
                    for log in data.get("logs", []):
                        self.activity_log.append_log(log)
                    for fav in data.get("favorites", []):
                        self.favorites.add_favorite(fav)
                    for rec in data.get("recommendations", []):
                        self.recommendations.add_recommendation(rec)
                    self.borrowed_books_list = data.get("borrowed_books", [])
            except Exception as e:
                print(f"Error loading state: {e}")

    def setup_modern_gui(self):
        # Membuat Main Container dengan CustomTkinter Tabview
        self.tabview = ctk.CTkTabview(self.root, width=1120, height=680, corner_radius=15)
        self.tabview.pack(padx=15, pady=(15, 10), fill="both", expand=True)

        # Menambahkan Tab Menu Utama
        self.tabview.add("1. Kelola Buku (SLL)")
        self.tabview.add("2. Sirkulasi (Queue & Return)")
        self.tabview.add("3. Pencarian (Search)")
        self.tabview.add("4. Pengurutan (Sort)")
        self.tabview.add("5. Indeks Pohon (BST)")
        self.tabview.add("6. Laporan & Favorit")

        # Konfigurasi gaya font Treeview bawaan
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", bg="#2a2d32", fg="white", fieldbg="#2a2d32", borderwidth=0, rowheight=32)
        style.map("Treeview", background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", bg="#1f6aa5", fg="white", borderwidth=0, font=('Helvetica', 10, 'bold'))

        # Membangun konten masing-masing tab
        self.build_inventory_tab()
        self.build_borrow_and_return_tab()
        self.build_search_tab()
        self.build_sort_tab()
        self.build_tree_tab()
        self.build_report_tab()

        # =================================================================
        # PANEL BOTTOM BAR (UNTUK TOMBOL RESET & KELUAR)
        # =================================================================
        bottom_frame = ctk.CTkFrame(self.root, height=50, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", padx=20, pady=(0, 15))

        # Tombol Reset Data Sistem (Aksen Merah)
        self.btn_reset_sistem = ctk.CTkButton(
            bottom_frame, text="⚠️ Reset Semua Data Sistem", 
            fg_color="#e74c3c", hover_color="#c0392b", font=("Helvetica", 12, "bold"),
            width=220, height=38,
            command=self.action_reset_all_data
        )
        self.btn_reset_sistem.pack(side="left", padx=5)

        # Tombol Keluar Aplikasi 
        self.btn_keluar_aplikasi = ctk.CTkButton(
            bottom_frame, text="🚪 Keluar Aplikasi", 
            fg_color="#7f8c8d", hover_color="#95a5a6", text_color="white", font=("Helvetica", 12, "bold"),
            width=160, height=38,
            command=self.action_exit_app
        )
        self.btn_keluar_aplikasi.pack(side="right", padx=5)

    def build_inventory_tab(self):
        tab = self.tabview.tab("1. Kelola Buku (SLL)")
        
        form_frame = ctk.CTkFrame(tab, width=360, corner_radius=12)
        form_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        lbl_title = ctk.CTkLabel(form_frame, text="FORM ENTRI DATA BUKU", font=("Helvetica", 14, "bold"), text_color="#3498db")
        lbl_title.pack(pady=20, padx=10)

        self.ent_inv_id = ctk.CTkEntry(form_frame, placeholder_text="ID Buku (Contoh: 101)", width=280)
        self.ent_inv_id.pack(pady=12, padx=20)

        self.ent_inv_title = ctk.CTkEntry(form_frame, placeholder_text="Judul Buku", width=280)
        self.ent_inv_title.pack(pady=12, padx=20)

        self.ent_inv_author = ctk.CTkEntry(form_frame, placeholder_text="Nama Penulis", width=280)
        self.ent_inv_author.pack(pady=12, padx=20)

        self.btn_simpan_buku_sll = ctk.CTkButton(
            form_frame, text="🟢 Simpan ke SLL & BST", 
            font=("Helvetica", 12, "bold"), fg_color="#2ecc71", hover_color="#27ae60", text_color="black",
            command=self.action_add_book
        )
        self.btn_simpan_buku_sll.pack(pady=25, padx=20, fill="x")

        table_frame = ctk.CTkFrame(tab, corner_radius=12)
        table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        lbl_table = ctk.CTkLabel(table_frame, text="DATABASE INVENTARIS (SINGLE LINKED LIST)", font=("Helvetica", 13, "bold"))
        lbl_table.pack(pady=15)

        self.tree_inv = ttk.Treeview(table_frame, columns=("ID", "Title", "Author"), show='headings')
        self.tree_inv.heading("ID", text="ID Buku")
        self.tree_inv.heading("Title", text="Judul Buku")
        self.tree_inv.heading("Author", text="Penulis / Kreator")
        self.tree_inv.pack(fill='both', expand=True, padx=15, pady=10)

        self.btn_hapus_buku_sll = ctk.CTkButton(
            table_frame, text="🔴 Hapus Buku Terpilih", 
            font=("Helvetica", 12, "bold"), fg_color="#e74c3c", hover_color="#c0392b",
            command=self.action_delete_book
        )
        self.btn_hapus_buku_sll.pack(pady=15, padx=15, anchor="e")

    def action_add_book(self):
        try:
            b_id = int(self.ent_inv_id.get())
            title = self.ent_inv_title.get().strip()
            author = self.ent_inv_author.get().strip()

            if not title or not author:
                messagebox.showerror("Error Input", "Seluruh kolom data wajib diisi!")
                return

            if any(b['id'] == b_id for b in self.inventory.to_list()):
                messagebox.showerror("Duplikasi ID", "ID Buku tersebut sudah terdaftar!")
                return

            self.inventory.insert_book(b_id, title, author)
            self.tree_index.insert(b_id, title)
            
            self.activity_log.append_log(f"Menambahkan buku baru: '{title}' [ID: {b_id}]")
            self.save_state_to_json()
            
            self.ent_inv_id.delete(0, tk.END)
            self.ent_inv_title.delete(0, tk.END)
            self.ent_inv_author.delete(0, tk.END)
            
            self.refresh_all_views()
            messagebox.showinfo("Sukses", f"Buku '{title}' berhasil disimpan!")
        except ValueError:
            messagebox.showerror("Gagal Validasi", "ID Buku wajib diisi dengan angka bulat!")

    def action_delete_book(self):
        selected_item = self.tree_inv.selection()
        if not selected_item:
            messagebox.showwarning("Pilih Data", "Pilih baris data pada tabel yang ingin dihapus terlebih dahulu!")
            return
        
        book_id = self.tree_inv.item(selected_item)['values'][0]
        title = self.tree_inv.item(selected_item)['values'][1]
        
        if self.inventory.delete_book(book_id):
            self.activity_log.append_log(f"Menghapus buku: '{title}' [ID: {book_id}]")
            self.save_state_to_json()
            self.refresh_all_views()
            messagebox.showinfo("Sukses", "Buku berhasil dihapus dari sistem.")
        else:
            messagebox.showerror("Error", "Gagal menghapus data buku dari struktur SLL.")

    def build_borrow_and_return_tab(self):
        tab = self.tabview.tab("2. Sirkulasi (Queue & Return)")
        
        tab.grid_columnconfigure(0, weight=1, uniform="sirkulasi")
        tab.grid_columnconfigure(1, weight=1, uniform="sirkulasi")
        tab.grid_rowconfigure(0, weight=1)

        # =================================================================
        # PANEL KIRI: ANTRIAN PEMINJAMAN (QUEUE FIFO)
        # =================================================================
        queue_panel = ctk.CTkFrame(tab, corner_radius=12)
        queue_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        lbl_q_title = ctk.CTkLabel(queue_panel, text="📥 ANTRIAN PEMINJAMAN BUKU (FIFO)", font=("Helvetica", 13, "bold"), text_color="#3498db")
        lbl_q_title.pack(pady=10)

        input_q_frame = ctk.CTkFrame(queue_panel, fg_color="transparent")
        input_q_frame.pack(fill="x", padx=15, pady=5)

        self.ent_borrower = ctk.CTkEntry(input_q_frame, placeholder_text="Nama Lengkap Anggota", width=200)
        self.ent_borrower.pack(side="left", padx=5, expand=True, fill="x")

        self.ent_borrow_id = ctk.CTkEntry(input_q_frame, placeholder_text="ID Buku", width=100)
        self.ent_borrow_id.pack(side="left", padx=5)

        self.btn_masuk_antrean_queue = ctk.CTkButton(
            input_q_frame, text="TAMBAH", font=("Helvetica", 11, "bold"), width=80,
            command=self.action_enqueue
        )
        self.btn_masuk_antrean_queue.pack(side="left", padx=5)

        self.tree_queue = ttk.Treeview(queue_panel, columns=("No", "Nama", "BookID"), show='headings', height=10)
        self.tree_queue.heading("No", text="No")
        self.tree_queue.heading("Nama", text="Nama Anggota")
        self.tree_queue.heading("BookID", text="ID Buku")
        self.tree_queue.column("No", width=40, anchor="center")
        self.tree_queue.pack(fill='both', expand=True, padx=15, pady=10)

        self.btn_proses_antrean_queue = ctk.CTkButton(
            queue_panel, text="✅ Proses Pinjam Terdepan (Dequeue)", 
            fg_color="#2ecc71", hover_color="#27ae60", text_color="black", font=("Helvetica", 12, "bold"),
            command=self.action_dequeue
        )
        self.btn_proses_antrean_queue.pack(pady=10, padx=15, fill="x")

        # =================================================================
        # PANEL KANAN: MANAJEMEN PENGEMBALIAN BUKU
        # =================================================================
        return_panel = ctk.CTkFrame(tab, corner_radius=12)
        return_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        lbl_r_title = ctk.CTkLabel(return_panel, text="📤 DAFTAR BUKU YANG SEDANG DIPINJAM", font=("Helvetica", 13, "bold"), text_color="#e67e22")
        lbl_r_title.pack(pady=10)

        self.tree_return = ttk.Treeview(return_panel, columns=("Nama", "BookID", "Judul"), show='headings', height=10)
        self.tree_return.heading("Nama", text="Nama Peminjam")
        self.tree_return.heading("BookID", text="ID Buku")
        self.tree_return.heading("Judul", text="Judul Buku")
        self.tree_return.pack(fill='both', expand=True, padx=15, pady=10)

        self.btn_kembalikan_buku = ctk.CTkButton(
            return_panel, text="↩️ Kembalikan Buku Terpilih", 
            fg_color="#e67e22", hover_color="#d35400", font=("Helvetica", 12, "bold"),
            command=self.action_return_book
        )
        self.btn_kembalikan_buku.pack(pady=10, padx=15, fill="x")

    def action_enqueue(self):
        name = self.ent_borrower.get().strip()
        try:
            b_id = int(self.ent_borrow_id.get())
            if not name:
                messagebox.showerror("Error", "Nama pembuat antrean wajib diisi!")
                return
            
            books = self.inventory.to_list()
            book_data = next((b for b in books if b['id'] == b_id), None)
            if not book_data:
                messagebox.showerror("Buku Absen", "ID Buku tidak terdaftar di gudang utama SLL!")
                return

            if any(b['book_id'] == b_id for b in self.borrowed_books_list):
                messagebox.showwarning("Sedang Dipinjam", "Buku tersebut saat ini sedang dibawa anggota lain!")
                return

            self.borrow_queue.enqueue(name, b_id)
            self.activity_log.append_log(f"Anggota '{name}' mengantre untuk meminjam Buku ID: {b_id}")
            self.save_state_to_json()
            
            self.ent_borrower.delete(0, tk.END)
            self.ent_borrow_id.delete(0, tk.END)
            self.refresh_all_views()
        except ValueError:
            messagebox.showerror("Validasi", "ID Buku harus diisi dalam bentuk angka murni!")

    def action_dequeue(self):
        processed = self.borrow_queue.dequeue()
        if not processed:
            messagebox.showwarning("Kosong", "Tidak ada antrean aktif saat ini.")
            return
        
        books = self.inventory.to_list()
        book_data = next((b for b in books if b['id'] == processed.book_id), {"title": "Unknown Title"})

        self.borrowed_books_list.append({
            "borrower": processed.borrower_name,
            "book_id": processed.book_id,
            "title": book_data['title']
        })

        self.activity_log.append_log(f"PEMINJAMAN DISETUJUI: {processed.borrower_name} resmi membawa Buku ID: {processed.book_id}")
        self.save_state_to_json()
        self.refresh_all_views()
        messagebox.showinfo("Berhasil", f"Buku Berhasil Dipinjam oleh {processed.borrower_name}!")

    def action_return_book(self):
        selected_item = self.tree_return.selection()
        if not selected_item:
            messagebox.showwarning("Pilih Data", "Silakan pilih baris buku terpinjam yang ingin dikembalikan!")
            return
        
        values = self.tree_return.item(selected_item)['values']
        borrower_name = values[0]
        book_id = int(values[1])
        book_title = values[2]

        self.borrowed_books_list = [b for b in self.borrowed_books_list if not (b['book_id'] == book_id and b['borrower'] == borrower_name)]

        self.activity_log.append_log(f"PENGEMBALIAN SELESAI: Buku '{book_title}' [ID: {book_id}] dikembalikan oleh {borrower_name}")
        self.save_state_to_json()
        self.refresh_all_views()
        messagebox.showinfo("Sukses", f"Buku '{book_title}' telah sukses dikembalikan ke sistem perpustakaan!")

    def build_search_tab(self):
        tab = self.tabview.tab("3. Pencarian (Search)")

        ctrl_frame = ctk.CTkFrame(tab, corner_radius=12)
        ctrl_frame.pack(fill="x", padx=15, pady=15)

        lbl_sec = ctk.CTkLabel(ctrl_frame, text="PANEL INSTRUMEN MESIN PENCARIAN (SEARCH ENGINE)", font=("Helvetica", 13, "bold"), text_color="#3498db")
        lbl_sec.pack(pady=12)

        row1 = ctk.CTkFrame(ctrl_frame, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=8)
        self.ent_src_title = ctk.CTkEntry(row1, placeholder_text="Ketik Kata Kunci Judul Buku...", width=550)
        self.ent_src_title.pack(side="left", padx=10)
        
        self.btn_cari_linear = ctk.CTkButton(
            row1, text="🔍 Linear Search O(n)", width=220, font=("Helvetica", 11, "bold"),
            command=self.action_linear_search
        )
        self.btn_cari_linear.pack(side="right", padx=10)

        row2 = ctk.CTkFrame(ctrl_frame, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=8)
        self.ent_src_id = ctk.CTkEntry(row2, placeholder_text="Ketik Angka ID Buku Spesifik...", width=550)
        self.ent_src_id.pack(side="left", padx=10)
        
        self.btn_cari_biner = ctk.CTkButton(
            row2, text="⚡ Binary Search O(log n)", width=220, font=("Helvetica", 11, "bold"),
            fg_color="#9b59b6", hover_color="#8e44ad",
            command=self.action_binary_search
        )
        self.btn_cari_biner.pack(side="right", padx=10)

        res_frame = ctk.CTkFrame(tab, corner_radius=12)
        res_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.txt_search_res = ctk.CTkTextbox(res_frame, font=("Courier New", 13), fg_color="#1e1e24", text_color="#3498db")
        self.txt_search_res.pack(fill="both", expand=True, padx=15, pady=15)

    def action_linear_search(self):
        target = self.ent_src_title.get().strip()
        if not target:
            messagebox.showwarning("Input Kosong", "Silakan masukkan kata kunci judul terlebih dahulu!")
            return
        
        books = self.inventory.to_list()
        results = SearchEngine.linear_search(books, target)
        
        self.txt_search_res.delete("1.0", tk.END)
        self.txt_search_res.insert(tk.END, f"=== LOG HASIL LINEAR SEARCH O(n) ===\nKata Kunci: '{target}'\n\n")
        if not results:
            self.txt_search_res.insert(tk.END, "Status: Buku tidak ditemukan di dalam memori internal.")
        else:
            for idx, res in results:
                self.txt_search_res.insert(tk.END, f"[Iterasi Langkah ke-{idx+1}] -> Match ditemukan! ID: {res['id']} | Judul: {res['title']} | Penulis: {res['author']}\n")

    def action_binary_search(self):
        try:
            target_id = int(self.ent_src_id.get())
            books = self.inventory.to_list()
            
            sorted_books = SortEngine.quick_sort(books)
            result = SearchEngine.binary_search(sorted_books, target_id)
            
            self.txt_search_res.delete("1.0", tk.END)
            self.txt_search_res.insert(tk.END, f"=== LOG HASIL BINARY SEARCH O(log n) ===\nTarget ID: {target_id}\n\n")
            if result:
                self.txt_search_res.insert(tk.END, f"STATUS: BERHASIL DITEMUKAN SECARA LOGARITMIK!\n👉 ID Buku  : {result['id']}\n👉 Judul    : {result['title']}\n👉 Penulis  : {result['author']}\n")
            else:
                self.txt_search_res.insert(tk.END, f"Status: Buku dengan ID {target_id} TIDAK ada di database.")
        except ValueError:
            messagebox.showerror("Error Tipe Data", "Pencarian Biner membutuhkan input ID berupa angka murni!")

    def build_sort_tab(self):
        tab = self.tabview.tab("4. Pengurutan (Sort)")

        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=15)

        self.btn_urut_bubble_title = ctk.CTkButton(
            btn_frame, text="🔤 Urut Judul (Bubble Sort - O(n²))", 
            fg_color="#e67e22", hover_color="#d35400", font=("Helvetica", 11, "bold"),
            command=self.action_bubble_sort
        )
        self.btn_urut_bubble_title.pack(side="left", padx=15, pady=5, expand=True, fill="x")

        self.btn_urut_quick_id = ctk.CTkButton(
            btn_frame, text="🔢 Urut ID Buku (Quick Sort - O(n log n))", 
            fg_color="#d35400", hover_color="#e67e22", font=("Helvetica", 11, "bold"),
            command=self.action_quick_sort
        )
        self.btn_urut_quick_id.pack(side="right", padx=15, pady=5, expand=True, fill="x")

        table_frame = ctk.CTkFrame(tab, corner_radius=12)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.tree_sort = ttk.Treeview(table_frame, columns=("ID", "Title", "Author"), show='headings')
        self.tree_sort.heading("ID", text="ID Buku")
        self.tree_sort.heading("Title", text="Judul Terurut")
        self.tree_sort.heading("Author", text="Penulis")
        self.tree_sort.pack(fill='both', expand=True, padx=15, pady=15)

    def action_bubble_sort(self):
        books = self.inventory.to_list()
        sorted_books = SortEngine.bubble_sort(books, key='title')
        self.render_sorted_tree(sorted_books)
        messagebox.showinfo("Sort Sukses", "Tabel berhasil diurutkan berdasarkan alfabetis Judul Buku via Bubble Sort!")

    def action_quick_sort(self):
        books = self.inventory.to_list()
        sorted_books = SortEngine.quick_sort(books)
        self.render_sorted_tree(sorted_books)
        messagebox.showinfo("Sort Sukses", "Tabel berhasil diurutkan berdasarkan ID via Quick Sort!")

    def render_sorted_tree(self, sorted_list):
        for row in self.tree_sort.get_children():
            self.tree_sort.delete(row)
        for b in sorted_list:
            self.tree_sort.insert("", tk.END, values=(b['id'], b['title'], b['author']))

    # =================================================================
    # TAB 5 - INDEKS POHON (BST HIERARCHY CARDS)
    # =================================================================
    def build_tree_tab(self):
        tab = self.tabview.tab("5. Indeks Pohon (BST)")

        main_frame = ctk.CTkFrame(tab, corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        lbl_tree_title = ctk.CTkLabel(
            main_frame, text="🌿 VISUALISASI HIERARKI INDEKS BINER (BINARY SEARCH TREE)", 
            font=("Helvetica", 13, "bold"), text_color="#2ecc71"
        )
        lbl_tree_title.pack(pady=(15, 5), padx=15, anchor="w")
        
        lbl_tree_desc = ctk.CTkLabel(
            main_frame, text="Menampilkan struktur indeks memori non-linear berdasarkan ID Buku menggunakan metode Pre-order Traversal untuk melihat struktur percabangan Node.", 
            font=("Helvetica", 11), text_color="#7f8c8d"
        )
        lbl_tree_desc.pack(pady=(0, 10), padx=15, anchor="w")

        self.panel_tree_canvas = ctk.CTkScrollableFrame(
            main_frame, fg_color="#111215", corner_radius=10, border_width=1, border_color="#27ae60"
        )
        self.panel_tree_canvas.pack(fill="both", expand=True, padx=15, pady=10)

        self.btn_refresh_indeks_bst = ctk.CTkButton(
            main_frame, text="⚡ Sinkronisasi & Rekonstruksi Pohon BST", 
            font=("Helvetica", 12, "bold"), fg_color="#2ecc71", hover_color="#27ae60", text_color="black",
            height=40,
            command=self.refresh_tree_tab_content
        )
        self.btn_refresh_indeks_bst.pack(pady=15, padx=15, fill="x")

    def refresh_tree_tab_content(self):
        # 1. Bangun ulang objek pohon indeks dari data inventory SLL terbaru
        self.tree_index = BinarySearchTree()
        for b in self.inventory.to_list():
            self.tree_index.insert(b['id'], b['title'])
            
        # 2. Bersihkan seluruh widget visual lama di dalam canvas
        for widget in self.panel_tree_canvas.winfo_children():
            widget.destroy()

        # 3. Fungsi Helper Rekursif untuk merender struktur hierarki pohon (Pre-order Style)
        def render_node_visual(node, indent="", is_last=True, level=0):
            if node is None:
                return
            
            # Membuat container horizontal untuk satu baris node
            row_frame = ctk.CTkFrame(self.panel_tree_canvas, fg_color="transparent")
            row_frame.pack(fill="x", anchor="w", padx=10, pady=2)
            
            # Menentukan karakter garis pemandu silsilah cabang pohon
            marker = "└── " if is_last else "├── "
            prefix = indent + marker if level > 0 else "👑 ROOT ➔ "
            
            # Label Garis Pemandu Hubungan Pointer (Parent-Child Linkage)
            lbl_prefix = ctk.CTkLabel(
                row_frame, text=prefix, font=("Consolas", 13, "bold"), 
                text_color="#27ae60" if level > 0 else "#f1c40f"
            )
            lbl_prefix.pack(side="left")
            
            # Card Badge Premium untuk membungkus data Node itu sendiri
            card_color = "#1e272e" if level > 0 else "#2c3a47"
            border_color = "#2ecc71" if level > 0 else "#f1c40f"
            
            node_card = ctk.CTkFrame(
                row_frame, fg_color=card_color, corner_radius=6, 
                border_width=1, border_color=border_color
            )
            node_card.pack(side="left", padx=2)
            
            # =================================================================
            # FIX BARIS 546: MENYESUAIKAN ATRIBUT NODE AGAR ANTI-CRASH (Berdasarkan image_627d59.png)
            # Menggunakan atribut dinamis bawaan (jika .key gagal, fallback ke .id)
            # =================================================================
            n_id = getattr(node, 'id', getattr(node, 'key', 'N/A'))
            n_title = getattr(node, 'title', getattr(node, 'value', 'N/A'))
            
            node_text = f"ID: {n_id} | {n_title}"
            lbl_node = ctk.CTkLabel(
                node_card, text=node_text, font=("Helvetica", 11, "bold"), 
                text_color="#ffffff", padx=12, pady=4
            )
            lbl_node.pack()
            
            # Hitung indentasi masa depan untuk anak-anak cabangnya
            next_indent = indent + ("    " if is_last else "│   ")
            
            # Ambil anak cabang (Children Node)
            children = []
            if node.left:
                children.append((node.left, False))
            if node.right:
                children.append((node.right, True))
            
            # Koreksi flag anak terakhir jika hanya ada satu anak murni
            if len(children) == 1:
                children[0] = (children[0][0], True)
                
            # Lakukan pemanggilan rekursif untuk anak kiri dan kanan
            for child_node, child_is_last in children:
                render_node_visual(child_node, next_indent, child_is_last, level + 1)

        # 4. Mulai proses rendering dari puncak tertinggi pohon (Root Node)
        if self.tree_index.root is None:
            lbl_empty = ctk.CTkLabel(
                self.panel_tree_canvas, 
                text=" 🌲 Pohon indeks belum terbentuk. Silakan masukkan data buku terlebih dahulu di Tab 1.", 
                font=("Helvetica", 12, "italic"), text_color="#7f8c8d"
            )
            lbl_empty.pack(pady=40, padx=20)
        else:
            render_node_visual(self.tree_index.root, indent="", is_last=True, level=0)

    # =================================================================
    # TAB 6 - LAPORAN & FAVORIT (HORIZONTAL CHIPS CAROUSEL)
    # =================================================================
    def build_report_tab(self):
        tab = self.tabview.tab("6. Laporan & Favorit")

        tab.grid_columnconfigure(0, weight=1, uniform="group1")
        tab.grid_columnconfigure(1, weight=1, uniform="group1")
        tab.grid_rowconfigure(0, weight=1)

        # KOLOM KIRI: PANEL MANAJEMEN KONDISIONAL LIST (CSLL & CDLL)
        left_panel = ctk.CTkFrame(tab, corner_radius=12)
        left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        lbl_left_title = ctk.CTkLabel(
            left_panel, 
            text="⚙️ KONTROL DATA CAROUSEL & REKOMENDASI", 
            font=("Helvetica", 13, "bold"), 
            text_color="#3498db"
        )
        lbl_left_title.pack(pady=15, padx=15, anchor="w")

        lbl_input_hint = ctk.CTkLabel(left_panel, text="Masukkan Judul Buku Target:", font=("Helvetica", 11, "bold"))
        lbl_input_hint.pack(padx=20, anchor="w")
        
        self.ent_fav_title = ctk.CTkEntry(left_panel, placeholder_text="Contoh: Belajar Golang dari Nol", height=40)
        self.ent_fav_title.pack(fill="x", padx=20, pady=(5, 15))

        btn_action_container = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_action_container.pack(fill="x", padx=20, pady=5)
        btn_action_container.grid_columnconfigure(0, weight=1)
        btn_action_container.grid_columnconfigure(1, weight=1)

        self.btn_tambah_favorit_csll = ctk.CTkButton(
            btn_action_container, text="❤️ Sematkan Favorit", 
            fg_color="#e74c3c", hover_color="#c0392b", font=("Helvetica", 12, "bold"),
            height=38,
            command=self.action_add_fav
        )
        self.btn_tambah_favorit_csll.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.btn_tambah_rekomendasi_cdll = ctk.CTkButton(
            btn_action_container, text="⭐ Jadikan Rekomendasi", 
            fg_color="#f1c40f", hover_color="#f39c12", text_color="black", font=("Helvetica", 12, "bold"),
            height=38,
            command=self.action_add_rec
        )
        self.btn_tambah_rekomendasi_cdll.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        separator = ctk.CTkFrame(left_panel, height=2, fg_color="#34495e")
        separator.pack(fill="x", padx=20, pady=20)

        lbl_preview_title = ctk.CTkLabel(
            left_panel, text="📊 VISUALISASI LIVE STRUKTUR DATA MELINGKAR", 
            font=("Helvetica", 12, "bold"), text_color="#a4b0be"
        )
        lbl_preview_title.pack(padx=20, anchor="w")

        # --- CAROUSEL FAVORIT (CSLL) PANEL ---
        lbl_csll_tag = ctk.CTkLabel(left_panel, text="📌 Circular Singly Linked List (Favorit)", font=("Helvetica", 11, "bold"), text_color="#e74c3c")
        lbl_csll_tag.pack(padx=20, pady=(15, 2), anchor="w")
        
        self.panel_csll_cards = ctk.CTkScrollableFrame(left_panel, height=75, fg_color="#1e272e", corner_radius=10, orientation="horizontal")
        self.panel_csll_cards.pack(fill="x", padx=20, pady=5)

        # --- CAROUSEL REKOMENDASI (CDLL) PANEL ---
        lbl_cdll_tag = ctk.CTkLabel(left_panel, text="✨ Circular Doubly Linked List (Rekomendasi Carousel)", font=("Helvetica", 11, "bold"), text_color="#f1c40f")
        lbl_cdll_tag.pack(padx=20, pady=(15, 2), anchor="w")
        
        self.panel_cdll_cards = ctk.CTkScrollableFrame(left_panel, height=75, fg_color="#1e272e", corner_radius=10, orientation="horizontal")
        self.panel_cdll_cards.pack(fill="x", padx=20, pady=5)

        # KOLOM KANAN: LIVE SYSTEM LOG TERMINAL (DOUBLE LINKED LIST)
        right_panel = ctk.CTkFrame(tab, corner_radius=12)
        right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        lbl_right_title = ctk.CTkLabel(
            right_panel, 
            text="📋 LIVE SYSTEM LOGS (DOUBLE LINKED LIST)", 
            font=("Helvetica", 13, "bold"), 
            text_color="#2ecc71"
        )
        lbl_right_title.pack(pady=15, padx=15, anchor="w")

        self.txt_reports = ctk.CTkTextbox(
            right_panel, 
            font=("Consolas", 11), 
            fg_color="#151518", 
            text_color="#00ff00",
            border_width=1,
            border_color="#27ae60"
        )
        self.txt_reports.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def action_add_fav(self):
        t = self.ent_fav_title.get().strip()
        if t:
            self.favorites.add_favorite(t)
            self.activity_log.append_log(f"Menandai buku '{t}' sebagai Favorit (CSLL)")
            self.save_state_to_json()
            self.ent_fav_title.delete(0, tk.END)
            self.refresh_all_views()
        else:
            messagebox.showwarning("Input Kosong", "Judul buku favorit tidak boleh kosong!")

    def action_add_rec(self):
        t = self.ent_fav_title.get().strip()
        if t:
            self.recommendations.add_recommendation(t)
            self.activity_log.append_log(f"Menambahkan rekomendasi sistem: '{t}' (CDLL)")
            self.save_state_to_json()
            self.ent_fav_title.delete(0, tk.END)
            self.refresh_all_views()
        else:
            messagebox.showwarning("Input Kosong", "Judul buku rekomendasi tidak boleh kosong!")

    def action_reset_all_data(self):
        confirm = messagebox.askyesno(
            "Konfirmasi Reset", 
            "Apakah Anda yakin ingin menghapus SELURUH data buku, antrean sirkulasi, log, dan rekomendasi? Tindakan ini tidak bisa dibatalkan."
        )
        if confirm:
            self.inventory = SingleLinkedList()
            self.borrow_queue = BorrowQueue()
            self.activity_log = DoubleLinkedList()
            self.favorites = CircularSinglyLinkedList()
            self.recommendations = CircularDoublyLinkedList()
            self.tree_index = BinarySearchTree()
            self.borrowed_books_list = []

            if os.path.exists(self.db_filename):
                try:
                    os.remove(self.db_filename)
                except Exception as e:
                    print(f"Gagal menghapus file state: {e}")

            self.activity_log.append_log("SISTEM BERHASIL DI-RESET: Database memori internal kembali bersih.")
            self.refresh_all_views()
            messagebox.showinfo("Reset Sukses", "Seluruh basis data sistem perpustakaan telah dibersihkan!")

    def action_exit_app(self):
        confirm = messagebox.askyesno("Konfirmasi Keluar", "Apakah Anda yakin ingin menutup aplikasi?")
        if confirm:
            self.save_state_to_json()
            self.root.quit()

    def refresh_all_views(self):
        # Refresh Tabel SLL
        for row in self.tree_inv.get_children():
            self.tree_inv.delete(row)
        for b in self.inventory.to_list():
            self.tree_inv.insert("", tk.END, values=(b['id'], b['title'], b['author']))

        # Refresh Tabel Antrean Queue
        for row in self.tree_queue.get_children():
            self.tree_queue.delete(row)
        for idx, q in enumerate(self.borrow_queue.to_list()):
            self.tree_queue.insert("", tk.END, values=(idx + 1, q['name'], q['book_id']))

        # Refresh Tabel Pengembalian Buku Terpinjam
        for row in self.tree_return.get_children():
            self.tree_return.delete(row)
        for rb in self.borrowed_books_list:
            self.tree_return.insert("", tk.END, values=(rb['borrower'], rb['book_id'], rb['title']))

        # =================================================================
        # CSLL CAROUSEL VISUALIZATION
        # =================================================================
        for widget in self.panel_csll_cards.winfo_children():
            widget.destroy()

        list_fav = self.favorites.to_list()
        if not list_fav:
            lbl_empty = ctk.CTkLabel(self.panel_csll_cards, text=" ⭕ Belum ada buku yang disematkan di favorit.", font=("Helvetica", 11, "italic"), text_color="#7f8c8d")
            lbl_empty.pack(pady=20, padx=10)
        else:
            for idx, fav_title in enumerate(list_fav):
                card = ctk.CTkFrame(self.panel_csll_cards, fg_color="#2c3a47", corner_radius=6, border_width=1, border_color="#e74c3c")
                card.pack(side="left", padx=4, pady=10)
                
                lbl_text = ctk.CTkLabel(card, text=f"❤️ {fav_title}", font=("Helvetica", 11, "bold"), text_color="#ffffff", padx=10, pady=5)
                lbl_text.pack()

                pointer_txt = "➔ (HEAD)" if idx == len(list_fav) - 1 else "➔"
                lbl_ptr = ctk.CTkLabel(self.panel_csll_cards, text=pointer_txt, font=("Consolas", 12, "bold"), text_color="#e74c3c", padx=5)
                lbl_ptr.pack(side="left")

        # =================================================================
        # CDLL CAROUSEL VISUALIZATION
        # =================================================================
        for widget in self.panel_cdll_cards.winfo_children():
            widget.destroy()

        list_rec = self.recommendations.to_list()
        if not list_rec:
            lbl_empty_rec = ctk.CTkLabel(self.panel_cdll_cards, text=" ⭕ Antrean rekomendasi sistem masih kosong.", font=("Helvetica", 11, "italic"), text_color="#7f8c8d")
            lbl_empty_rec.pack(pady=20, padx=10)
        else:
            for idx, rec_title in enumerate(list_rec):
                card = ctk.CTkFrame(self.panel_cdll_cards, fg_color="#2f3640", corner_radius=6, border_width=1, border_color="#f1c40f")
                card.pack(side="left", padx=4, pady=10)
                
                lbl_text = ctk.CTkLabel(card, text=f"⭐ {rec_title}", font=("Helvetica", 11, "bold"), text_color="#f5cd79", padx=10, pady=5)
                lbl_text.pack()

                pointer_txt = "⇄ (LOOP)" if idx == len(list_rec) - 1 else "⇄"
                lbl_ptr = ctk.CTkLabel(self.panel_cdll_cards, text=pointer_txt, font=("Consolas", 12, "bold"), text_color="#f1c40f", padx=5)
                lbl_ptr.pack(side="left")

        # Refresh DLL Console Logs
        self.txt_reports.delete("1.0", tk.END)
        self.txt_reports.insert(tk.END, f"=== KONSOL MONITORING REALTIME SYSTEM LOG (DLL) ===\n")
        self.txt_reports.insert(tk.END, f"Status Basis Data: Terhubung (Memory Internal Teramankan)\n")
        self.txt_reports.insert(tk.END, f"Jumlah Total Buku Saat Ini: {len(self.inventory.to_list())} Unit\n")
        self.txt_reports.insert(tk.END, f"----------------------------------------------------\n\n")
        
        logs = self.activity_log.to_list_forward()
        if not logs:
            self.txt_reports.insert(tk.END, " > [SYSTEM] Menunggu interaksi atau input dari user...")
        else:
            for log in logs:
                self.txt_reports.insert(tk.END, f" 🟢 [LOG] {log}\n")

        # Otomatis memperbarui visualisasi berundak pohon BST pada Tab 5
        self.refresh_tree_tab_content()