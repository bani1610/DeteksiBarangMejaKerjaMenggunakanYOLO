# Smart Workspace Monitor

Smart Workspace Monitor adalah proyek computer vision sederhana berbasis YOLOv8 untuk memantau kondisi meja kerja melalui webcam secara real-time.

Aplikasi akan:
- Mendeteksi objek pada meja kerja (misalnya laptop, mouse, keyboard, cell phone, book, cup, bottle, chair, dan lainnya)
- Menampilkan status meja (rapi, berantakan, kosong, atau barang tertinggal)
- Menampilkan waktu saat ini
- Menyimpan screenshot saat tombol `s` ditekan

## Fitur Utama

- Deteksi objek real-time menggunakan model YOLOv8
- Filter khusus objek yang relevan untuk area kerja
- Penilaian kondisi meja berdasarkan jumlah barang
- Peringatan setelah jam kerja jika masih ada barang di meja
- Tampilan visual hasil deteksi dengan anotasi bounding box

## Teknologi

- Python 3.10+
- Ultralytics YOLOv8
- OpenCV (cv2)

## Struktur Proyek

- `main.py` : Aplikasi utama Smart Workspace Monitor
- `yolov8s.pt` : Model yang digunakan saat ini
- `yolov8n.pt`, `yolov8m.pt` : Alternatif model

## Prasyarat

Pastikan perangkat memiliki:
- Python 3.10 atau lebih baru
- Webcam aktif
- Koneksi internet (jika ingin mengunduh dependency/model pertama kali)

## Instalasi

### 1. Masuk ke folder proyek

Windows (PowerShell):

cd [nama foldenya]

### 2. (Opsional tapi disarankan) Buat virtual environment

python -m venv .venv
.venv\Scripts\Activate.ps1

### 3. Install dependency

pip install ultralytics opencv-python

## Cara Menjalankan

Jalankan aplikasi:

python main.py

Jika memakai path interpreter tertentu, bisa juga:

C:/Users/shola/AppData/Local/Programs/Python/Python310/python.exe main.py

## Kontrol Keyboard

- Tekan `q` untuk keluar dari aplikasi
- Tekan `s` untuk menyimpan screenshot

## Logika Status Meja

Aplikasi menentukan status berdasarkan jumlah objek terdeteksi dan waktu saat ini:

- BERANTAKAN: jumlah barang lebih dari batas rapi
- BARANG TERTINGGAL!: masih ada barang setelah jam kerja
- Rapi: ada barang tapi masih dalam batas rapi
- Meja Kosong: tidak ada barang terdeteksi

## Konfigurasi Penting

Di dalam `main.py` terdapat parameter yang bisa diubah:

- `JAM_KERJA_AKHIR` (default 17)
- `MAX_BARANG_RAPI` (default 4)
- `DESK_CLASSES` (daftar objek yang dianggap barang meja)

## Troubleshooting

### 1) Error: ModuleNotFoundError: No module named ultralytics

Penyebab: package belum terpasang di interpreter yang dipakai.

Solusi:
- Install ke interpreter yang benar:

C:/Users/shola/AppData/Local/Programs/Python/Python310/python.exe -m pip install ultralytics opencv-python

- Pastikan VS Code memilih interpreter yang sama dengan yang dipakai saat menjalankan file.

### 2) Webcam tidak terbuka

- Pastikan webcam tidak dipakai aplikasi lain
- Coba ganti index kamera di `cv2.VideoCapture(0)` menjadi `cv2.VideoCapture(1)`

### 3) Deteksi kurang akurat

- Gunakan pencahayaan lebih terang
- Arahkan kamera agar objek terlihat jelas
- Coba model lain (`yolov8n.pt` lebih cepat, `yolov8m.pt` bisa lebih detail namun lebih berat)

## Catatan

Model yang dipakai saat ini adalah `yolov8s.pt` (lihat di `main.py`).
Jika ingin mengganti model, ubah baris:

model = YOLO('yolov8s.pt')

Contoh alternatif:
- model = YOLO('yolov8n.pt')
- model = YOLO('yolov8m.pt')
