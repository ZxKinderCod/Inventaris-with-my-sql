"""
main.py
Pintu masuk program Inventaris & Peminjaman Alat Laboratorium Fisika.

Cara pakai:
1. Nyalakan MySQL (dan Apache) di XAMPP.
2. Jalankan file ini (tombol Run di VS Code, atau: python main.py).

Alur: main.py -> gui.py -> tab (gui_*.py) -> file logika -> database.py -> MySQL

Sebelum jendela dibuka, program mengecek koneksi ke MySQL.
Jika gagal, tampil kotak pesan yang jelas (bukan traceback panjang).
"""

import tkinter as tk
from tkinter import messagebox

import mysql.connector

from database import koneksi
import gui


def tampil_error(pesan):
    """Menampilkan kotak pesan error tanpa membuka jendela kosong."""
    akar = tk.Tk()
    akar.withdraw()          # sembunyikan jendela utama Tk
    messagebox.showerror("Gagal Terhubung ke Database", pesan)
    akar.destroy()


def mysql_siap():
    """Mengecek koneksi ke MySQL. Return True jika berhasil."""
    try:
        sambungan = koneksi()
        sambungan.close()
        return True
    except mysql.connector.Error as galat:
        if galat.errno == 2003:
            # Server MySQL belum menyala
            tampil_error("Nyalakan MySQL di XAMPP dulu!")
        elif galat.errno == 1049:
            # Nama database di database.py tidak ada di server
            tampil_error("Database 'inventaris_laboratorium' tidak ditemukan.\n"
                         "Cek di phpMyAdmin dan nama di database.py.")
        else:
            tampil_error(f"Kesalahan database:\n{galat}")
        return False


# Pintu masuk program
if __name__ == "__main__":
    if mysql_siap():
        gui.mulai()