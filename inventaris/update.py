# UPDATE DAFTAR ALAT DAN UPDATE DATA MAHASISWA
"""
update.py
---------
Fungsi: mengubah data yang sudah ada di database.
  - ubah_alat()       : ubah nama, jumlah, dan kondisi alat
  - ubah_mahasiswa()  : ubah nama mahasiswa
Kode alat dan NIM tidak bisa diubah karena menjadi kunci data.
Dipanggil dari gui.py saat tombol "Ubah" ditekan.
"""

from database import jalankan, ambil


def ubah_alat(kode, nama, jumlah, kondisi):
    """
    Mengubah data satu alat berdasarkan kodenya.

    kode    : kode alat yang akan diubah (harus sudah ada)
    nama    : nama alat yang baru
    jumlah  : jumlah stok yang baru (angka lebih dari 0)
    kondisi : "baik" atau "rusak"

    return: (berhasil, pesan)
    """
    kode = kode.strip()
    nama = nama.strip()
    jumlah = str(jumlah).strip()

    # 1. Data wajib diisi
    if kode == "" or nama == "" or jumlah == "":
        return False, "Kode, nama, dan jumlah wajib diisi!"

    # 2. Jumlah harus angka bulat lebih dari 0
    if not jumlah.isdigit() or int(jumlah) <= 0:
        return False, "Jumlah harus berupa angka lebih dari 0!"

    # 3. Kondisi hanya boleh baik atau rusak
    if kondisi not in ("baik", "rusak"):
        return False, "Kondisi harus 'baik' atau 'rusak'!"

    # 4. Alat harus sudah terdaftar
    ada = ambil("SELECT kode FROM alat WHERE kode = %s", (kode,))
    if not ada:
        return False, f"Alat dengan kode {kode} tidak ditemukan!"

    # 5. Stok baru tidak boleh lebih kecil dari alat yang sedang dipinjam
    hasil = ambil(
        "SELECT COUNT(*) FROM peminjaman WHERE kode_alat = %s AND status = 'dipinjam'",
        (kode,)
    )
    sedang_dipinjam = hasil[0][0]
    if int(jumlah) < sedang_dipinjam:
        return False, f"Jumlah tidak boleh kurang dari {sedang_dipinjam} (sedang dipinjam)!"

    # 6. Semua aman, simpan perubahan
    jalankan(
        "UPDATE alat SET nama = %s, jumlah = %s, kondisi = %s WHERE kode = %s",
        (nama, int(jumlah), kondisi, kode)
    )
    return True, f"Data alat {kode} berhasil diubah."


def ubah_mahasiswa(nim, nama):
    """
    Mengubah nama mahasiswa berdasarkan NIM-nya.

    nim  : NIM mahasiswa yang akan diubah (harus sudah ada)
    nama : nama yang baru

    return: (berhasil, pesan)
    """
    nim = nim.strip()
    nama = nama.strip()

    # 1. Data wajib diisi
    if nim == "" or nama == "":
        return False, "NIM dan nama wajib diisi!"

    # 2. Mahasiswa harus sudah terdaftar
    ada = ambil("SELECT nim FROM mahasiswa WHERE nim = %s", (nim,))
    if not ada:
        return False, f"Mahasiswa dengan NIM {nim} tidak ditemukan!"

    # 3. Simpan perubahan
    jalankan("UPDATE mahasiswa SET nama = %s WHERE nim = %s", (nama, nim))
    return True, f"Data mahasiswa {nim} berhasil diubah."


# Bagian ini hanya jalan jika file dijalankan langsung (untuk tes)
if __name__ == "__main__":
    # --- Tes ubah alat (pakai data sementara TES01) ---
    jalankan("INSERT INTO alat VALUES ('TES01', 'Alat Tes', 3, 'baik')")
    print(ubah_alat("TES01", "Alat Tes Baru", 5, "rusak"))  # berhasil
    print(ubah_alat("XXX99", "Tidak Ada", 1, "baik"))       # kode tidak ada
    print(ubah_alat("TES01", "Alat Tes", 0, "baik"))        # jumlah salah
    print(ambil("SELECT * FROM alat WHERE kode = 'TES01'"))  # lihat hasil
    jalankan("DELETE FROM alat WHERE kode = 'TES01'")        # bersihkan

    # --- Tes ubah mahasiswa (pakai data sementara) ---
    jalankan("INSERT INTO mahasiswa VALUES ('25037010099', 'TES LAMA')")
    print(ubah_mahasiswa("25037010099", "TES BARU"))         # berhasil
    print(ubah_mahasiswa("25037010098", "TIDAK ADA"))        # NIM tidak ada
    print(ubah_mahasiswa("25037010099", ""))                 # nama kosong
    print(ambil("SELECT * FROM mahasiswa WHERE nim = '25037010099'"))
    jalankan("DELETE FROM mahasiswa WHERE nim = '25037010099'")  # bersihkan