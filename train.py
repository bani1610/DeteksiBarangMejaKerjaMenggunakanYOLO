from ultralytics import YOLO
import os
import json
from datetime import datetime

# ============================================================
#   TRAINING SCRIPT - SMART WORKSPACE MONITOR
#   Deteksi Barang di Meja Kerja menggunakan YOLOv8
#   Dataset: COCO128 (subset COCO, tersedia otomatis di YOLO)
# ============================================================

print("=" * 60)
print("   TRAINING: SMART WORKSPACE MONITOR")
print("   Dataset  : COCO128 (128 gambar dari dataset COCO)")
print("   Model    : YOLOv8s (small)")
print("=" * 60)

# -------------------------------------------------------
# KELAS BARANG MEJA KERJA yang relevan dari COCO dataset
# (COCO punya 80 kelas, kita fokus ke barang meja kerja)
# -------------------------------------------------------
DESK_CLASSES = [
    'laptop',       # laptop/notebook
    'mouse',        # mouse komputer
    'keyboard',     # keyboard
    'cell phone',   # smartphone
    'book',         # buku
    'cup',          # gelas/mug
    'bottle',       # botol minum
    'scissors',     # gunting
    'remote',       # remote control
    'tv',           # monitor/TV
    'potted plant', # tanaman hias
    'vase',         # vas/tempat pensil
    'chair',        # kursi
    'backpack',     # tas ransel
]

print(f"\n[INFO] Kelas barang meja kerja yang dideteksi ({len(DESK_CLASSES)} kelas):")
for i, cls in enumerate(DESK_CLASSES, 1):
    print(f"  {i:2d}. {cls}")

# -------------------------------------------------------
# STEP 1: Load model YOLOv8s (pretrained COCO)
# Fine-tune dari pretrained supaya training lebih cepat
# -------------------------------------------------------
print("\n[STEP 1] Memuat model YOLOv8s pretrained...")
model = YOLO('yolov8s.pt')
print("[OK] Model berhasil dimuat.")

# -------------------------------------------------------
# STEP 2: TRAINING
# Dataset COCO128 otomatis diunduh oleh ultralytics
# coco128.yaml = 128 gambar dari COCO (cocok untuk demo/tugas)
# -------------------------------------------------------
print("\n[STEP 2] Memulai training...")
print("         Dataset: COCO128 (akan otomatis didownload jika belum ada)")
print("         Estimasi waktu: 5-15 menit tergantung spesifikasi komputer\n")

training_results = model.train(
    data='coco128.yaml',           # Dataset COCO128 (bawaan ultralytics)
    epochs=30,                      # Jumlah epoch (30 cukup untuk demo)
    imgsz=640,                      # Ukuran gambar input
    batch=8,                        # Batch size (turunkan jika RAM kurang)
    name='workspace_monitor',       # Nama folder hasil training
    project='runs/train',           # Folder penyimpanan
    patience=10,                    # Early stopping jika tidak ada peningkatan
    save=True,                      # Simpan model terbaik
    plots=True,                     # Simpan grafik training (loss, mAP, dll)
    verbose=True,
    device=0 if os.path.exists('/dev/nvidia0') else 'cpu',  # GPU jika ada
)

print("\n[OK] Training selesai!")
best_model_path = 'runs/train/workspace_monitor/weights/best.pt'
print(f"[INFO] Model terbaik disimpan di: {best_model_path}")

# -------------------------------------------------------
# STEP 3: EVALUASI MODEL (Precision, Recall, mAP)
# Ini yang dibutuhkan untuk laporan!
# -------------------------------------------------------
print("\n[STEP 3] Mengevaluasi model (Precision, Recall, mAP)...")

eval_model = YOLO(best_model_path)
metrics = eval_model.val(
    data='coco128.yaml',
    split='val',        # Evaluasi pada data validasi
    verbose=False,
)

# Ambil metrik evaluasi
precision  = metrics.box.mp        # Mean Precision
recall     = metrics.box.mr        # Mean Recall
map50      = metrics.box.map50     # mAP @ IoU 0.50
map50_95   = metrics.box.map       # mAP @ IoU 0.50:0.95

# -------------------------------------------------------
# STEP 4: TAMPILKAN DAN SIMPAN HASIL EVALUASI
# -------------------------------------------------------
print("\n" + "=" * 60)
print("   HASIL EVALUASI MODEL")
print("=" * 60)
print(f"  Precision       : {precision:.4f}  ({precision*100:.2f}%)")
print(f"  Recall          : {recall:.4f}  ({recall*100:.2f}%)")
print(f"  mAP@0.50        : {map50:.4f}  ({map50*100:.2f}%)")
print(f"  mAP@0.50:0.95   : {map50_95:.4f}  ({map50_95*100:.2f}%)")
print("=" * 60)

# Penjelasan metrik untuk laporan
print("\n[PENJELASAN METRIK]")
print(f"  - Precision {precision*100:.1f}%  → dari semua deteksi, {precision*100:.1f}% benar (tidak salah deteksi)")
print(f"  - Recall    {recall*100:.1f}%  → dari semua objek nyata, {recall*100:.1f}% berhasil terdeteksi")
print(f"  - mAP50     {map50*100:.1f}%  → akurasi rata-rata dengan threshold IoU 50%")
print(f"  - mAP50-95  {map50_95*100:.1f}%  → akurasi rata-rata dengan berbagai threshold (lebih ketat)")

# Simpan hasil evaluasi ke file JSON untuk laporan
hasil = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "model": best_model_path,
    "dataset": "COCO128",
    "epochs": 30,
    "metrics": {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "mAP50": round(map50, 4),
        "mAP50_95": round(map50_95, 4),
    }
}

with open("hasil_evaluasi.json", "w") as f:
    json.dump(hasil, f, indent=4)

print(f"\n[OK] Hasil evaluasi disimpan ke: hasil_evaluasi.json")
print(f"[OK] Grafik training tersimpan di: runs/train/workspace_monitor/")

# -------------------------------------------------------
# STEP 5: PANDUAN SELANJUTNYA
# -------------------------------------------------------
print("\n" + "=" * 60)
print("   LANGKAH SELANJUTNYA")
print("=" * 60)
print("  1. Jalankan main.py untuk deteksi real-time dengan webcam")
print("     → main.py sudah otomatis pakai model terbaik (best.pt)")
print("  2. Lihat grafik training di folder:")
print("     → runs/train/workspace_monitor/")
print("  3. Gunakan hasil evaluasi di atas untuk laporan bab 5")
print("=" * 60)
