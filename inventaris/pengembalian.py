"""
pengembalian.py
---------------
Fungsi: mengatur proses pengembalian alat.
  - kembali() : mencatat alat yang dikembalikan mahasiswa
Dipanggil dari gui_pengembalian.py saat tombol "Kembalikan" ditekan.
"""

from datetime import date

from database import jalankan, ambil


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