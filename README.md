# Sistem Antrian Pasien Berbasis Prioritas

Repositori ini berisi proyek simulasi sistem antrian pasien untuk layanan ambulans yang dikembangkan sebagai bagian dari mata kuliah **Struktur Data dan Algoritma**. Aplikasi ini menggunakan bahasa Python dan mengimplementasikan struktur data **priority queue** (`heapq`) untuk mengelola tingkat keparahan pasien (hijau, kuning, merah).

Program berjalan di terminal dan menyediakan fitur seperti pendaftaran pasien, pencarian data pasien, pengelolaan ambulans, dan estimasi waktu kedatangan berdasarkan tingkat keparahan.

## Fitur Utama:
- Manajemen antrian pasien berdasarkan prioritas (red > yellow > green)
- Simulasi kedatangan ambulans menggunakan multithreading (`Timer`)
- Estimasi waktu tunggu berdasarkan tingkat keparahan
- Pencarian pasien berdasarkan nama
- Antarmuka berbasis teks yang interaktif

## Bahasa & Tools:
- Python 3.x
- Modul: `heapq`, `threading`, `datetime`

