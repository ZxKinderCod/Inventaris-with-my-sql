"""
tambah_alat.py
--------------
Fungsi: menambah data alat baru ke tabel alat.
Dipanggil dari gui.py saat tombol "Tambah" ditekan.
"""

from database import jalankan, ambil


def tambah_alat(kode, nama, jumlah, kondisi):
    """
    Menambah satu alat ke database setelah data diperiksa.

    kode    : kode unik alat, contoh "A001"
    nama    : nama alat, contoh "Multimeter"
    jumlah  : jumlah stok (angka)
    kondisi : "baik" atau "rusak"

    return: (berhasil, pesan)
            berhasil = True/False, pesan = keterangan untuk ditampilkan
    """
    # Hapus spasi berlebih di awal dan akhir
    kode = kode.strip()
    nama = nama.strip()
    jumlah = str(jumlah).strip()

    # 1. Semua data wajib diisi
    if kode == "" or nama == "" or jumlah == "":
        return False, "Kode, nama, dan jumlah wajib diisi!"

    # 2. Jumlah harus angka bulat lebih dari 0
    if not jumlah.isdigit() or int(jumlah) <= 0:
        return False, "Jumlah harus berupa angka lebih dari 0!"

    # 3. Kondisi hanya boleh baik atau rusak
    if kondisi not in ("baik", "rusak"):
        return False, "Kondisi harus 'baik' atau 'rusak'!"

    # 4. Kode alat tidak boleh sama dengan yang sudah ada
    sudah_ada = ambil("SELECT kode FROM alat WHERE kode = %s", (kode,))
    if sudah_ada:
        return False, f"Kode alat {kode} sudah terdaftar!"

    # 5. Semua aman, simpan ke database
    jalankan(
        "INSERT INTO alat (kode, nama, jumlah, kondisi) VALUES (%s, %s, %s, %s)",
        (kode, nama, int(jumlah), kondisi)
    )
    return True, f"Alat {nama} berhasil ditambahkan."


# Bagian ini hanya jalan jika file dijalankan langsung (untuk tes)
if __name__ == "__main__":
    print(tambah_alat("A001", "Multimeter", 5, "baik"))
    print(tambah_alat("A001", "Multimeter", 5, "baik"))   # sengaja diulang
    print(tambah_alat("A002", "Osiloskop", "abc", "baik"))  # sengaja salah