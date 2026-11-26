# Klasifikasi Prioritas Penanganan Wilayah Menggunakan Metode Simple Additive Weighting (SAW)

Program berbasis antarmuka teks (*command line*) yang dikembangkan dengan bahasa Python untuk menentukan kabupaten/kota yang perlu diprioritaskan dalam penanganan berdasarkan persentase stunting, persentase penduduk miskin, dan Indeks Pembangunan Manusia (IPM) tahun 2018. Setiap wilayah diberi nilai preferensi menggunakan metode Simple Additive Weighting (SAW), lalu dikelompokkan ke dalam tiga status prioritas: Tinggi, Sedang, dan Rendah.

## Daftar Isi

- [Latar Belakang](#latar-belakang)
- [Tujuan](#tujuan)
- [Fitur Utama](#fitur-utama)
- [Metodologi](#metodologi)
- [Struktur Repositori](#struktur-repositori)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Cara Menjalankan Program](#cara-menjalankan-program)
- [Panduan Penggunaan](#panduan-penggunaan)
- [Format Data](#format-data)
- [Keterbatasan](#keterbatasan)
- [Tim Pengembang](#tim-pengembang)

## Latar Belakang

Stunting masih menjadi salah satu masalah kesehatan utama di Indonesia dan berkaitan erat dengan kondisi ekonomi serta kualitas pembangunan manusia di suatu wilayah. Karena sumber daya untuk intervensi terbatas, pemerintah perlu menentukan wilayah mana yang paling membutuhkan penanganan lebih dulu. Program ini membantu proses tersebut dengan menggabungkan tiga indikator, yaitu persentase stunting, persentase penduduk miskin, dan IPM, menggunakan metode SAW sehingga setiap wilayah dapat dibandingkan secara terukur.

## Tujuan

1. Menghitung nilai preferensi setiap kabupaten/kota berdasarkan tiga kriteria menggunakan metode SAW.
2. Mengklasifikasikan wilayah ke dalam status prioritas Tinggi, Sedang, atau Rendah.
3. Menampilkan peringkat wilayah dari yang paling membutuhkan penanganan.
4. Menyediakan fitur penambahan data manual untuk menguji program dengan data baru.

## Fitur Utama

| No | Fitur | Keterangan |
|----|-------|------------|
| 1 | Login | Hanya anggota kelompok yang dapat masuk, dengan batas 3 kali percobaan. |
| 2 | Peringkat dan status | Menampilkan seluruh wilayah terurut dari nilai V tertinggi beserta statusnya. |
| 3 | Rekap status | Menampilkan jumlah wilayah pada setiap status (Tinggi, Sedang, Rendah). |
| 4 | Daftar prioritas Tinggi | Menampilkan wilayah yang paling perlu ditangani lebih dulu. |
| 5 | Cari berdasarkan provinsi | Menampilkan kabupaten/kota dalam provinsi yang dicari beserta peringkat dan statusnya. |
| 6 | Laporan data bermasalah | Menampilkan baris dataset yang ditolak beserta alasannya. |
| 7 | Tambah data wilayah | Menambahkan data kabupaten/kota secara manual, lalu seluruh nilai dihitung ulang. |

Seluruh validasi data dilakukan tanpa `try/except`.

## Metodologi

### 1. Kriteria dan Bobot

| Kriteria | Atribut | Bobot |
|----------|---------|-------|
| Persentase stunting | Benefit (semakin tinggi semakin diprioritaskan) | 1/3 |
| Persentase penduduk miskin | Benefit (semakin tinggi semakin diprioritaskan) | 1/3 |
| IPM | Cost (semakin rendah semakin diprioritaskan) | 1/3 |

### 2. Normalisasi

```
R-Stunting = Stunting / Stunting tertinggi
R-Miskin   = Miskin / Miskin tertinggi
R-IPM      = IPM terendah / IPM
```

### 3. Nilai Preferensi

```
V = (1/3 × R-Stunting) + (1/3 × R-Miskin) + (1/3 × R-IPM)
```

Nilai V dibulatkan 4 angka di belakang koma, lalu wilayah diurutkan dari V tertinggi ke terendah. Wilayah dengan nilai V sama mendapat peringkat yang sama.

### 4. Klasifikasi Status

| Nilai V | Status |
|---------|--------|
| V ≥ 0,70 | Tinggi |
| 0,50 ≤ V < 0,70 | Sedang |
| V < 0,50 | Rendah |

## Struktur Repositori

```
.
├── mini_project_saw.py      # Program utama
├── dataset_stunting.csv     # Dataset 52 kabupaten/kota tahun 2018
└── README.md                # Dokumentasi
```

## Persyaratan Sistem

- Python versi 3.6 atau yang lebih baru.
- Tidak memerlukan pustaka tambahan (hanya pustaka standar `csv` dan `os`).

## Cara Menjalankan Program

Kloning repositori:

```
git clone https://github.com/7ALSIK/Klasifikasi-Prioritas-Penanganan-Stunting.git
cd Klasifikasi-Prioritas-Penanganan-Stunting
```

Jalankan program:

```
python mini_project_saw.py
```

Pada sebagian sistem, gunakan perintah `python3`.

> **Catatan:** Jalankan program dari dalam direktori repositori agar berkas `dataset_stunting.csv` dapat terbaca.

## Panduan Penggunaan

1. **Login.** Masukkan nama anggota kelompok sebagai username dan NIM sebagai password. Username tidak membedakan huruf besar dan kecil.
2. **Menu Utama:**
   - **Menu 1 – Tampilkan peringkat dan status.**
   - **Menu 2 – Rekap jumlah wilayah per status.**
   - **Menu 3 – Daftar wilayah berstatus Tinggi.**
   - **Menu 4 – Cari berdasarkan provinsi.** Masukkan nama atau sebagian nama provinsi, misalnya `sumatera barat` atau `jawa`.
   - **Menu 5 – Laporan data bermasalah.**
   - **Menu 6 – Tambah data wilayah.** Masukkan provinsi, kabupaten/kota, persentase stunting, persentase miskin, dan IPM. Desimal boleh ditulis dengan titik atau koma.
   - **Menu 0 – Keluar.**

## Format Data

Berkas `dataset_stunting.csv` menggunakan format berikut.

| Kolom | Keterangan |
|-------|------------|
| PROVINSI | Nama provinsi. |
| KABKOTA | Nama kabupaten/kota. |
| PCT_STUNTING_2018 | Persentase stunting tahun 2018 (0–100). |
| PCT_MISKIN_2018 | Persentase penduduk miskin tahun 2018 (0–100). |
| IPM_2018 | Indeks Pembangunan Manusia tahun 2018 (lebih dari 0, maksimal 100). |
| FLAG_ANOMALI | Diisi `1` jika baris tidak ingin dihitung; dikosongkan jika normal. |

Contoh:

```
PROVINSI,KABKOTA,PCT_STUNTING_2018,PCT_MISKIN_2018,IPM_2018,FLAG_ANOMALI
BALI,Bangli,43.1,4.89,68.96,
```

Sumber data: dataset LR-SCTM (Mendeley Data), diambil 2 kabupaten/kota dari setiap provinsi.

## Keterbatasan

- Bobot ketiga kriteria bernilai sama (1/3) dan ambang klasifikasi bersifat tetap; keduanya dapat diubah melalui konstanta di bagian awal program.
- Normalisasi SAW bergantung pada nilai tertinggi dan terendah dataset, sehingga penambahan satu data ekstrem dapat mengubah status wilayah lain.
- Data yang ditambahkan melalui menu 6 hanya tersimpan selama program berjalan dan tidak ditulis ke berkas CSV.
- Akun login ditulis langsung di dalam program dan password belum dienkripsi; program ditujukan untuk keperluan pembelajaran.

## Tim Pengembang

**Kelompok 7A**

| No | Nama | NIM |
|----|------|-----|
| 1 | Hanif Alfi | 2610931029 |
| 2 | Shaloom Nadhira Utami Muliawan | 2610933038 |
| 3 | Yogi Andika | 2610933034 |
| 4 | Ardaffa Yazid Ilmany | 2610932036 |

Praktikum Programa Komputer 2026 – Laboratorium Sistem Informasi dan Keputusan, Departemen Teknik Industri, Universitas Andalas.
