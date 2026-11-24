<div align="center">

# 📚 Sistem Manajemen Tugas

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=38BDF8&center=true&vCenter=true&width=650&lines=Atur+tugas%2C+atur+prioritas.;Pantau+deadline%2C+selesaikan+target.;Satu+langkah+kecil+menuju+lebih+produktif." alt="Typing animation" />

**Aplikasi manajemen tugas sederhana berbasis Python dan Object-Oriented Programming.**

<br/>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Paradigm](https://img.shields.io/badge/Paradigm-OOP-7C3AED?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Project%20Akademik-22C55E?style=for-the-badge)

</div>

---

## ✨ Tentang Proyek

**Sistem Manajemen Tugas** adalah aplikasi berbasis terminal/CLI yang dibuat untuk membantu pengguna mencatat dan mengelola tugas. Pengguna dapat menambahkan tugas, menentukan tenggat dan prioritas, memperbarui progres, serta mencari tugas berdasarkan kata kunci.

Proyek ini dikembangkan menggunakan Python dengan pendekatan **Object-Oriented Programming (OOP)**. Struktur program dipisahkan menjadi modul pengelolaan data pengguna dan modul utama untuk interaksi dengan pengguna.

## 🚀 Fitur

| Fitur | Deskripsi |
|---|---|
| ➕ Tambah tugas | Menambahkan judul, deskripsi, tenggat, dan prioritas tugas. |
| 📋 Lihat tugas | Menampilkan seluruh tugas yang tersimpan. |
| ✏️ Ubah tugas | Memperbarui informasi tugas yang sudah dibuat. |
| 🔄 Ubah status | Mengatur status menjadi belum dikerjakan, sedang dikerjakan, atau selesai. |
| ✅ Tandai selesai | Mengubah status tugas menjadi selesai secara langsung. |
| 🗑️ Hapus tugas | Menghapus tugas berdasarkan ID setelah konfirmasi. |
| 🔎 Cari tugas | Mencari tugas berdasarkan kata kunci pada judul atau deskripsi. |
| 🧩 Filter tugas | Menyaring tugas berdasarkan status atau prioritas. |
| ⏰ Cek keterlambatan | Menampilkan tugas yang tenggatnya sudah lewat dan belum selesai. |

## 🛠️ Teknologi

- **Python 3** — bahasa pemrograman utama.
- **OOP (Object-Oriented Programming)** — pengorganisasian program menggunakan class, object, atribut, dan method.
- **Python Standard Library**
  - `datetime` untuk validasi tanggal dan pemeriksaan tenggat.

Tidak memerlukan instalasi library eksternal.

## 📁 Struktur Proyek

```text
PROYEK AKHIR PBO/
│
├── main.py       # Menu utama dan interaksi melalui terminal
├── pengguna.py   # Class Pengguna dan pengelolaan data tugas
└── README.md     # Dokumentasi proyek
```

### Peran setiap file

- **`pengguna.py`**  
  Berisi class `Pengguna`, atribut untuk menyimpan identitas dan daftar tugas, validasi data, serta method untuk menambah, menampilkan, mengubah, menghapus, mencari, dan memfilter tugas.

- **`main.py`**  
  Menangani input dan output, menampilkan menu, serta memanggil method dari object `Pengguna`.

## ⚙️ Cara Menjalankan

### 1. Pastikan Python sudah terpasang

Periksa melalui terminal:

```bash
python --version
```

Jika perintah tersebut tidak dikenali di Windows, coba:

```bash
py --version
```

### 2. Clone repository

```bash
git clone URL_REPOSITORY_KAMU
```

Ganti `URL_REPOSITORY_KAMU` dengan URL repository GitHub proyek ini.

### 3. Masuk ke folder proyek

```bash
cd "PROYEK AKHIR PBO"
```

### 4. Jalankan program

```bash
python main.py
```

Atau di Windows:

```bash
py main.py
```

## 🖥️ Gambaran Menu

Saat program dijalankan, pengguna akan diminta memasukkan nama. Setelah itu, menu utama menyediakan pilihan berikut:

```text
=== SISTEM MANAJEMEN TUGAS ===
Pengguna: Nama Pengguna (ID 1)

1. Tambah tugas
2. Lihat semua tugas
3. Ubah tugas
4. Ubah status tugas
5. Tandai tugas selesai
6. Hapus tugas
7. Cari tugas
8. Filter tugas
9. Cek tugas terlambat
0. Keluar
```

**Format tenggat:** `YYYY-MM-DD`  
Contoh: `2026-12-31`

**Pilihan prioritas:** rendah, sedang, tinggi.

**Pilihan status:** belum dikerjakan, sedang dikerjakan, selesai.

## 🧠 Konsep OOP yang Digunakan

| Konsep | Penerapan dalam proyek |
|---|---|
| Class | Class `Pengguna` menjadi cetak biru object pengguna. |
| Object | Object `pengguna` dibuat di dalam fungsi `main()`. |
| Encapsulation | Atribut seperti `__nama` dan `__daftar_tugas` dibuat private. |
| Constructor | `__init__()` menginisialisasi data awal object. |
| Method | Method mengelola operasi tugas, misalnya `tambah_tugas()` dan `hapus_tugas()`. |
| Property | `@property` dan setter digunakan untuk mengakses serta memvalidasi atribut tertentu. |

## 📌 Catatan Pengembangan

Versi saat ini menyimpan daftar tugas **di dalam memori program**. Artinya, data tugas belum disimpan secara permanen ke file atau database. Ketika program ditutup, data yang dibuat selama sesi tersebut akan hilang.

Aplikasi ini masih berbasis terminal (CLI), belum menggunakan GUI atau integrasi database.

## 🎯 Tujuan Proyek

Proyek ini dibuat sebagai bagian dari pembelajaran mata kuliah **Pemrograman Berbasis Objek (PBO)**, dengan fokus pada penerapan konsep dasar OOP melalui studi kasus pengelolaan tugas.

---

<div align="center">

**Made with 🐍 Python**

*Plan your tasks. Set your priorities. Get things done.*

</div>
