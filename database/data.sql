-- =====================================================
-- Data asli : daftar alat laboratorium dan mahasiswa
-- Sumber    : 5 file PDF "Daftar Alat Laboratorium"
-- =====================================================

-- Hapus data contoh lebih dulu (riwayat peminjaman ikut terhapus)
DELETE FROM peminjaman;
DELETE FROM alat;
DELETE FROM mahasiswa;

-- -----------------------------------------------------
-- ALAT : Elektronika Dasar (kode ED)
-- Kolom : kode, nama, jumlah, kondisi
-- -----------------------------------------------------
INSERT INTO alat (kode, nama, jumlah, kondisi) VALUES
('ED001', 'resistor', 1, 'baik'),
('ED002', 'project board', 1, 'baik'),
('ED003', 'osiloskop analog', 1, 'baik'),
('ED004', 'osiloskop digital', 1, 'baik'),
('ED005', 'catu daya', 1, 'baik'),
('ED006', 'capit buaya', 1, 'baik'),
('ED007', 'kabel penghubung', 1, 'baik'),
('ED008', 'bohlam', 1, 'baik'),
('ED009', 'multimeter digital', 1, 'baik'),
('ED010', 'mutimeter analog', 1, 'baik'),
('ED011', 'solder', 1, 'baik'),
('ED012', 'pcb', 1, 'baik'),
('ED013', 'papan kayu', 1, 'baik'),
('ED014', 'AFG', 1, 'baik');

-- -----------------------------------------------------
-- ALAT : Biologi Dasar (kode BD)
-- -----------------------------------------------------
INSERT INTO alat (kode, nama, jumlah, kondisi) VALUES
('BD001', 'mikroskop', 1, 'baik'),
('BD002', 'preparat hewan', 1, 'baik'),
('BD003', 'preparat tumbuhan', 1, 'baik'),
('BD004', 'kompor listrik', 1, 'baik'),
('BD005', 'pinset', 1, 'baik'),
('BD006', 'gelas beaker 100ml', 1, 'baik'),
('BD007', 'thermometer', 1, 'baik'),
('BD008', 'cawan petri', 1, 'baik'),
('BD009', 'mortar dan stamper', 1, 'baik'),
('BD010', 'gelas ukur', 1, 'baik'),
('BD011', 'corong pemisah', 1, 'baik'),
('BD012', 'Termometer Air', 1, 'baik'),
('BD013', 'Termometer Tanah', 1, 'baik'),
('BD014', 'Batang Besi', 1, 'baik'),
('BD015', 'gelas beaker 50ml', 1, 'baik'),
('BD016', 'gelas beaker 500ml', 1, 'baik'),
('BD017', 'kertas filter', 1, 'baik');

-- -----------------------------------------------------
-- ALAT : Kimia Dasar (kode KDI / KDII)
-- -----------------------------------------------------
INSERT INTO alat (kode, nama, jumlah, kondisi) VALUES
('KDI001', 'gelas beaker 500ml', 1, 'baik'),
('KDI002', 'thermometer', 1, 'baik'),
('KDI003', 'cawan petri', 1, 'baik'),
('KDI004', 'biuret', 1, 'baik'),
('KDI005', 'pH meter', 1, 'baik'),
('KDI006', 'erlenmenyer', 1, 'baik'),
('KDI007', 'gelas ukur', 1, 'baik'),
('KDI008', 'tabung reaksi', 1, 'baik'),
('KDI009', 'pipet tetes', 1, 'baik'),
('KDI010', 'capit', 1, 'baik'),
('KDI011', 'kaki tiga', 1, 'baik'),
('KDI012', 'rak tabung reaksi', 1, 'baik'),
('KDI013', 'kaca arloji', 1, 'baik'),
('KDI014', 'jembatan garam', 1, 'baik'),
('KDI015', 'bunsen spirtus', 1, 'baik'),
('KDI016', 'neraca analitik', 1, 'baik'),
('KDI017', 'spatula', 1, 'baik'),
('KDI018', 'pengaduk', 1, 'baik'),
('KDI019', 'ph paper', 1, 'baik'),
('KDI020', 'kompor listrik', 1, 'baik'),
('KDI021', 'buret', 1, 'baik'),
('KDI022', 'gelar beaker 100ml', 1, 'baik'),
('KDI023', 'gelar beaker 50ml', 1, 'baik'),
('KDII024', 'rak tabung reaksi', 1, 'baik'),
('KDII025', 'penjepit', 1, 'baik'),
('KDII026', 'baterai', 1, 'baik'),
('KDII027', 'capit buaya', 1, 'baik'),
('KDII028', 'elektroda zn dan cu', 1, 'baik'),
('KDII029', 'larutan iodin', 1, 'baik'),
('KDII030', 'benedict', 1, 'baik'),
('KDII031', 'caco3', 1, 'baik'),
('KDII032', 'aquades', 1, 'baik'),
('KDII033', 'hcl', 1, 'baik');

-- -----------------------------------------------------
-- ALAT : Fisika Dasar (kode FDI / FDII)
-- -----------------------------------------------------
INSERT INTO alat (kode, nama, jumlah, kondisi) VALUES
('FDI01', '1 set pesawat atwood', 3, 'baik'),
('FDI02', 'pegas penumbuk', 4, 'baik'),
('FDI03', 'neraca analitik', 1, 'baik'),
('FDI04', 'pasak penumbuk', 4, 'baik'),
('FDI05', 'stopwatch', 1, 'baik'),
('FDI06', 'busur', 1, 'baik'),
('FDI07', 'multimeter analog', 2, 'baik'),
('FDI08', 'multimeter digital', 2, 'baik'),
('FDI09', 'statif', 1, 'baik'),
('FDI10', 'penggaris', 1, 'baik'),
('FDI11', 'meteran', 1, 'baik'),
('FDI12', 'mikrometer skrup', 3, 'baik'),
('FDI13', 'neraca ohaus', 2, 'baik'),
('FDI14', 'jangka sorong', 2, 'baik'),
('FDI15', 'rel kereta dinamika', 2, 'baik'),
('FDI16', 'beban 10 gram', 1, 'baik'),
('FDI17', 'beban 25 gram', 1, 'baik'),
('FDI18', 'beban 50 gram', 1, 'baik'),
('FDI19', 'beban bandul', 2, 'baik'),
('FDI20', 'catu daya', 4, 'baik'),
('FDI21', 'kabel penghubung hitam merah', 1, 'baik'),
('FDI22', 'kereta dinamika', 4, 'baik'),
('FDI23', 'gunting', 1, 'baik'),
('FDI24', 'pita petik', 1, 'baik'),
('FDI25', 'pewaktu petik', 1, 'baik'),
('FDI26', 'pegas', 2, 'baik'),
('FDI27', 'bandul matematis', 2, 'baik'),
('FDI28', 'tali', 1, 'baik'),
('FDI29', 'neraca ohaous 3 lengan', 1, 'baik'),
('FDII30', 'rel presisi', 1, 'baik'),
('FDII31', 'laser', 1, 'baik'),
('FDII32', 'busur derajat', 1, 'baik'),
('FDII33', 'cermin datar', 2, 'baik'),
('FDII34', 'slide diafragma', 1, 'baik'),
('FDII35', 'layar', 1, 'baik'),
('FDII36', 'tumpakan', 1, 'baik'),
('FDII37', 'tumpakan berpenjepit', 1, 'baik'),
('FDII38', 'lensa cembung', 1, 'baik'),
('FDII39', 'cermin kombinasi', 1, 'baik'),
('FDII40', 'resistor (kotak)', 2, 'baik'),
('FDII41', 'project board', 1, 'baik'),
('FDII42', 'prisma sama sisi', 1, 'baik'),
('FDII43', 'prisma siku siku', 1, 'baik'),
('FDII44', 'papan alas/sterofoam', 1, 'baik'),
('FDII45', 'kotak sklar', 1, 'baik'),
('FDII46', 'kotak penghubung', 1, 'baik'),
('FDII47', 'jepit buaya bersteker', 2, 'baik');

-- -----------------------------------------------------
-- MAHASISWA : 54 mahasiswa Fisika
-- Kolom : nim (NPM), nama
-- Tanda '' pada FA''IZIN = cara menulis tanda petik di SQL
-- -----------------------------------------------------
INSERT INTO mahasiswa (nim, nama) VALUES
('25037010001', 'NIRINA ALIVIA SAPUTRI'),
('25037010002', 'AULYA ANNAFI'),
('25037010004', 'BUNGA KAYLA ALMEIRA'),
('25037010005', 'ISAURA SAIDAH'),
('25037010006', 'NUHA ZAHIRAH ROSSY HANDRATNO'),
('25037010007', 'CITRA PRAMUDYA LESTARI'),
('25037010008', 'MUTIARA RACHMATUL DEA FEBYANA'),
('25037010010', 'HABIBAH AR RACHMAH'),
('25037010011', 'APRILLIA PUSPITA SARI'),
('25037010012', 'KHIRZA MILLATIA'),
('25037010013', 'NAUFAL AZIS SAPUTRA'),
('25037010014', 'FITRI OKTAVIA WULANHARI'),
('25037010015', 'NAYLA ALVIRA NAZIELA CHEASA'),
('25037010016', 'DWI AHMAD ALFARIED'),
('25037010018', 'DEVIANA NUR WIDYA HARTANTO'),
('25037010019', 'MUHAMMAD AKMAL RAGA AKSANA'),
('25037010020', 'ANIS PUJI NUR KHOFIFAH'),
('25037010021', 'ANNISA MIRA ANWARI'),
('25037010022', 'ALEYDA HILWA NUR FARIZA'),
('25037010024', 'MUHAMMAD RAHUL DEAN TEGAR PRATAMA'),
('25037010025', 'ADINDA SEPTIA RANI'),
('25037010026', 'AHMAD FAHMI IDRIS'),
('25037010027', 'CLAUDIA OLIVIA PUTRI'),
('25037010028', 'SELFI PUTRI LESMANA'),
('25037010029', 'WARDATUS ELVIABELLA AVIANTY'),
('25037010030', 'ADERIN KELDA RAMADANI'),
('25037010031', 'VIONA PUTRI RAHARDIAN'),
('25037010032', 'FAIZA SALSABILLA'),
('25037010033', 'CHELSY CITRA JELITA'),
('25037010034', 'GIGIH RIDHO APRIANSYAH'),
('25037010035', 'AZWAN FA''IZIN AL FARIZY'),
('25037010036', 'ANDIKA PUTRA ISWANTO'),
('25037010037', 'MUHAMMAD FAHRI RIZAL'),
('25037010038', 'AHMAD TEGAR FIRDAUS'),
('25037010039', 'ENDANG NUR KHASANAH'),
('25037010041', 'NABILA PUTRI WAHYUDI'),
('25037010042', 'FITRI JULIA HASANAH'),
('25037010043', 'ATHAYA GUSTY SHARAPOVA'),
('25037010044', 'KHOFIFA DEWI MAYASARI'),
('25037010045', 'WINDA NURUL PUTRI'),
('25037010046', 'NAILA NOVITA SARI'),
('25037010047', 'GORGENA VICARIO ANGEL'),
('25037010048', 'DZAKI AR ROMSI PRASETYO'),
('25037010050', 'MUHAMMAD FARIS AMRULLAH'),
('25037010051', 'SAMGAR CHRISNALD SATRIABUDI'),
('25037010052', 'ADAM MAULANA'),
('25037010053', 'BAGAS DHARMAJAYA'),
('25037010054', 'MOCHAMMAD AFIF MUROBBIN'),
('25037010055', 'AZIZAH JULIA IZZATTI ABELVANA IGNACIA'),
('25037010057', 'FAIZ AZKA RADITYA'),
('25037010059', 'MUHAMMAD AKBAR MAULANA'),
('25037010060', 'SYAFIKA AIYUNI'),
('25037010061', 'DESY KHIRANI PUTRI'),
('25037010062', 'ANDRA DEWANGGA PUTRA WINTORO');