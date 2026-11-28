"""
gui_riwayat.py
Tab Riwayat pada GUI inventaris laboratorium.

Fitur:
- Menampilkan seluruh riwayat transaksi peminjaman (dipinjam & dikembalikan).
- Status 'dipinjam' diberi warna oranye supaya mudah dibedakan.
- Kolom cari untuk menyaring berdasarkan NIM, nama, atau nama alat.
- Tabel ini hanya untuk melihat data (tidak ada tombol ubah/hapus).

Alur: gui.py -> TabRiwayat -> daftar.daftar_riwayat() -> MySQL
Nyalakan MySQL di XAMPP sebelum menjalankan program.
"""

import tkinter as tk
from tkinter import ttk

from daftar import daftar_riwayat


class TabRiwayat(ttk.Frame):
    """Tab untuk melihat riwayat semua transaksi peminjaman."""

    def __init__(self, induk):
        super().__init__(induk)
        self.semua_data = []          # semua riwayat dari database
        self.var_cari = tk.StringVar()
        self.buat_tampilan()
        self.segarkan()

    def buat_tampilan(self):
        # Baris atas: kolom cari dan tombol segarkan
        atas = ttk.Frame(self)
        atas.pack(fill="x", padx=10, pady=10)
        ttk.Label(atas, text="Cari NIM / Nama / Alat:").pack(side="left")
        ttk.Entry(atas, textvariable=self.var_cari, width=30).pack(side="left", padx=5)
        ttk.Button(atas, text="Segarkan", command=self.segarkan).pack(side="left")
        # Setiap ketikan langsung menyaring tabel
        self.var_cari.trace_add("write", lambda *a: self.tampilkan())

        # Tabel riwayat (9 kolom)
        kolom = ("id", "nim", "nama", "kode", "alat", "jumlah", "pinjam", "kembali", "status")
        judul = ("ID", "NIM", "Nama", "Kode Alat", "Nama Alat",
                 "Jumlah", "Tgl Pinjam", "Tgl Kembali", "Status")
        lebar = (40, 100, 180, 70, 180, 55, 90, 90, 100)

        bingkai = ttk.Frame(self)
        bingkai.pack(fill="both", expand=True, padx=10)

        self.tabel = ttk.Treeview(bingkai, columns=kolom, show="headings", height=15)
        for k, j, l in zip(kolom, judul, lebar):
            self.tabel.heading(k, text=j)
            self.tabel.column(k, width=l)

        gulir = ttk.Scrollbar(bingkai, orient="vertical", command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=gulir.set)
        self.tabel.pack(side="left", fill="both", expand=True)
        gulir.pack(side="right", fill="y")

        # Yang masih dipinjam ditampilkan dengan tulisan oranye
        self.tabel.tag_configure("dipinjam", foreground="#c75b00")

        # Label jumlah data di bawah tabel
        self.label_total = ttk.Label(self, text="Total: 0 transaksi")
        self.label_total.pack(anchor="w", padx=10, pady=8)

    def segarkan(self):
        """Ambil ulang data dari database (dipanggil gui.py saat tab dibuka)."""
        self.semua_data = daftar_riwayat()
        self.tampilkan()

    def tampilkan(self):
        """Isi tabel, disaring sesuai kata kunci di kolom cari."""
        kata = self.var_cari.get().strip().lower()
        self.tabel.delete(*self.tabel.get_children())
        jumlah = 0
        for baris in self.semua_data:
            # baris = (id, nim, nama_mhs, kode_alat, nama_alat, jumlah,
            #          tgl_pinjam, tgl_kembali, status)
            if (kata in str(baris[1]).lower()
                    or kata in str(baris[2]).lower()
                    or kata in str(baris[4]).lower()):
                # Tanggal kembali masih kosong (None) jika belum dikembalikan
                nilai = [("-" if x is None else str(x)) for x in baris]
                tag = ("dipinjam",) if baris[8] == "dipinjam" else ()
                self.tabel.insert("", "end", values=nilai, tags=tag)
                jumlah += 1
        self.label_total.config(text=f"Total: {jumlah} transaksi")


# Bagian ini hanya jalan jika file dijalankan langsung (untuk tes)
if __name__ == "__main__":
    jendela = tk.Tk()
    jendela.title("Tes Tab Riwayat")
    jendela.geometry("1000x450")
    TabRiwayat(jendela).pack(fill="both", expand=True)
    jendela.mainloop()