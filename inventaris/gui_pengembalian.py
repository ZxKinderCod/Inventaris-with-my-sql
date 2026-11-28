"""
gui_pengembalian.py
Tab Pengembalian pada GUI inventaris laboratorium.

Fitur:
- Menampilkan semua peminjam aktif (status 'dipinjam').
- Kolom cari untuk menyaring berdasarkan NIM atau nama.
- Bisa memilih beberapa baris sekaligus (Ctrl/Shift + klik),
  lalu tombol "Kembalikan" memproses semuanya.

Alur: gui.py -> TabPengembalian -> pengembalian.kembali() -> MySQL
Nyalakan MySQL di XAMPP sebelum menjalankan program.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from daftar import daftar_peminjam_aktif
from pengembalian import kembali


class TabPengembalian(ttk.Frame):
    """Tab untuk mengembalikan alat yang sedang dipinjam."""

    def __init__(self, induk):
        super().__init__(induk)
        self.semua_data = []          # semua peminjam aktif dari database
        self.var_cari = tk.StringVar()
        self.buat_tampilan()
        self.segarkan()

    def buat_tampilan(self):
        # Baris atas: kolom cari
        atas = ttk.Frame(self)
        atas.pack(fill="x", padx=10, pady=10)
        ttk.Label(atas, text="Cari NIM / Nama:").pack(side="left")
        kotak = ttk.Entry(atas, textvariable=self.var_cari, width=30)
        kotak.pack(side="left", padx=5)
        # Setiap ketikan langsung menyaring tabel
        self.var_cari.trace_add("write", lambda *a: self.tampilkan())

        # Tabel peminjam aktif (selectmode extended = boleh pilih banyak)
        kolom = ("id", "nim", "nama", "kode", "alat", "jumlah", "tgl")
        judul = ("ID", "NIM", "Nama", "Kode Alat", "Nama Alat", "Jumlah", "Tgl Pinjam")
        lebar = (50, 110, 200, 80, 200, 60, 100)

        self.tabel = ttk.Treeview(self, columns=kolom, show="headings",
                                  selectmode="extended", height=15)
        for k, j, l in zip(kolom, judul, lebar):
            self.tabel.heading(k, text=j)
            self.tabel.column(k, width=l)
        self.tabel.pack(fill="both", expand=True, padx=10)

        # Tombol
        bawah = ttk.Frame(self)
        bawah.pack(fill="x", padx=10, pady=10)
        ttk.Button(bawah, text="Kembalikan", command=self.kembalikan).pack(side="left")
        ttk.Button(bawah, text="Segarkan", command=self.segarkan).pack(side="left", padx=5)

    def segarkan(self):
        """Ambil ulang data dari database (dipanggil gui.py saat tab dibuka)."""
        self.semua_data = daftar_peminjam_aktif()
        self.tampilkan()

    def tampilkan(self):
        """Isi tabel, disaring sesuai kata kunci di kolom cari."""
        kata = self.var_cari.get().strip().lower()
        self.tabel.delete(*self.tabel.get_children())
        for baris in self.semua_data:
            # baris = (id, nim, nama_mhs, kode_alat, nama_alat, jumlah, tgl_pinjam)
            if kata in str(baris[1]).lower() or kata in str(baris[2]).lower():
                # iid = id peminjaman, dipakai saat tombol Kembalikan ditekan
                self.tabel.insert("", "end", iid=str(baris[0]),
                                  values=[str(x) for x in baris])

    def kembalikan(self):
        """Kembalikan semua baris yang dipilih."""
        pilihan = self.tabel.selection()
        if not pilihan:
            messagebox.showwarning("Peringatan", "Pilih minimal satu baris dulu!")
            return
        if not messagebox.askyesno("Konfirmasi",
                                   f"Kembalikan {len(pilihan)} peminjaman?"):
            return

        hasil = []
        for id_pinjam in pilihan:
            berhasil, pesan = kembali(int(id_pinjam))
            hasil.append(pesan)

        messagebox.showinfo("Hasil", "\n".join(hasil))
        self.segarkan()


# Bagian ini hanya jalan jika file dijalankan langsung (untuk tes)
if __name__ == "__main__":
    jendela = tk.Tk()
    jendela.title("Tes Tab Pengembalian")
    jendela.geometry("900x450")
    TabPengembalian(jendela).pack(fill="both", expand=True)
    jendela.mainloop()