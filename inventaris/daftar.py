# daftar alat, cek stok, peminjam aktif, riwayat
"""
daftar.py
---------
Fungsi: mengambil (membaca) data dari database untuk ditampilkan di GUI.
  - daftar_alat()            : semua alat + stok yang masih tersedia
  - daftar_alat_tersedia()   : hanya alat yang boleh dipinjam
  - daftar_mahasiswa()       : semua mahasiswa + jumlah alat yang dipinjam
  - daftar_peminjam_aktif()  : yang sedang meminjam alat
  - daftar_riwayat()         : semua transaksi peminjaman

Semua fungsi mengembalikan list data, setiap baris berbentuk tuple.
"""

from database import ambil


def daftar_alat(kata_kunci=""):
    """
    Mengambil semua alat beserta stok yang tersedia.
    Stok tersedia = jumlah total - jumlah yang sedang dipinjam.

    kata_kunci : (opsional) mencari berdasarkan kode atau nama alat.
                 Jika kosong, semua alat ditampilkan.

    return: list berisi (kode, nama, jumlah, kondisi, tersedia)
    """
    pola = f"%{kata_kunci.strip()}%"   # tanda % artinya "mengandung kata ini"
    return ambil(
        """
        SELECT a.kode, a.nama, a.jumlah, a.kondisi,
               a.jumlah - COUNT(p.id) AS tersedia
        FROM alat a
        LEFT JOIN peminjaman p
               ON p.kode_alat = a.kode AND p.status = 'dipinjam'
        WHERE a.kode LIKE %s OR a.nama LIKE %s
        GROUP BY a.kode, a.nama, a.jumlah, a.kondisi
        ORDER BY a.kode
        """,
        (pola, pola)
    )


def daftar_alat_tersedia():
    """
    Mengambil alat yang boleh dipinjam: kondisi baik dan stok masih ada.
    Dipakai untuk pilihan (dropdown) di menu peminjaman.

    return: list berisi (kode, nama, tersedia)
    """
    return ambil(
        """
        SELECT a.kode, a.nama, a.jumlah - COUNT(p.id) AS tersedia
        FROM alat a
        LEFT JOIN peminjaman p
               ON p.kode_alat = a.kode AND p.status = 'dipinjam'
        WHERE a.kondisi = 'baik'
        GROUP BY a.kode, a.nama, a.jumlah
        HAVING tersedia > 0
        ORDER BY a.kode
        """
    )


def daftar_mahasiswa(kata_kunci=""):
    """
    Mengambil semua mahasiswa beserta jumlah alat yang sedang dipinjam.

    kata_kunci : (opsional) mencari berdasarkan NIM atau nama.

    return: list berisi (nim, nama, sedang_dipinjam)
    """
    pola = f"%{kata_kunci.strip()}%"
    return ambil(
        """
        SELECT m.nim, m.nama, COUNT(p.id) AS sedang_dipinjam
        FROM mahasiswa m
        LEFT JOIN peminjaman p
               ON p.nim = m.nim AND p.status = 'dipinjam'
        WHERE m.nim LIKE %s OR m.nama LIKE %s
        GROUP BY m.nim, m.nama
        ORDER BY m.nim
        """,
        (pola, pola)
    )


def daftar_peminjam_aktif():
    """
    Mengambil data peminjaman yang alatnya BELUM dikembalikan.

    return: list berisi (id, nim, nama_mahasiswa, kode_alat, nama_alat, tgl_pinjam)
    """
    return ambil(
        """
        SELECT p.id, p.nim, m.nama, p.kode_alat, a.nama, p.tgl_pinjam
        FROM peminjaman p
        JOIN mahasiswa m ON p.nim = m.nim
        JOIN alat a ON p.kode_alat = a.kode
        WHERE p.status = 'dipinjam'
        ORDER BY p.id
        """
    )


def daftar_riwayat():
    """
    Mengambil semua transaksi peminjaman (yang dipinjam maupun dikembalikan).
    Transaksi terbaru ada di paling atas.

    return: list berisi (id, nim, nama_mahasiswa, kode_alat, nama_alat,
                         tgl_pinjam, tgl_kembali, status)
    """
    return ambil(
        """
        SELECT p.id, p.nim, m.nama, p.kode_alat, a.nama,
               p.tgl_pinjam, p.tgl_kembali, p.status
        FROM peminjaman p
        JOIN mahasiswa m ON p.nim = m.nim
        JOIN alat a ON p.kode_alat = a.kode
        ORDER BY p.id DESC
        """
    )


# Bagian ini hanya jalan jika file dijalankan langsung (untuk tes)
if __name__ == "__main__":
    print("Jumlah alat:", len(daftar_alat()))
    print("Jumlah mahasiswa:", len(daftar_mahasiswa()))
    print("Peminjam aktif:", len(daftar_peminjam_aktif()))
    print("Riwayat:", len(daftar_riwayat()))
    print("Alat yang bisa dipinjam:", len(daftar_alat_tersedia()))
    print("Hasil cari 'osiloskop':", len(daftar_alat("osiloskop")))
    print("Contoh 1 alat:", daftar_alat()[0])