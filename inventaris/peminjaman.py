#proses pinjam & kembali + validasi (stok, rusak, NIM)
"""
peminjaman.py
-------------
Fungsi: mengatur proses peminjaman dan pengembalian alat.
  - pinjam()   : mahasiswa meminjam 1 unit alat
  - kembali()  : mahasiswa mengembalikan alat

Aturan peminjaman:
  1. NIM harus valid (angka, 11 digit) dan sudah terdaftar.
  2. Alat harus sudah terdaftar.
  3. Alat yang kondisinya rusak tidak bisa dipinjam.
  4. Alat yang stoknya habis tidak bisa dipinjam.
"""

from datetime import date

from database import jalankan, ambil
from tambah_mahasiswa import nim_valid   # pemeriksaan NIM sudah ada di file ini


def pinjam(nim, kode_alat):
    """
    Mencatat peminjaman 1 unit alat oleh seorang mahasiswa.

    nim       : NIM mahasiswa yang meminjam
    kode_alat : kode alat yang dipinjam

    return: (berhasil, pesan)
    """
    nim = nim.strip()
    kode_alat = kode_alat.strip()

    # 1. Data wajib diisi
    if nim == "" or kode_alat == "":
        return False, "NIM dan kode alat wajib diisi!"

    # 2. NIM harus angka dan panjangnya sesuai
    if not nim_valid(nim):
        return False, "NIM harus berupa angka dan 11 digit!"

    # 3. Mahasiswa harus sudah terdaftar
    mhs = ambil("SELECT nama FROM mahasiswa WHERE nim = %s", (nim,))
    if not mhs:
        return False, f"NIM {nim} belum terdaftar!"
    nama_mhs = mhs[0][0]

    # 4. Alat harus sudah terdaftar
    alat = ambil("SELECT nama, jumlah, kondisi FROM alat WHERE kode = %s", (kode_alat,))
    if not alat:
        return False, f"Alat dengan kode {kode_alat} tidak ditemukan!"
    nama_alat, jumlah, kondisi = alat[0]

    # 5. Alat rusak tidak boleh dipinjam
    if kondisi == "rusak":
        return False, f"{nama_alat} ({kode_alat}) rusak, tidak bisa dipinjam!"

    # 6. Hitung stok tersedia = jumlah total - yang sedang dipinjam
    hasil = ambil(
        "SELECT COUNT(*) FROM peminjaman WHERE kode_alat = %s AND status = 'dipinjam'",
        (kode_alat,)
    )
    tersedia = jumlah - hasil[0][0]
    if tersedia <= 0:
        return False, f"Stok {nama_alat} ({kode_alat}) habis!"

    # 7. Semua aman, catat peminjaman dengan tanggal hari ini
    jalankan(
        "INSERT INTO peminjaman (nim, kode_alat, tgl_pinjam) VALUES (%s, %s, %s)",
        (nim, kode_alat, date.today())
    )
    return True, f"Peminjaman berhasil: {nama_mhs} meminjam {nama_alat} ({kode_alat})."


def kembali(id_peminjaman):
    """
    Mencatat pengembalian alat berdasarkan nomor transaksi (id).

    id_peminjaman : nomor transaksi yang dipilih dari tabel peminjam aktif

    return: (berhasil, pesan)
    """
    # 1. Cari transaksi beserta nama alatnya
    data = ambil(
        """
        SELECT p.status, a.nama, p.kode_alat
        FROM peminjaman p JOIN alat a ON p.kode_alat = a.kode
        WHERE p.id = %s
        """,
        (id_peminjaman,)
    )
    if not data:
        return False, "Data peminjaman tidak ditemukan!"
    status, nama_alat, kode_alat = data[0]

    # 2. Alat yang sudah dikembalikan tidak boleh dikembalikan lagi
    if status == "dikembalikan":
        return False, "Alat sudah pernah dikembalikan!"

    # 3. Ubah status dan isi tanggal kembali dengan hari ini
    jalankan(
        "UPDATE peminjaman SET status = 'dikembalikan', tgl_kembali = %s WHERE id = %s",
        (date.today(), id_peminjaman)
    )
    return True, f"{nama_alat} ({kode_alat}) berhasil dikembalikan."


# Bagian ini hanya jalan jika file dijalankan langsung (untuk tes)
if __name__ == "__main__":
    # Siapkan data sementara: alat baik (stok 1), alat rusak, 1 mahasiswa
    jalankan("INSERT INTO alat VALUES ('TES01', 'Alat Tes', 1, 'baik')")
    jalankan("INSERT INTO alat VALUES ('TES02', 'Alat Rusak Tes', 1, 'rusak')")
    jalankan("INSERT INTO mahasiswa VALUES ('25037010099', 'TES MAHASISWA')")

    print(pinjam("25037010099", "TES01"))   # berhasil
    print(pinjam("25037010099", "TES01"))   # stok habis (stok hanya 1)
    print(pinjam("25037010099", "TES02"))   # alat rusak
    print(pinjam("2503701009A", "TES01"))   # NIM ada huruf
    print(pinjam("25037010098", "TES01"))   # NIM belum terdaftar
    print(pinjam("25037010099", "XXX99"))   # kode alat tidak ada

    # Ambil nomor transaksi yang tadi dibuat, lalu kembalikan
    id_tes = ambil("SELECT id FROM peminjaman WHERE kode_alat = 'TES01'")[0][0]
    print(kembali(id_tes))                  # berhasil
    print(kembali(id_tes))                  # sudah dikembalikan
    print(kembali(999999))                  # transaksi tidak ada

    # Bersihkan data tes (riwayat ikut terhapus otomatis)
    jalankan("DELETE FROM alat WHERE kode IN ('TES01', 'TES02')")
    jalankan("DELETE FROM mahasiswa WHERE nim = '25037010099'")