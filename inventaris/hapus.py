# HAPUS DAFTAR ALAT DAN HAPUS DATA MAHASISWA
"""
hapus.py
--------
Fungsi: menghapus data dari database.
  - hapus_alat()       : hapus satu alat berdasarkan kode
  - hapus_mahasiswa()  : hapus satu mahasiswa berdasarkan NIM

Aturan:
  - Alat/mahasiswa yang MASIH DIPINJAM tidak boleh dihapus.
  - Jika hanya punya riwayat lama (sudah dikembalikan), data boleh
    dihapus dan riwayatnya ikut terhapus (ON DELETE CASCADE di database).

Catatan: pertanyaan konfirmasi "Yakin hapus?" ditangani di gui.py.
"""

from database import jalankan, ambil


def hapus_alat(kode):
    """
    Menghapus satu alat berdasarkan kodenya.

    kode : kode alat yang akan dihapus

    return: (berhasil, pesan)
    """
    kode = kode.strip()

    # 1. Kode wajib diisi
    if kode == "":
        return False, "Kode alat wajib diisi!"

    # 2. Alat harus sudah terdaftar
    ada = ambil("SELECT kode FROM alat WHERE kode = %s", (kode,))
    if not ada:
        return False, f"Alat dengan kode {kode} tidak ditemukan!"

    # 3. Cek apakah alat masih dipinjam (status 'dipinjam')
    hasil = ambil(
        "SELECT COUNT(*) FROM peminjaman WHERE kode_alat = %s AND status = 'dipinjam'",
        (kode,)
    )
    sedang_dipinjam = hasil[0][0]
    if sedang_dipinjam > 0:
        return False, f"Alat {kode} tidak bisa dihapus, masih dipinjam ({sedang_dipinjam} unit)!"

    # 4. Aman, hapus alat (riwayatnya ikut terhapus otomatis)
    jalankan("DELETE FROM alat WHERE kode = %s", (kode,))
    return True, f"Alat {kode} berhasil dihapus. Riwayat peminjamannya ikut terhapus."


def hapus_mahasiswa(nim):
    """
    Menghapus satu mahasiswa berdasarkan NIM-nya.

    nim : NIM mahasiswa yang akan dihapus

    return: (berhasil, pesan)
    """
    nim = nim.strip()

    # 1. NIM wajib diisi
    if nim == "":
        return False, "NIM wajib diisi!"

    # 2. Mahasiswa harus sudah terdaftar
    ada = ambil("SELECT nim FROM mahasiswa WHERE nim = %s", (nim,))
    if not ada:
        return False, f"Mahasiswa dengan NIM {nim} tidak ditemukan!"

    # 3. Cek apakah mahasiswa masih meminjam alat
    hasil = ambil(
        "SELECT COUNT(*) FROM peminjaman WHERE nim = %s AND status = 'dipinjam'",
        (nim,)
    )
    masih_meminjam = hasil[0][0]
    if masih_meminjam > 0:
        return False, f"Mahasiswa {nim} tidak bisa dihapus, masih meminjam {masih_meminjam} alat!"

    # 4. Aman, hapus mahasiswa (riwayatnya ikut terhapus otomatis)
    jalankan("DELETE FROM mahasiswa WHERE nim = %s", (nim,))
    return True, f"Mahasiswa {nim} berhasil dihapus."


# Bagian ini hanya jalan jika file dijalankan langsung (untuk tes)
if __name__ == "__main__":
    # Siapkan data sementara: 1 alat, 1 mahasiswa, 1 pinjaman aktif
    jalankan("INSERT INTO alat VALUES ('TES01', 'Alat Tes', 3, 'baik')")
    jalankan("INSERT INTO mahasiswa VALUES ('25037010099', 'TES MAHASISWA')")
    jalankan("INSERT INTO peminjaman (nim, kode_alat, tgl_pinjam) "
             "VALUES ('25037010099', 'TES01', CURDATE())")

    # Selama masih dipinjam, keduanya harus ditolak
    print(hapus_alat("TES01"))
    print(hapus_mahasiswa("25037010099"))

    # Kembalikan alatnya, lalu hapus harus berhasil
    jalankan("UPDATE peminjaman SET status = 'dikembalikan', tgl_kembali = CURDATE() "
             "WHERE nim = '25037010099'")
    print(hapus_alat("TES01"))
    print(hapus_mahasiswa("25037010099"))

    # Data yang tidak ada / input kosong
    print(hapus_alat("XXX99"))
    print(hapus_mahasiswa(""))

    # Bersihkan sisa data tes (jaga-jaga kalau ada yang gagal)
    jalankan("DELETE FROM alat WHERE kode = 'TES01'")
    jalankan("DELETE FROM mahasiswa WHERE nim = '25037010099'")