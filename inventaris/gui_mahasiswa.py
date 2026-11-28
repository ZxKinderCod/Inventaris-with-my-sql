"""
gui_mahasiswa.py
----------------
Fungsi: tampilan (GUI) untuk tab "Data Mahasiswa".

Satu tab ini MENGGABUNGKAN beberapa fitur sekaligus:
  - TAMBAH : tombol "Tambah" -> memakai tambah_mahasiswa() dari tambah_mahasiswa.py
             (termasuk validasi NIM: harus angka dan 11 digit)
  - UBAH   : tombol "Ubah"   -> memakai ubah_mahasiswa()   dari update.py
  - HAPUS  : tombol "Hapus"  -> memakai hapus_mahasiswa()  dari hapus.py
  - DAFTAR : tabel + kolom cari -> memakai daftar_mahasiswa() dari daftar.py

File ini hanya mengurus TAMPILAN. Pemeriksaan data (validasi) dan akses
database dikerjakan oleh file-file logika di atas.
Kelas TabMahasiswa dipasang ke jendela utama oleh gui.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from tambah_mahasiswa import tambah_mahasiswa
from update import ubah_mahasiswa
from hapus import hapus_mahasiswa
from daftar import daftar_mahasiswa


class TabMahasiswa(ttk.Frame):
    """Tab Data Mahasiswa: form isian, tombol, kolom cari, dan tabel."""

    def __init__(self, induk):
        super().__init__(induk)

        # Variabel untuk menyimpan isi kotak isian
        self.var_nim = tk.StringVar()
        self.var_nama = tk.StringVar()
        self.var_cari = tk.StringVar()

        # Susun tampilan dari atas ke bawah, lalu isi tabel
        self.buat_form()
        self.buat_tombol()
        self.buat_tabel()
        self.muat_data()

    # ------------------------------------------------------------
    # BAGIAN TAMPILAN
    # ------------------------------------------------------------
    def buat_form(self):
        """Membuat kotak isian: NIM dan nama."""
        form = ttk.LabelFrame(self, text="Form Data Mahasiswa")
        form.pack(fill="x", padx=10, pady=(10, 5))

        # Label di baris atas
        for kolom, teks in enumerate(["NIM / NPM", "Nama Mahasiswa"]):
            ttk.Label(form, text=teks).grid(
                row=0, column=kolom, sticky="w", padx=8, pady=(6, 0))

        # Kotak isian di baris bawah
        self.entry_nim = ttk.Entry(form, textvariable=self.var_nim, width=18)
        self.entry_nim.grid(row=1, column=0, padx=8, pady=(0, 8))
        ttk.Entry(form, textvariable=self.var_nama, width=45).grid(
            row=1, column=1, padx=8, pady=(0, 8))

    def buat_tombol(self):
        """Membuat tombol Tambah, Ubah, Hapus, dan Bersihkan."""
        bingkai = ttk.Frame(self)
        bingkai.pack(fill="x", padx=10, pady=5)
        ttk.Button(bingkai, text="Tambah", command=self.tombol_tambah).pack(side="left", padx=4)
        ttk.Button(bingkai, text="Ubah", command=self.tombol_ubah).pack(side="left", padx=4)
        ttk.Button(bingkai, text="Hapus", command=self.tombol_hapus).pack(side="left", padx=4)
        ttk.Button(bingkai, text="Bersihkan", command=self.bersihkan).pack(side="left", padx=4)

    def buat_tabel(self):
        """Membuat kolom pencarian dan tabel daftar mahasiswa."""
        # Baris pencarian: tabel langsung menyaring saat mengetik
        baris_cari = ttk.Frame(self)
        baris_cari.pack(fill="x", padx=10, pady=(5, 0))
        ttk.Label(baris_cari, text="Cari (NIM / nama):").pack(side="left")
        kotak_cari = ttk.Entry(baris_cari, textvariable=self.var_cari, width=30)
        kotak_cari.pack(side="left", padx=5)
        kotak_cari.bind("<KeyRelease>", lambda e: self.muat_data())
        self.label_total = ttk.Label(baris_cari, text="")
        self.label_total.pack(side="right")

        # Tabel beserta scrollbar
        bingkai = ttk.Frame(self)
        bingkai.pack(fill="both", expand=True, padx=10, pady=8)

        kolom = ("NIM", "Nama", "Sedang Dipinjam")
        lebar = {"NIM": 120, "Nama": 330, "Sedang Dipinjam": 120}
        self.tabel = ttk.Treeview(bingkai, columns=kolom, show="headings")
        for k in kolom:
            self.tabel.heading(k, text=k)
            self.tabel.column(k, width=lebar[k],
                              anchor="center" if k == "Sedang Dipinjam" else "w")

        gulir = ttk.Scrollbar(bingkai, orient="vertical", command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=gulir.set)
        self.tabel.pack(side="left", fill="both", expand=True)
        gulir.pack(side="right", fill="y")

        # Mahasiswa yang sedang meminjam alat ditampilkan dengan tulisan oranye
        self.tabel.tag_configure("meminjam", foreground="#c75b00")

        # Klik satu baris -> datanya masuk ke form
        self.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)

    # ------------------------------------------------------------
    # BAGIAN DATA (menghubungkan tampilan dengan file logika)
    # ------------------------------------------------------------
    def muat_data(self):
        """Mengisi tabel dengan data dari daftar_mahasiswa() (sesuai kolom cari)."""
        self.tabel.delete(*self.tabel.get_children())   # kosongkan dulu
        data = daftar_mahasiswa(self.var_cari.get())
        for baris in data:
            tag = ("meminjam",) if baris[2] > 0 else ()
            # NIM dipakai sebagai id baris (iid) supaya tetap berupa teks utuh
            self.tabel.insert("", "end", iid=baris[0], values=baris, tags=tag)
        self.label_total.config(text=f"Total: {len(data)} mahasiswa")

    def segarkan(self):
        """Dipanggil gui.py saat tab dibuka, memuat ulang tabel."""
        self.muat_data()

    def pilih_baris(self, event):
        """Dipanggil saat baris tabel diklik: isi form dengan data baris itu."""
        pilihan = self.tabel.selection()
        if not pilihan:
            return
        nim = pilihan[0]                                # id baris = NIM
        nama = self.tabel.item(nim)["values"][1]
        self.var_nim.set(nim)
        self.var_nama.set(str(nama))
        # NIM adalah kunci data, jadi dikunci agar tidak bisa diubah
        self.entry_nim.config(state="disabled")

    def bersihkan(self):
        """Mengosongkan form dan membuka kembali kunci kotak NIM."""
        self.var_nim.set("")
        self.var_nama.set("")
        self.entry_nim.config(state="normal")
        self.tabel.selection_remove(self.tabel.selection())

    def tampil_pesan(self, berhasil, pesan):
        """Menampilkan kotak pesan: info jika berhasil, error jika gagal."""
        if berhasil:
            messagebox.showinfo("Berhasil", pesan)
        else:
            messagebox.showerror("Gagal", pesan)

    # ------------------------------------------------------------
    # BAGIAN TOMBOL
    # ------------------------------------------------------------
    def tombol_tambah(self):
        """Tombol Tambah: memanggil tambah_mahasiswa() dengan isi form."""
        berhasil, pesan = tambah_mahasiswa(self.var_nim.get(), self.var_nama.get())
        self.tampil_pesan(berhasil, pesan)
        if berhasil:
            self.bersihkan()
            self.muat_data()

    def tombol_ubah(self):
        """Tombol Ubah: memanggil ubah_mahasiswa() dengan isi form."""
        berhasil, pesan = ubah_mahasiswa(self.var_nim.get(), self.var_nama.get())
        self.tampil_pesan(berhasil, pesan)
        if berhasil:
            self.bersihkan()
            self.muat_data()

    def tombol_hapus(self):
        """Tombol Hapus: minta konfirmasi, lalu memanggil hapus_mahasiswa()."""
        nim = self.var_nim.get()
        if nim.strip() == "":
            messagebox.showerror("Gagal", "Pilih mahasiswa dari tabel dulu!")
            return
        yakin = messagebox.askyesno(
            "Konfirmasi",
            f"Yakin hapus {nim} - {self.var_nama.get()}?\n"
            "Riwayat peminjamannya juga ikut terhapus.")
        if not yakin:
            return
        berhasil, pesan = hapus_mahasiswa(nim)
        self.tampil_pesan(berhasil, pesan)
        if berhasil:
            self.bersihkan()
            self.muat_data()


# Bagian ini hanya jalan jika file dijalankan langsung (untuk melihat tab ini sendirian)
if __name__ == "__main__":
    jendela = tk.Tk()
    jendela.title("Tes Tab Data Mahasiswa")
    jendela.geometry("720x520")
    TabMahasiswa(jendela).pack(fill="both", expand=True)
    jendela.mainloop()