# koneksi ke MySQL (XAMPP) + fungsi query

"""
database.py
-----------
Fungsi: menghubungkan program Python ke database MySQL (XAMPP).
File lain tidak perlu tahu cara konek, cukup memanggil
fungsi jalankan() dan ambil() dari file ini.
"""

import mysql.connector


def koneksi():
    """Membuka koneksi ke database lab_fisika di MySQL XAMPP."""
    return mysql.connector.connect(
        host="localhost",      # MySQL berjalan di komputer sendiri
        user="root",           # user bawaan XAMPP
        password="",           # password bawaan XAMPP kosong
        database="lab_fisika"  # nama database yang kita buat
    )


def jalankan(sql, data=()):
    """
    Menjalankan perintah yang MENGUBAH data (INSERT, UPDATE, DELETE).

    sql  : perintah SQL, nilai diganti tanda %s
    data : isi nilai untuk tanda %s, berbentuk tuple
    return: jumlah baris yang berubah
    """
    con = koneksi()
    cur = con.cursor()
    try:
        cur.execute(sql, data)
        con.commit()          # simpan perubahan ke database
        return cur.rowcount
    finally:
        cur.close()           # selalu tutup koneksi setelah selesai
        con.close()


def ambil(sql, data=()):
    """
    Menjalankan perintah yang MEMBACA data (SELECT).

    return: list berisi baris-baris hasil query
    """
    con = koneksi()
    cur = con.cursor()
    try:
        cur.execute(sql, data)
        return cur.fetchall()
    finally:
        cur.close()
        con.close()


# Bagian ini hanya jalan jika file dijalankan langsung (untuk tes koneksi)
if __name__ == "__main__":
    print("Tabel di database:", ambil("SHOW TABLES"))