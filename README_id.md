# Navigation
* [Tentang](#-zenvix-launcher--game-launcher)
* [Fitur Utama](#-fitur-utama)
* [Prasyarat dan Dependensi](#%EF%B8%8F-prasyarat-&-dependensi)
* [Struktur Projek](#-struktur-direktori-proyek)
* [Cara Menjalankan](#-cara-menjalankan)
* [Konfigurasi Warna](#-konfigurasi-warna-&-gaya-style-guide)
* [Lisensi](#-lisensi)

## Language / Bahasa
* [Indonesia](URL)
* [English](URL)


---

# 🚀 ZENVIX Launcher // Game Launcher

Game Launcher adalah aplikasi desktop berbasis **Python 3** dan **Tkinter** yang dirancang untuk mengelola dan meluncurkan koleksi game Anda dari satu tempat. Antarmuka aplikasi ini mengusung tema **Futuristic Cyberpunk / Tactical Tech** yang terinspirasi dari gaya UI *Arknights: Endfield*, dengan dominasi warna *matte charcoal* pekat dan aksen Kuning Stabilo (`#dfff00`).

---

## ⚡ Fitur Utama

- **UI / UX**: Tampilan gelap (*matte black/panel charcoal*) yang modern dan bersih dengan kontras tinggi untuk kenyamanan mata.
- **Dynamic Button Transition**: Tombol utama **JALANKAN GAME** memiliki efek animasi transisi warna yang meredup menjadi lebih gelap saat dilewati oleh pointer mouse (*hover effect*), meniru fungsionalitas sistem HUD militer.
- **Manajemen Game Komprehensif**: Fitur lengkap untuk Menambah, Mengedit, Menghapus, dan Menjalankan game secara instan.
- **Pemindaian Folder Otomatis (Auto Scan)**: Mampu memindai seluruh isi folder untuk mendeteksi file eksekutor game (`.exe`, `.sh`, `.bat`, dll.) sekaligus mencari file ikon yang cocok secara otomatis.
- **Sistem Salin & Manajemen Ikon Lokal**: Menyalin ikon game secara otomatis ke dalam direktori lokal (`icons/`) dan menggunakan metode *caching* (via *Pillow*) agar performa pemuatan tabel tetap lancar dengan tinggi baris (`rowheight=42`) yang lega.
- **Dukungan Lintas Platform (Wine Integration)**: Mendeteksi sistem operasi secara otomatis. Di sistem Linux, tersedia opsi integrasi untuk menjalankan file *executable* Windows (`.exe`) menggunakan **Wine** langsung dari launcher.
- **Smart Center Windows**: Perbaikan kalkulasi geometri yang memastikan jendela utama, jendela dialog tambah/edit, serta jendela penjelajah file (*File Dialog*) selalu muncul tepat di tengah layar atau di atas jendela induknya.

---

## 🛠️ Prasyarat & Dependensi

Pastikan perangkat Anda sudah terinstal **Python 3**. Untuk performa rendering visual ikon game yang maksimal, sangat disarankan untuk menginstal pustaka **Pillow (PIL)**.

### Instalasi Dependensi (Linux / Windows)

```bash
pip install Pillow

```

*Catatan untuk pengguna Linux:* Jika Tkinter belum terpasang secara bawaan di sistem Anda, instal melalui package manager:
#### Ubuntu / Debian / Mint
```bash
# Ubuntu / Debian / Mint
sudo apt install python3-tk
```
#### Arch Linux / Manjaro
```bash
# Arch Linux
sudo pacman -S tk
```
#### Fedora
```bash
sudo dnf install python3-tkinter
```
#### CentOS / RHEL
```bash
sudo yum install python3-tkinter
```

*Catatan untuk pengguna Linux:* Jika Python mengalami masalah atau kendala, disarankan menggunakan venv atau Virtual Environment:
### Instalasi Venv
#### Ubuntu / Debian / Mint
```bash
# Ubuntu / Debian / Mint
sudo apt update
sudo apt install python3-venv
```
#### Fedora
```bash
sudo dnf install python3-venv
```
#### Arch Linux
*The module is usually included with the python package, but you can also use python-virtualenv if preferred.*

### Membuat Lingkungan Virtual / Virtual Environment
```bash
python3 -m venv .venv
```
### Mengaktifkan Venv
```bash
source .venv/bin/activate
```
### Keluar dari venv
```bash
deactivate
```

---

## 📂 Struktur Direktori Proyek

Setelah dijalankan pertama kali, aplikasi akan otomatis membuat file konfigurasi data dan folder penyimpanan ikon secara lokal:

```text
GameLauncher/
├── game_launcher.py  # Berkas kode utama aplikasi
├── games.json        # Database lokal penyimpanan data game (Format JSON)
└── icons/            # Direktori penyimpanan dan cache ikon game

```

---

## 🚀 Cara Menjalankan

Lakukan eksekusi langsung melalui terminal atau command prompt pada direktori tempat berkas `game_launcher.py` disimpan:

```bash
python3 game_launcher.py

```
*Jika python bawaan error, pakai venv saja*
### Mengaktifkan Venv
```bash
source .venv/bin/activate
```
### Keluar dari venv
```bash
deactivate
```
### Jalankan game launchernya
```bash
python3 game_launcher.py
```

---

## 🔧 Konfigurasi Warna & Gaya (Style Guide)

Jika Anda ingin memodifikasi palet warna bawaan, berikut adalah referensi kode warna yang digunakan:

| Komponen Visual | Kode Warna (Hex) | Deskripsi |
| --- | --- | --- |
| **Background Utama** | `#111214` | Warna latar belakang gelap pekat |
| **Panel / Input Box** | `#1b1c1f` | Warna latar belakang tabel dan kotak isian |
| **Aksen Utama** | `#dfff00` | Kuning Stabilo / Electric Lime untuk elemen penting |
| **Teks Utama** | `#f5f6f7` | Putih bersih untuk keterbacaan tinggi |
| **Teks Sekunder** | `#7e8494` | Abu-abu redup untuk status sistem / label |
| **Hover Run Button** | `#bacc00` | Transisi kuning redup saat pointer di atas tombol |
| **Pressed Run Button** | `#94a300` | Kuning tua taktis saat tombol diklik |

---

## 📝 Lisensi

Proyek ini dibuat untuk pemakaian personal dan pengembangan hobi. Silakan dimodifikasi dan dikembangkan lebih lanjut sesuai kebutuhan koleksi game Anda!

*Jika ada informasi yang kurang, mohon maaf, dan jika ada bug terkait launcher, beritahu saya ya, atau kalau mau secara suka rela mengembangkannya, silahkan*
