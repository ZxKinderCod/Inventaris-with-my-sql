"""
gui_peminjaman.py
-----------------
Fungsi: tampilan (GUI) untuk tab "Peminjaman".

Satu tab ini MENGGABUNGKAN beberapa fitur sekaligus:
  - CEK NIM    : nama mahasiswa tampil otomatis saat NIM diketik
                 -> memakai daftar_mahasiswa() dari daftar.py
  - PILIH ALAT : tabel alat yang boleh dipinjam (kondisi baik, stok ada) + kolom cari
                 -> memakai daftar_alat_tersedia() dari daftar.py
  - KERANJANG  : menampung beberapa alat beserta jumlahnya sebelum dipinjam
                 (disimpan sementara di program, belum masuk database)
  - PINJAM     : tombol "Pinjam Semua" -> memakai pinjam() dari peminjaman.py,
                 semua alat di keranjang dipinjam dalam SATU proses

Contoh: meminjam 2 resistor, 1 multimeter, dan 1 project board sekali proses.

File ini hanya mengurus TAMPILAN. Semua aturan (NIM valid, alat rusak, stok
cukup) diperiksa oleh pinjam() di peminjaman.py.
Kelas TabPeminjaman dipasang ke jendela utama oleh gui.py. Method segarkan()
dipanggil gui.py saat tab dibuka, supaya stok yang tampil selalu terbaru.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from daftar import daftar_alat_tersedia, daftar_mahasiswa
from peminjaman import pinjam
from tambah_mahasiswa import PANJANG_NIM


class TabPeminjaman(ttk.Frame):
    """Tab Peminjaman: data peminjam, pilihan alat, keranjang, tombol pinjam."""

    def __init__(self, induk):
        super().__init__(induk)

        # Variabel untuk menyimpan isi kotak isian
        self.var_nim = tk.StringVar()
        self.var_cari = tk.StringVar()
        self.var_jumlah = tk.StringVar(value="1")

        # Keranjang disimpan sementara di sini, bentuknya {kode_alat: [nama, jumlah]}
        self.keranjang = {}

        # Susun tampilan dari atas ke bawah, lalu isi tabel alat
        self.buat_data_peminjam()
        self.buat_panel_tengah()
        self.buat_tombol_bawah()
        self.muat_alat()

    # ------------------------------------------------------------
    # BAGIAN TAMPILAN
    # ------------------------------------------------------------
    def buat_data_peminjam(self):
        """Membuat kotak NIM dan label nama mahasiswa."""
        bingkai = ttk.LabelFrame(self, text="Data Peminjam")
        bingkai.pack(fill="x", padx=10, pady=(10, 5))

        ttk.Label(bingkai, text="NIM / NPM").grid(row=0, column=0, padx=8, pady=8)
        kotak_nim = ttk.Entry(bingkai, textvariable=self.var_nim, width=18)
        kotak_nim.grid(row=0, column=1, padx=8)
        kotak_nim.bind("<KeyRelease>", lambda e: self.cek_nim())

        # Label ini terisi nama mahasiswa saat NIM yang diketik sudah lengkap
        self.label_nama = ttk.Label(bingkai, text="", font=("Arial", 10, "bold"))
        self.label_nama.grid(row=0, column=2, padx=8)

    def buat_tabel(self, induk, kolom, lebar):
        """Membuat tabel + scrollbar di dalam 'induk', lalu mengembalikan tabelnya."""
        bingkai = ttk.Frame(induk)
        bingkai.pack(fill="both", expand=True, padx=8)

        tabel = ttk.Treeview(bingkai, columns=kolom, show="headings", height=12)
        for k in kolom:
            tabel.heading(k, text=k)
            tabel.column(k, width=lebar[k],
                         anchor="w" if k in ("Kode", "Nama") else "center")

        gulir = ttk.Scrollbar(bingkai, orient="vertical", command=tabel.yview)
        tabel.configure(yscrollcommand=gulir.set)
        tabel.pack(side="left", fill="both", expand=True)
        gulir.pack(side="right", fill="y")
        return tabel

    def buat_panel_tengah(self):
        """Membuat dua panel berdampingan: Pilih Alat (kiri) dan Keranjang (kanan)."""
        tengah = ttk.Frame(self)
        tengah.pack(fill="both", expand=True, padx=10, pady=5)

        # ----- Panel kiri: pilih alat -----
        kiri = ttk.LabelFrame(tengah, text="Pilih Alat")
        kiri.pack(side="left", fill="both", expand=True, padx=(0, 5))

        baris_cari = ttk.Frame(kiri)
        baris_cari.pack(fill="x", padx=8, pady=6)
        ttk.Label(baris_cari, text="Cari:").pack(side="left")
        kotak_cari = ttk.Entry(baris_cari, textvariable=self.var_cari, width=25)
        kotak_cari.pack(side="left", padx=5)
        kotak_cari.bind("<KeyRelease>", lambda e: self.muat_alat())

        self.tabel_alat = self.buat_tabel(
            kiri, ("Kode", "Nama", "Tersedia"),
            {"Kode": 80, "Nama": 200, "Tersedia": 70})

        baris_jumlah = ttk.Frame(kiri)
        baris_jumlah.pack(fill="x", padx=8, pady=8)
        ttk.Label(baris_jumlah, text="Jumlah:").pack(side="left")
        ttk.Spinbox(baris_jumlah, from_=1, to=99, textvariable=self.var_jumlah,
                    width=5).pack(side="left", padx=5)
        ttk.Button(baris_jumlah, text="Tambah ke Keranjang",
                   command=self.tambah_ke_keranjang).pack(side="left", padx=5)

        # ----- Panel kanan: keranjang -----
        kanan = ttk.LabelFrame(tengah, text="Keranjang Peminjaman")
        kanan.pack(side="left", fill="both", expand=True, padx=(5, 0))

        self.tabel_keranjang = self.buat_tabel(
            kanan, ("Kode", "Nama", "Jumlah"),
            {"Kode": 80, "Nama": 200, "Jumlah": 70})

        self.label_total = ttk.Label(kanan, text="Keranjang kosong")
        self.label_total.pack(anchor="w", padx=8, pady=(6, 0))

        baris_tombol = ttk.Frame(kanan)
        baris_tombol.pack(fill="x", padx=8, pady=8)
        ttk.Button(baris_tombol, text="Hapus Item",
                   command=self.hapus_dari_keranjang).pack(side="left", padx=(0, 5))
        ttk.Button(baris_tombol, text="Kosongkan",
                   command=self.kosongkan_keranjang).pack(side="left")

    def buat_tombol_bawah(self):
        """Membuat tombol Pinjam Semua di bagian bawah."""
        bawah = ttk.Frame(self)
        bawah.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(bawah, text="Pinjam Semua",
                   command=self.tombol_pinjam).pack(side="right")

    # ------------------------------------------------------------
    # BAGIAN DATA (menghubungkan tampilan dengan file logika)
    # ------------------------------------------------------------
    def segarkan(self):
        """Memuat ulang tabel alat (dipanggil gui.py saat tab ini dibuka)."""
        self.muat_alat()

    def muat_alat(self):
        """Mengisi tabel alat dari daftar_alat_tersedia() (sesuai kolom cari)."""
        self.tabel_alat.delete(*self.tabel_alat.get_children())
        for kode, nama, tersedia in daftar_alat_tersedia(self.var_cari.get()):
            # Kode alat dipakai sebagai id baris (iid) agar mudah diambil kembali
            self.tabel_alat.insert("", "end", iid=kode, values=(kode, nama, tersedia))

    def cek_nim(self):
        """Menampilkan nama mahasiswa jika NIM yang diketik sudah lengkap."""
        nim = self.var_nim.get().strip()
        self.label_nama.config(text="")
        if len(nim) != PANJANG_NIM:
            return
        for baris in daftar_mahasiswa(nim):
            if baris[0] == nim:
                self.label_nama.config(text=baris[1])
                return
        self.label_nama.config(text="(NIM belum terdaftar)")

    def tampil_keranjang(self):
        """Menggambar ulang isi keranjang dari self.keranjang."""
        self.tabel_keranjang.delete(*self.tabel_keranjang.get_children())
        for kode, (nama, jumlah) in self.keranjang.items():
            self.tabel_keranjang.insert("", "end", iid=kode, values=(kode, nama, jumlah))

        if self.keranjang:
            total_unit = sum(jumlah for nama, jumlah in self.keranjang.values())
            self.label_total.config(
                text=f"{len(self.keranjang)} jenis alat, {total_unit} unit")
        else:
            self.label_total.config(text="Keranjang kosong")

    # ------------------------------------------------------------
    # BAGIAN TOMBOL
    # ------------------------------------------------------------
    def tambah_ke_keranjang(self):
        """Memasukkan alat yang dipilih beserta jumlahnya ke keranjang."""
        pilihan = self.tabel_alat.selection()
        if not pilihan:
            messagebox.showerror("Gagal", "Pilih alat dari tabel dulu!")
            return

        jumlah = self.var_jumlah.get().strip()
        if not jumlah.isdigit() or int(jumlah) <= 0:
            messagebox.showerror("Gagal", "Jumlah harus berupa angka lebih dari 0!")
            return
        jumlah = int(jumlah)

        kode = pilihan[0]                                   # id baris = kode alat
        nama, tersedia = self.tabel_alat.item(kode)["values"][1:3]

        # Jumlah di keranjang tidak boleh melebihi stok yang tersedia
        sudah = self.keranjang[kode][1] if kode in self.keranjang else 0
        if sudah + jumlah > int(tersedia):
            messagebox.showerror(
                "Gagal",
                f"Stok {nama} tidak cukup.\n"
                f"Tersedia {tersedia}, sudah di keranjang {sudah}.")
            return

        # Jika alat yang sama dipilih lagi, jumlahnya digabung
        self.keranjang[kode] = [str(nama), sudah + jumlah]
        self.var_jumlah.set("1")
        self.tampil_keranjang()

    def hapus_dari_keranjang(self):
        """Menghapus satu alat yang dipilih dari keranjang."""
        pilihan = self.tabel_keranjang.selection()
        if not pilihan:
            messagebox.showerror("Gagal", "Pilih item di keranjang dulu!")
            return
        del self.keranjang[pilihan[0]]
        self.tampil_keranjang()

    def kosongkan_keranjang(self):
        """Mengosongkan seluruh isi keranjang."""
        self.keranjang.clear()
        self.tampil_keranjang()

    def tombol_pinjam(self):
        """Tombol Pinjam Semua: memanggil pinjam() dengan seluruh isi keranjang."""
        # Ubah isi keranjang menjadi list [(kode, jumlah), ...] untuk pinjam()
        daftar_barang = [(kode, jumlah)
                         for kode, (nama, jumlah) in self.keranjang.items()]

        berhasil, pesan = pinjam(self.var_nim.get(), daftar_barang)

        if berhasil:
            messagebox.showinfo("Berhasil", pesan)
            self.var_nim.set("")
            self.label_nama.config(text="")
            self.kosongkan_keranjang()      # keranjang hanya dikosongkan jika berhasil
        else:
            messagebox.showerror("Gagal", pesan)

        self.muat_alat()                    # stok bisa berubah, jadi tampilkan ulang


# Bagian ini hanya jalan jika file dijalankan langsung (untuk melihat tab ini sendirian)
if __name__ == "__main__":
    jendela = tk.Tk()
    jendela.title("Tes Tab Peminjaman")
    jendela.geometry("900x560")
    TabPeminjaman(jendela).pack(fill="both", expand=True)
    jendela.mainloop()