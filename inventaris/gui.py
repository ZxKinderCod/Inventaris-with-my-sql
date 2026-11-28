"""
gui.py
Jendela utama aplikasi Inventaris & Peminjaman Alat Laboratorium Fisika.

Isi jendela: satu ttk.Notebook dengan 5 tab, masing-masing dari file sendiri:
    1. Data Alat       -> gui_alat.TabAlat
    2. Data Mahasiswa  -> gui_mahasiswa.TabMahasiswa
    3. Peminjaman      -> gui_peminjaman.TabPeminjaman
    4. Pengembalian    -> gui_pengembalian.TabPengembalian
    5. Riwayat         -> gui_riwayat.TabRiwayat

Setiap kali tab berpindah, method segarkan() milik tab yang dibuka dipanggil,
sehingga datanya selalu terbaru (misalnya stok setelah ada peminjaman).

Alur: main.py -> gui.mulai() -> tab -> file logika -> database.py -> MySQL
Nyalakan MySQL di XAMPP sebelum menjalankan program.
"""

import tkinter as tk
from tkinter import ttk

from gui_alat import TabAlat
from gui_mahasiswa import TabMahasiswa
from gui_peminjaman import TabPeminjaman
from gui_pengembalian import TabPengembalian
from gui_riwayat import TabRiwayat


def mulai():
    """Membuat jendela utama beserta semua tab, lalu menjalankannya."""
    jendela = tk.Tk()
    jendela.title("Inventaris & Peminjaman Alat Laboratorium Fisika")
    jendela.geometry("1000x600")

    # Notebook = wadah tab
    notebook = ttk.Notebook(jendela)
    notebook.pack(fill="both", expand=True, padx=5, pady=5)

    # Buat tiap tab, lalu tambahkan ke notebook dengan judulnya
    daftar_tab = [
        (TabAlat(notebook), "Data Alat"),
        (TabMahasiswa(notebook), "Data Mahasiswa"),
        (TabPeminjaman(notebook), "Peminjaman"),
        (TabPengembalian(notebook), "Pengembalian"),
        (TabRiwayat(notebook), "Riwayat"),
    ]
    for tab, judul in daftar_tab:
        notebook.add(tab, text=judul)

    def saat_tab_berpindah(event):
        """Dipanggil setiap tab berpindah: muat ulang data tab yang dibuka."""
        tab_aktif = notebook.nametowidget(notebook.select())
        tab_aktif.segarkan()

    notebook.bind("<<NotebookTabChanged>>", saat_tab_berpindah)

    jendela.mainloop()


# Bagian ini hanya jalan jika file dijalankan langsung (untuk tes)
if __name__ == "__main__":
    mulai()