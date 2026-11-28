# Sistem Inventaris & Peminjaman Alat Laboratorium Fisika

Aplikasi desktop untuk mengelola inventaris dan peminjaman alat Laboratorium Fisika. Dibuat dengan **Python (Tkinter)** dan **MySQL (XAMPP)**, memakai GUI yang bisa diklik.

Tugas besar Dasar Pemrograman, Program Studi Fisika, Universitas Pembangunan Nasional "Veteran" Jawa Timur.

## Anggota

- Gigih Ridho Apriansyah
- Adam Maulana
- Gorgena Vicario Angel
- Fitri Julia Hasanah
- Syafika Aiyuni

## Fitur

- **Data Alat**: tambah, ubah, hapus, cari, dan lihat stok tersedia. Alat rusak ditandai merah.
- **Data Mahasiswa**: tambah, ubah, hapus, dan cari berdasarkan NIM/nama. Mahasiswa yang sedang meminjam ditandai oranye.
- **Peminjaman multi-alat**: satu proses bisa meminjam banyak jenis alat dengan jumlah per alat (sistem keranjang).
- **Pengembalian**: pilih satu atau banyak peminjaman sekaligus, lalu kembalikan.
- **Riwayat**: seluruh transaksi (dipinjam dan dikembalikan), bisa dicari.
- **Pengaman koneksi**: jika MySQL belum menyala, muncul pesan "Nyalakan MySQL di XAMPP dulu!".

## Aturan Sistem

- Alat tidak bisa dipinjam jika stok habis atau kondisinya `rusak`.
- NIM harus angka dan tepat **11 digit**, serta sudah terdaftar.
- Stok tersedia = jumlah total − jumlah yang sedang dipinjam.
- Peminjaman **semua atau tidak sama sekali**: jika satu alat bermasalah, tidak ada yang dipinjam dan semua masalah ditampilkan.
- Satu proses peminjaman menghasilkan satu baris `peminjaman` per jenis alat.
- Alat atau mahasiswa yang masih dipinjam **tidak boleh dihapus**. Jika hanya punya riwayat lama, boleh dihapus dan riwayatnya ikut terhapus (`ON DELETE CASCADE`).
- Kode alat dan NIM adalah kunci data, sehingga tidak bisa diubah.

## Teknologi

| Komponen | Keterangan |
|---|---|
| Bahasa | Python 3 |
| GUI | Tkinter (`ttk.Notebook`, `ttk.Treeview`) |
| Database | MySQL / MariaDB (XAMPP), dikelola lewat phpMyAdmin |
| Library | `mysql-connector-python` |

## Struktur Folder

```
TUBES DASPRO/
├── database/
│   ├── file.sql      # struktur database (CREATE TABLE)
│   ├── data.sql      # data asli: 111 alat dan 54 mahasiswa
│   └── link.sql      # SQL pendukung
└── inventaris/
    ├── main.py              # pintu masuk program
    ├── gui.py               # jendela utama + 5 tab
    ├── gui_alat.py          # tab Data Alat
    ├── gui_mahasiswa.py     # tab Data Mahasiswa
    ├── gui_peminjaman.py    # tab Peminjaman (keranjang)
    ├── gui_pengembalian.py  # tab Pengembalian
    ├── gui_riwayat.py       # tab Riwayat
    ├── database.py          # koneksi MySQL
    ├── tambah_alat.py       # logika tambah alat
    ├── tambah_mahasiswa.py  # logika tambah mahasiswa + validasi NIM
    ├── update.py            # logika ubah alat dan mahasiswa
    ├── hapus.py             # logika hapus alat dan mahasiswa
    ├── daftar.py            # logika membaca data (daftar, stok, riwayat)
    ├── peminjaman.py        # logika pinjam (multi-alat)
    └── pengembalian.py      # logika kembali
```

## Alur Program

```
main.py -> gui.py -> tab (gui_*.py) -> file logika -> database.py -> MySQL
```

Setiap file GUI hanya mengurus tampilan. Aturan dan perintah SQL ada di file logika, sehingga mudah dibaca dan dites sendiri-sendiri.

## Cara Menjalankan

### 1. Persiapan

1. Pasang [XAMPP](https://www.apachefriends.org/) dan Python 3.
2. Pasang library:
   ```bash
   pip install mysql-connector-python
   ```
3. Buka XAMPP Control Panel, klik **Start** pada **MySQL** (dan Apache jika ingin memakai phpMyAdmin).

### 2. Buat database

Buka phpMyAdmin (contoh: `http://localhost:8080/phpmyadmin`), masuk ke tab **SQL**, lalu jalankan skema di bawah.

```sql
CREATE DATABASE IF NOT EXISTS inventaris_laboratorium;
USE inventaris_laboratorium;

-- Tabel alat: stok dan kondisi alat laboratorium
CREATE TABLE alat (
  kode    VARCHAR(10) PRIMARY KEY,           -- kode unik, contoh: ED001
  nama    VARCHAR(50) NOT NULL,              -- nama alat
  jumlah  INT NOT NULL,                      -- total stok
  kondisi ENUM('baik','rusak') NOT NULL      -- hanya 'baik' atau 'rusak'
) ENGINE = InnoDB;

-- Tabel mahasiswa: data peminjam
CREATE TABLE mahasiswa (
  nim  VARCHAR(15) PRIMARY KEY,              -- NIM/NPM unik (11 digit)
  nama VARCHAR(50) NOT NULL
) ENGINE = InnoDB;

-- Tabel peminjaman: riwayat pinjam dan kembali
CREATE TABLE peminjaman (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  nim         VARCHAR(15) NOT NULL,          -- siapa yang meminjam
  nama        VARCHAR(50) NOT NULL,          -- nama peminjam (disalin saat meminjam)
  kode_alat   VARCHAR(10) NOT NULL,          -- alat yang dipinjam
  jumlah      INT NOT NULL DEFAULT 1,        -- jumlah unit
  tgl_pinjam  DATE NOT NULL,
  tgl_kembali DATE NULL,                     -- kosong sampai dikembalikan
  status      ENUM('dipinjam','dikembalikan') DEFAULT 'dipinjam',
  CONSTRAINT fk_pinjam_mahasiswa FOREIGN KEY (nim)
      REFERENCES mahasiswa(nim) ON DELETE CASCADE,
  CONSTRAINT fk_pinjam_alat FOREIGN KEY (kode_alat)
      REFERENCES alat(kode) ON DELETE CASCADE
) ENGINE = InnoDB;
```

Opsional, view untuk melihat nama alat dan mahasiswa di phpMyAdmin:

```sql
CREATE VIEW v_peminjaman AS
SELECT p.id, p.nim, p.nama AS nama_mahasiswa,
       p.kode_alat, a.nama AS nama_alat,
       p.jumlah, p.tgl_pinjam, p.tgl_kembali, p.status
FROM peminjaman p
JOIN alat a ON p.kode_alat = a.kode;
```

### 3. Isi data awal

Di phpMyAdmin, pilih database `inventaris_laboratorium`, buka tab **Impor**, lalu pilih `database/data.sql`.
Data berisi **111 alat** (Elektronika Dasar, Biologi Dasar, Kimia Dasar, Fisika Dasar) dan **54 mahasiswa** Fisika. Semua alat berkondisi `baik`.

### 4. Atur koneksi

Pengaturan bawaan di `inventaris/database.py`:

| Pengaturan | Nilai |
|---|---|
| host | `localhost` |
| user | `root` |
| password | (kosong) |
| port | `3306` |
| database | `inventaris_laboratorium` |

Ubah jika konfigurasi XAMPP kamu berbeda.

### 5. Jalankan

```bash
cd inventaris
python main.py
```

Atau buka `main.py` di VS Code lalu klik **Run**.

## Cara Pakai

1. **Data Alat / Data Mahasiswa**: isi form lalu klik **Tambah**. Klik satu baris untuk mengisi form, lalu **Ubah** atau **Hapus**. Klik **Bersihkan** untuk mengosongkan form.
2. **Peminjaman**: ketik NIM (nama muncul otomatis), pilih alat, isi jumlah, klik **Tambah ke Keranjang**, ulangi untuk alat lain, lalu **Pinjam Semua**.
3. **Pengembalian**: pilih satu atau beberapa baris (Ctrl/Shift + klik), lalu klik **Kembalikan**.
4. **Riwayat**: lihat semua transaksi. Yang masih dipinjam berwarna oranye.

Untuk demo alat rusak: ubah kondisi satu alat menjadi `rusak` lewat tombol **Ubah**, lalu coba pinjam alat itu. Sistem akan menolak.

## Catatan Desain

- Database dinormalisasi lewat tabel `alat`, `mahasiswa`, dan `peminjaman` yang dihubungkan foreign key.
- Kolom `nama` di `peminjaman` sengaja disalin dari `mahasiswa` saat meminjam, supaya riwayat langsung terbaca di phpMyAdmin. Jika nama mahasiswa diubah lewat aplikasi, `update.py` ikut memperbarui nama di `peminjaman`, sehingga data tetap sinkron.
- Kode alat dan NIM dipakai sebagai `iid` di `ttk.Treeview` agar angka 0 di depan tidak hilang.
- Query stok memakai `CAST(... AS SIGNED)` dan `COALESCE(SUM(...), 0)` agar hasilnya bilangan bulat, bukan `Decimal` atau `NULL`.
- Blok `if __name__ == "__main__":` di tiap file dipakai untuk tes mandiri. File saling terhubung lewat `import`.

## Masalah Umum

| Pesan / gejala | Penyebab dan solusi |
|---|---|
| `2003 ... 10061 actively refused it` | MySQL di XAMPP belum di-Start. |
| `1049 Unknown database` | Database belum dibuat, atau nama di `database.py` tidak sama dengan di phpMyAdmin. |
| File `.sql` berwarna merah di VS Code | File tanpa ekstensi dianggap Python. Ganti namanya menjadi `.sql`. |
| Relasi `ON DELETE CASCADE` hilang | Pastikan semua tabel `InnoDB`, lalu pasang ulang constraint dengan `ALTER TABLE ... ADD CONSTRAINT`. |

## Screenshot

<img width="753" height="470" alt="image" src="https://github.com/user-attachments/assets/80022138-0e01-43c1-ac30-6a15a2e0099b" />
<img width="755" height="476" alt="Screenshot 2026-11-29 000729" src="https://github.com/user-attachments/assets/49019821-9c34-499f-bde3-aecdc21f27fe" />

