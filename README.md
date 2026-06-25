# 🖥️ Smart Workspace Monitor

**Smart Workspace Monitor** adalah proyek *computer vision* berbasis YOLOv8 untuk memantau kondisi meja kerja secara *real-time* melalui webcam. Aplikasi ini dirancang untuk mendeteksi barang-barang spesifik di area kerja dan memberikan peringatan visual mengenai status kerapian meja Anda.

---

## ✨ Fitur Utama

- **Real-Time Object Detection**: Menggunakan model YOLOv8 untuk deteksi cepat dan akurat.
- **Strict Desk Filtering**: Hanya menggambar *bounding box* untuk objek yang relevan dengan meja kerja (mengabaikan orang atau objek latar belakang).
- **Dynamic Bounding Box Colors**: Warna kotak deteksi di-generate secara acak namun konsisten untuk setiap jenis barang agar mudah dibedakan.
- **Natural View (Mirroring)**: Tampilan kamera otomatis di-flip secara horizontal agar pergerakan terasa natural.
- **Resizable Window**: Jendela aplikasi dapat di-resize dan di-maximize menyesuaikan resolusi layar.
- **Smart Status Logic**: Penilaian kondisi meja (Rapi, Berantakan, Kosong) berdasarkan jumlah barang.
- **Overtime Alert**: Peringatan khusus jika masih ada barang yang tertinggal di meja setelah jam kerja selesai.
- **Quick Capture**: Fitur *screenshot* instan dengan satu tombol.

---

## 🛠️ Teknologi & Dependensi

- **Python** 3.10+
- **Ultralytics YOLOv8** (Model AI)
- **OpenCV (`cv2`)** (Pemrosesan gambar & UI)

---

## ⚙️ Prasyarat & Instalasi

Pastikan PC/Laptop Anda memiliki webcam yang aktif dan koneksi internet (untuk unduhan model pertama kali).

### 1. Kloning / Masuk ke Direktori Proyek
Buka terminal atau PowerShell, lalu arahkan ke folder proyek:
```bash
cd [nama foldernya]
```

### 2. Buat Virtual Environment (Disarankan)
Agar dependensi tidak bentrok dengan proyek lain:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependensi
```bash
pip install ultralytics opencv-python
```

---

## 🚀 Cara Menjalankan

Jalankan perintah berikut di terminal:
```bash
python main.py
```

Jika menggunakan *absolute path* interpreter tertentu:
```bash
C:/Users/name/AppData/Local/Programs/Python/Python310/python.exe main.py
```

---

## 🎮 Kontrol Keyboard

| Tombol | Fungsi |
| :---: | :--- |
| `q` | Keluar dan mematikan aplikasi |
| `s` | Menyimpan *screenshot* kondisi meja saat ini ke dalam folder proyek |

---

## 🧠 Logika Status Meja

Aplikasi menentukan status berdasarkan jumlah objek yang terdeteksi dan batas jam kerja:

| Status | Indikator Warna | Kondisi |
| :--- | :---: | :--- |
| **Meja Kosong** | Kuning / Cyan | Tidak ada barang yang terdeteksi sama sekali. |
| **Rapi** | Hijau | Jumlah barang > 0, tapi masih di bawah batas `MAX_BARANG_RAPI`. |
| **BERANTAKAN** | Merah | Jumlah barang melebihi batas `MAX_BARANG_RAPI`. |
| **BARANG TERTINGGAL!**| Oranye | Ada barang di meja **dan** waktu sudah melewati `JAM_KERJA_AKHIR`. |

---

## 🔧 Konfigurasi

Anda dapat menyesuaikan sensitivitas dan aturan aplikasi dengan mengubah variabel berikut di dalam `main.py`:

- `JAM_KERJA_AKHIR` : Batas jam kerja (Default: `17` / Jam 5 sore).
- `MAX_BARANG_RAPI` : Batas maksimal barang di meja agar tetap dianggap rapi (Default: `4`).
- `DESK_CLASSES` : Daftar kelas barang yang ingin diizinkan untuk dideteksi.
- `model = YOLO('yolov8s.pt')` : Mengubah ukuran model. (Gunakan `yolov8n.pt` untuk performa lebih ringan, atau `yolov8m.pt` untuk akurasi lebih tinggi).

---

## 🐛 Troubleshooting

### 1. `ModuleNotFoundError: No module named ultralytics`
**Penyebab:** *Package* belum terpasang di Python interpreter yang sedang aktif.
**Solusi:** Pastikan Anda menginstal di interpreter yang sama dengan yang dijalankan.
```bash
C:/Users/name/AppData/Local/Programs/Python/Python310/python.exe -m pip install ultralytics opencv-python
```

### 2. Webcam Tidak Terbuka / Black Screen
- Pastikan webcam tidak sedang digunakan oleh aplikasi lain (Zoom, Google Meet, dll).
- Jika memiliki lebih dari satu kamera, ubah indeks di baris `cap = cv2.VideoCapture(0)` menjadi `cv2.VideoCapture(1)`.

### 3. Deteksi Kurang Akurat / Barang Tidak Dikenali
- Pastikan pencahayaan ruangan cukup terang.
- Atur posisi kamera agar menyorot meja dari sudut pandang yang jelas.
- Coba ganti model ke `yolov8m.pt` jika PC memiliki spesifikasi yang memadai untuk deteksi yang lebih tajam.