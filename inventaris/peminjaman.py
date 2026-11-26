"""
peminjaman.py
-------------
Fungsi: mengatur proses peminjaman alat.
  - cek_alat() : memeriksa satu alat (tidak menyimpan apa pun)
  - pinjam()   : meminjam BEBERAPA alat sekaligus dalam satu proses

Contoh satu proses: 2 resistor + 1 multimeter + 2 project board.

Aturan:
  1. NIM  harus valid (angka, 11 digit) dan sudah terdaftar.
  2. Setiap alat harus terdaftar, kondisinya baik, dan stok tersedia
     harus cukup untuk jumlah yang diminta.
  3. SEMUA ATAU TIDAK SAMA SEKALI: jika satu alat saja bermasalah,
     tidak ada alat yang dipinjam dan semua masalah ditampilkan.
"""

from datetime import date

from database import jalankan, ambil
from tambah_mahasiswa import nim_valid   # pemeriksaan NIM sudah ada di file ini


def cek_alat(kode, jumlah):
    """
    Memeriksa apakah satu alat boleh dipinjam sebanyak 'jumlah' unit.

    return: teks masalah, atau "" (kosong) jika aman
    """
    # Alat harus terdaftar
    alat = ambil("SELECT nama, jumlah, kondisi FROM alat WHERE kode = %s", (kode,))
    if not alat:
        return f"Alat {kode} tidak ditemukan"
    nama, stok, kondisi = alat[0]

    # Alat rusak tidak boleh dipinjam
    if kondisi == "rusak":
        return f"{nama} ({kode}) rusak, tidak bisa dipinjam"

    # Stok tersedia = stok total - total unit yang sedang dipinjam
    hasil = ambil(
        "SELECT COALESCE(SUM(jumlah), 0) FROM peminjaman "
        "WHERE kode_alat = %s AND status = 'dipinjam'",
        (kode,)
    )
    tersedia = stok - int(hasil[0][0])
    if jumlah > tersedia:
        return f"Stok {nama} ({kode}) tidak cukup: diminta {jumlah}, tersedia {tersedia}"

    return ""


def pinjam(nim, daftar_barang):
    """
    Mencatat peminjaman beberapa alat sekaligus oleh satu mahasiswa.

    nim           : NIM mahasiswa yang meminjam
    daftar_barang : list berisi (kode_alat, jumlah),
                    contoh: [("ED001", 2), ("ED009", 1), ("ED002", 2)]

    return: (berhasil, pesan)
    """
    nim = nim.strip()

    # 1. Keranjang tidak boleh kosong
    if not daftar_barang:
        return False, "Pilih minimal satu alat untuk dipinjam!"

    # 2. NIM wajib diisi, harus valid, dan sudah terdaftar
    if nim == "":
        return False, "NIM wajib diisi!"
    if not nim_valid(nim):
        return False, "NIM harus berupa angka dan 11 digit!"
    mhs = ambil("SELECT nama FROM mahasiswa WHERE nim = %s", (nim,))
    if not mhs:
        return False, f"NIM {nim} belum terdaftar!"
    nama_mhs = mhs[0][0]

    # 3. Periksa jumlah, lalu gabungkan alat yang kodenya sama
    total = {}   # bentuk: {kode_alat: jumlah}
    for kode, jumlah in daftar_barang:
        kode = kode.strip()
        if not str(jumlah).isdigit() or int(jumlah) <= 0:
            return False, f"Jumlah alat {kode} harus angka lebih dari 0!"
        total[kode] = total.get(kode, 0) + int(jumlah)

    # 4. Periksa SEMUA alat dulu, kumpulkan semua masalah
    masalah = []
    for kode, jumlah in total.items():
        pesan = cek_alat(kode, jumlah)
        if pesan != "":
            masalah.append(pesan)
    if masalah:
        return False, "Peminjaman dibatalkan:\n- " + "\n- ".join(masalah)

    # 5. Semua aman: simpan satu baris per jenis alat, tanggal hari ini
    for kode, jumlah in total.items():
        jalankan(
            "INSERT INTO peminjaman (nim, kode_alat, jumlah, tgl_pinjam) "
            "VALUES (%s, %s, %s, %s)",
            (nim, kode, jumlah, date.today())
        )
    return True, (f"{nama_mhs} berhasil meminjam {len(total)} jenis alat "
                  f"({sum(total.values())} unit).")


# Bagian ini hanya jalan jika file dijalankan langsung (untuk tes)
if __name__ == "__main__":
    from daftar import daftar_alat

    # Siapkan data sementara
    jalankan("INSERT INTO alat VALUES ('TES01', 'Resistor Tes', 3, 'baik')")
    jalankan("INSERT INTO alat VALUES ('TES02', 'Multimeter Tes', 1, 'baik')")
    jalankan("INSERT INTO alat VALUES ('TES03', 'Alat Rusak Tes', 2, 'rusak')")
    jalankan("INSERT INTO mahasiswa VALUES ('25037010099', 'TES MAHASISWA')")

    print(pinjam("25037010099", [("TES01", 2), ("TES02", 1)]))  # berhasil
    print(pinjam("25037010099", [("TES01", 2), ("TES02", 1)]))  # stok kurang, semua batal
    print(pinjam("25037010099", [("TES03", 1)]))                # alat rusak
    print(pinjam("2503701009A", [("TES01", 1)]))                # NIM ada huruf
    print(pinjam("25037010099", []))                            # keranjang kosong
    print(daftar_alat("TES0"))                                  # cek sisa stok

    # Bersihkan data tes (riwayat ikut terhapus otomatis)
    jalankan("DELETE FROM alat WHERE kode IN ('TES01', 'TES02', 'TES03')")
    jalankan("DELETE FROM mahasiswa WHERE nim = '25037010099'")