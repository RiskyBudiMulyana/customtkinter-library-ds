# 📚 Digital Library Management System

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![GUI Framework](https://img.shields.io/badge/UI-CustomTkinter-darkblue)
![Architecture](https://img.shields.io/badge/Architecture-Modular%20OOP-orange)
![Database](https://img.shields.io/badge/Database-Flat%20File%20%28JSON%29-green)

Sistem Manajemen Perpustakaan Digital Modern adalah aplikasi desktop berbasis **Python** dan **CustomTkinter** yang dirancang untuk mengotomatisasi seluruh alur kerja operasional perpustakaan. Aplikasi ini mengintegrasikan antarmuka grafis modern dengan implementasi **struktur data murni (pure data structures)** yang dibangun dari nol tanpa pustaka eksternal tingkat tinggi maupun sistem database komersial.

---

## 🛠️ Batasan Teknis & Aturan Arsitektur

*   **Pure Python & Tanpa Database Eksternal:** Seluruh state aplikasi disimpan dalam bentuk berkas flat (`JSON`) dan dikelola langsung di memori internal saat aplikasi berjalan. Dilarang menggunakan SQLite, MySQL, atau ORM.
*   **Built From Scratch:** Struktur data direkayasa sendiri secara independen (melalui pembuatan class `Node` mandiri) tanpa menggunakan modul bawaan seperti `collections`.
*   **Modularitas & Paradigma OOP:** Memisahkan dengan jelas antara layer antarmuka (*frontend*), engine logika (*middleware*), dan struktur data (*backend*).
*   **Clean Code:** Setiap blok kode logis dilengkapi dengan komentar penjelas yang komprehensif.

---

## 🏗️ Implementasi Struktur Data

Untuk memastikan efisiensi performa dan pemahaman konseptual yang mendalam, aplikasi ini mengimplementasikan enam jenis struktur data murni:

| Struktur Data | Modul Backend | Fungsi / Peran dalam Sistem |
| :--- | :---: | :--- |
| **Single Linked List (SLL)** | `backend/sll.py` | Mengelola database inventaris utama (tambah, hapus, dan iterasi daftar buku). |
| **Queue (FIFO Queue)** | `backend/queue_fifo.py` | Mengatur antrean sirkulasi peminjaman buku anggota berdasarkan urutan masuk. |
| **Double Linked List (DLL)** | `backend/dll.py` | Pencatatan *logs* aktivitas sistem secara *real-time* dengan kapabilitas traversal maju-mundur. |
| **Circular Singly Linked List** | `backend/circular_lists.py` | Mengelola daftar buku favorit pengguna dalam bentuk korsel (*carousel*) berputar. |
| **Circular Doubly Linked List** | `backend/circular_lists.py` | Mengelola sistem rekomendasi buku dinamis yang dapat di-*loop* dua arah. |
| **Binary Search Tree (BST)** | `backend/bst.py` | Membangun indeks hierarki pohon berbasis ID Buku untuk mempercepat pencarian. |

---

## 📂 Struktur Direktori Proyek

Aplikasi ini disusun menggunakan pola arsitektur modular (*Separation of Concerns*):

```text
/
├── main.py                    # Entry point / titik masuk utama aplikasi
├── library_state.json         # File penyimpanan database lokal (JSON)
├── backend/                   # Layer Struktur Data Murni
│   ├── __init__.py
│   ├── sll.py                 # Implementasi Single Linked List
│   ├── dll.py                 # Implementasi Double Linked List
│   ├── queue_fifo.py          # Implementasi Antrean FIFO
│   ├── circular_lists.py      # Implementasi CSLL & CDLL
│   └── bst.py                 # Implementasi Binary Search Tree
├── middleware/                # Layer Engine Logika Bisnis
│   ├── __init__.py
│   ├── search_engine.py       # Algoritma Linear & Binary Search
│   └── sort_engine.py         # Algoritma Bubble & Quick Sort
└── frontend/                  # Layer Antarmuka Grafis (GUI)
    ├── __init__.py
    └── gui_app.py             # Antarmuka utama berbasis CustomTkinter
