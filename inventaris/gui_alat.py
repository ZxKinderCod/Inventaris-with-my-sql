"""
gui_alat.py
-----------
Fungsi: tampilan (GUI) untuk tab "Data Alat".

Satu tab ini MENGGABUNGKAN beberapa fitur sekaligus:
  - TAMBAH : tombol "Tambah" -> memakai tambah_alat() dari tambah_alat.py
  - UBAH   : tombol "Ubah"   -> memakai ubah_alat()   dari update.py
  - HAPUS  : tombol "Hapus"  -> memakai hapus_alat()  dari hapus.py
  - DAFTAR : tabel + kolom cari -> memakai daftar_alat() dari daftar.py

File ini hanya mengurus TAMPILAN. Pemeriksaan data (validasi) dan akses
database dikerjakan oleh file-file logika di atas.
Kelas TabAlat dipasang ke jendela utama oleh gui.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from tambah_alat import tambah_alat
from update import ubah_alat
from hapus import hapus_alat
from daftar import daftar_alat


class TabAlat(ttk.Frame):
    """Tab Data Alat: form isian, tombol, kolom cari, dan tabel."""

    def __init__(self, induk):
        super().__init__(induk)

        # Variabel untuk menyimpan isi kotak isian
        self.var_kode = tk.StringVar()
        self.var_nama = tk.StringVar()
        self.var_jumlah = tk.StringVar()
        self.var_kondisi = tk.StringVar(value="baik")
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
        """Membuat kotak isian: kode, nama, jumlah, dan kondisi."""
        form = ttk.LabelFrame(self, text="Form Data Alat")
        form.pack(fill="x", padx=10, pady=(10, 5))

        # Label di baris atas
        for kolom, teks in enumerate(["Kode", "Nama Alat", "Jumlah", "Kondisi"]):
            ttk.Label(form, text=teks).grid(
                row=0, column=kolom, sticky="w", padx=8, pady=(6, 0))

        # Kotak isian di baris bawah
        self.entry_kode = ttk.Entry(form, textvariable=self.var_kode, width=12)
        self.entry_kode.grid(row=1, column=0, padx=8, pady=(0, 8))
        ttk.Entry(form, textvariable=self.var_nama, width=32).grid(
            row=1, column=1, padx=8, pady=(0, 8))
        ttk.Entry(form, textvariable=self.var_jumlah, width=8).grid(
            row=1, column=2, padx=8, pady=(0, 8))
        ttk.Combobox(form, textvariable=self.var_kondisi,
                     values=["baik", "rusak"], state="readonly",
                     width=8).grid(row=1, column=3, padx=8, pady=(0, 8))

    def buat_tombol(self):
        """Membuat tombol Tambah, Ubah, Hapus, dan Bersihkan."""
        bingkai = ttk.Frame(self)
        bingkai.pack(fill="x", padx=10, pady=5)
        ttk.Button(bingkai, text="Tambah", command=self.tombol_tambah).pack(side="left", padx=4)
        ttk.Button(bingkai, text="Ubah", command=self.tombol_ubah).pack(side="left", padx=4)
        ttk.Button(bingkai, text="Hapus", command=self.tombol_hapus).pack(side="left", padx=4)
        ttk.Button(bingkai, text="Bersihkan", command=self.bersihkan).pack(side="left", padx=4)

    def buat_tabel(self):
        """Membuat kolom pencarian dan tabel daftar alat."""
        # Baris pencarian: tabel langsung menyaring saat mengetik
        baris_cari = ttk.Frame(self)
        baris_cari.pack(fill="x", padx=10, pady=(5, 0))
        ttk.Label(baris_cari, text="Cari (kode / nama):").pack(side="left")
        kotak_cari = ttk.Entry(baris_cari, textvariable=self.var_cari, width=30)
        kotak_cari.pack(side="left", padx=5)
        kotak_cari.bind("<KeyRelease>", lambda e: self.muat_data())
        self.label_total = ttk.Label(baris_cari, text="")
        self.label_total.pack(side="right")

        # Tabel beserta scrollbar
        bingkai = ttk.Frame(self)
        bingkai.pack(fill="both", expand=True, padx=10, pady=8)

        kolom = ("Kode", "Nama", "Jumlah", "Kondisi", "Tersedia")
        lebar = {"Kode": 80, "Nama": 280, "Jumlah": 70, "Kondisi": 80, "Tersedia": 80}
        self.tabel = ttk.Treeview(bingkai, columns=kolom, show="headings")
        for k in kolom:
            self.tabel.heading(k, text=k)
            self.tabel.column(k, width=lebar[k],
                              anchor="w" if k in ("Kode", "Nama") else "center")

        gulir = ttk.Scrollbar(bingkai, orient="vertical", command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=gulir.set)
        self.tabel.pack(side="left", fill="both", expand=True)
        gulir.pack(side="right", fill="y")

        # Alat rusak ditampilkan dengan tulisan merah
        self.tabel.tag_configure("rusak", foreground="red")

        # Klik satu baris -> datanya masuk ke form
        self.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)

    # ------------------------------------------------------------
    # BAGIAN DATA (menghubungkan tampilan dengan file logika)
    # ------------------------------------------------------------
    def muat_data(self):
        """Mengisi tabel dengan data dari daftar_alat() (sesuai kolom cari)."""
        self.tabel.delete(*self.tabel.get_children())   # kosongkan dulu
        data = daftar_alat(self.var_cari.get())
        for baris in data:
            tag = ("rusak",) if baris[3] == "rusak" else ()
            self.tabel.insert("", "end", values=baris, tags=tag)
        self.label_total.config(text=f"Total: {len(data)} jenis alat")

    def pilih_baris(self, event):
        """Dipanggil saat baris tabel diklik: isi form dengan data baris itu."""
        pilihan = self.tabel.selection()
        if not pilihan:
            return
        kode, nama, jumlah, kondisi, _ = self.tabel.item(pilihan[0])["values"]
        self.var_kode.set(str(kode))
        self.var_nama.set(str(nama))
        self.var_jumlah.set(str(jumlah))
        self.var_kondisi.set(str(kondisi))
        # Kode adalah kunci data, jadi dikunci agar tidak bisa diubah
        self.entry_kode.config(state="disabled")

    def bersihkan(self):
        """Mengosongkan form dan membuka kembali kunci kotak kode."""
        self.var_kode.set("")
        self.var_nama.set("")
        self.var_jumlah.set("")
        self.var_kondisi.set("baik")
        self.entry_kode.config(state="normal")
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
        """Tombol Tambah: memanggil tambah_alat() dengan isi form."""
        berhasil, pesan = tambah_alat(
            self.var_kode.get(), self.var_nama.get(),
            self.var_jumlah.get(), self.var_kondisi.get())
        self.tampil_pesan(berhasil, pesan)
        if berhasil:
            self.bersihkan()
            self.muat_data()

    def tombol_ubah(self):
        """Tombol Ubah: memanggil ubah_alat() dengan isi form."""
        berhasil, pesan = ubah_alat(
            self.var_kode.get(), self.var_nama.get(),
            self.var_jumlah.get(), self.var_kondisi.get())
        self.tampil_pesan(berhasil, pesan)
        if berhasil:
            self.bersihkan()
            self.muat_data()

    def tombol_hapus(self):
        """Tombol Hapus: minta konfirmasi, lalu memanggil hapus_alat()."""
        kode = self.var_kode.get()
        if kode.strip() == "":
            messagebox.showerror("Gagal", "Pilih alat dari tabel dulu!")
            return
        if not messagebox.askyesno("Konfirmasi", f"Yakin hapus alat {kode}?"):
            return
        berhasil, pesan = hapus_alat(kode)
        self.tampil_pesan(berhasil, pesan)
        if berhasil:
            self.bersihkan()
            self.muat_data()


# Bagian ini hanya jalan jika file dijalankan langsung (untuk melihat tab ini sendirian)
if __name__ == "__main__":
    jendela = tk.Tk()
    jendela.title("Tes Tab Data Alat")
    jendela.geometry("820x520")
    TabAlat(jendela).pack(fill="both", expand=True)
    jendela.mainloop()