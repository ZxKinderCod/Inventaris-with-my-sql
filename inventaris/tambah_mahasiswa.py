"""
tambah_mahasiswa.py
-------------------
Fungsi: menambah data mahasiswa (NIM/NPM dan nama) ke tabel mahasiswa.
Dipanggil dari gui.py saat tombol "Tambah" di bagian mahasiswa ditekan.
"""

from database import jalankan, ambil

# Panjang NIM/NPM yang dianggap valid (contoh: 25037010034 = 11 digit)
PANJANG_NIM = 11


def nim_valid(nim):
    """
    Memeriksa apakah NIM valid: hanya angka dan panjangnya tepat PANJANG_NIM.
    Fungsi ini juga dipakai file lain (update, peminjaman).

    return: True jika valid, False jika tidak
    """
    return nim.isdigit() and len(nim) == PANJANG_NIM


def tambah_mahasiswa(nim, nama):
    """
    Menambah satu mahasiswa ke database setelah data diperiksa.

    nim  : NIM/NPM mahasiswa, harus angka dan 11 digit
    nama : nama lengkap mahasiswa

    return: (berhasil, pesan)
            berhasil = True/False, pesan = keterangan untuk ditampilkan
    """
    # Hapus spasi berlebih di awal dan akhir
    nim = nim.strip()
    nama = nama.strip()

    # 1. NIM dan nama wajib diisi
    if nim == "" or nama == "":
        return False, "NIM dan nama wajib diisi!"

    # 2. NIM harus angka dan panjangnya sesuai
    if not nim_valid(nim):
        return False, f"NIM harus berupa angka dan {PANJANG_NIM} digit!"

    # 3. NIM tidak boleh sama dengan yang sudah terdaftar
    sudah_ada = ambil("SELECT nim FROM mahasiswa WHERE nim = %s", (nim,))
    if sudah_ada:
        return False, f"NIM {nim} sudah terdaftar!"

    # 4. Semua aman, simpan ke database
    jalankan(
        "INSERT INTO mahasiswa (nim, nama) VALUES (%s, %s)",
        (nim, nama)
    )
    return True, f"Mahasiswa {nama} berhasil ditambahkan."


# Bagian ini hanya jalan jika file dijalankan langsung (untuk tes)
if __name__ == "__main__":
    print(tambah_mahasiswa("25037010099", "TES MAHASISWA"))  # data baru
    print(tambah_mahasiswa("25037010099", "TES MAHASISWA"))  # sengaja diulang
    print(tambah_mahasiswa("2503701", "NIM PENDEK"))         # sengaja kurang digit
    print(tambah_mahasiswa("2503701009A", "ADA HURUF"))      # sengaja ada huruf

    # Hapus data tes supaya tabel tetap bersih
    jalankan("DELETE FROM mahasiswa WHERE nim = %s", ("25037010099",))