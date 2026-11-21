-- =====================================================
-- Database : lab_fisika
-- Fungsi   : menyimpan data alat, mahasiswa, dan
--            transaksi peminjaman laboratorium fisika
-- =====================================================

-- Membuat database, lalu memakainya
CREATE DATABASE lab_fisika;
USE lab_fisika;

-- -----------------------------------------------------
-- Tabel alat : data stok alat laboratorium
-- -----------------------------------------------------
CREATE TABLE alat (
  kode VARCHAR(10) PRIMARY KEY,        -- kode unik alat, contoh: A001
  nama VARCHAR(50) NOT NULL,           -- nama alat, contoh: Multimeter
  jumlah INT NOT NULL,                 -- total stok alat
  kondisi ENUM('baik','rusak') NOT NULL  -- hanya boleh 'baik' atau 'rusak'
);

-- -----------------------------------------------------
-- Tabel mahasiswa : data peminjam
-- -----------------------------------------------------
CREATE TABLE mahasiswa (
  nim VARCHAR(15) PRIMARY KEY,         -- NIM/NPM unik tiap mahasiswa
  nama VARCHAR(50) NOT NULL            -- nama mahasiswa
);

-- -----------------------------------------------------
-- Tabel peminjaman : riwayat pinjam dan kembali
-- -----------------------------------------------------
CREATE TABLE peminjaman (
  id INT AUTO_INCREMENT PRIMARY KEY,   -- nomor transaksi, naik otomatis
  nim VARCHAR(15) NOT NULL,            -- siapa yang meminjam
  kode_alat VARCHAR(10) NOT NULL,      -- alat yang dipinjam
  tgl_pinjam DATE NOT NULL,            -- tanggal pinjam
  tgl_kembali DATE NULL,               -- kosong sampai alat dikembalikan
  status ENUM('dipinjam','dikembalikan') DEFAULT 'dipinjam',

  -- Relasi antar tabel: NIM dan kode alat harus sudah terdaftar.
  -- ON DELETE CASCADE: jika mahasiswa/alat dihapus,
  -- riwayat peminjamannya ikut terhapus.
  FOREIGN KEY (nim) REFERENCES mahasiswa(nim) ON DELETE CASCADE,
  FOREIGN KEY (kode_alat) REFERENCES alat(kode) ON DELETE CASCADE
);