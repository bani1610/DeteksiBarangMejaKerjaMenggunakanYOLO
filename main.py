from ultralytics import YOLO
import cv2
from datetime import datetime
import random
import os

# ============================================
#   SMART WORKSPACE MONITOR
#   Deteksi Barang di Meja Kerja dengan YOLO
# ============================================

print("=" * 50)
print("   SMART WORKSPACE MONITOR")
print("=" * 50)

# 1. Load model - pakai hasil training jika sudah ada, jika belum pakai pretrained
BEST_MODEL_PATH = 'runs/train/workspace_monitor/weights/best.pt'
if os.path.exists(BEST_MODEL_PATH):
    print(f"[OK] Menggunakan model hasil training: {BEST_MODEL_PATH}")
    model = YOLO(BEST_MODEL_PATH)
else:
    print("[INFO] Model training belum ada. Jalankan train.py terlebih dahulu.")
    print("[INFO] Menggunakan model pretrained YOLOv8s sementara...")
    model = YOLO('yolov8s.pt')

# 2. Daftar barang meja kerja yang ingin dideteksi
# (hanya kelas yang relevan dengan meja kerja dari dataset COCO)
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

# 3. Konfigurasi
JAM_KERJA_AKHIR = 17  # Jam 5 sore
MAX_BARANG_RAPI = 4   # Maksimal barang agar dianggap "rapi"

# Fungsi untuk bikin warna acak tapi konsisten per barang
def get_color(class_id):
    random.seed(class_id)
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# 4. Buka webcam
print("Membuka webcam...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Tidak bisa membuka webcam!")
    exit()

print("Sistem aktif! Arahkan kamera ke meja kerja Anda.")
print("Tekan 'q' untuk keluar, tekan 's' untuk screenshot.")
print("-" * 50)

# BIKIN WINDOW BISA DI-RESIZE & MAXIMIZE
cv2.namedWindow('Smart Workspace Monitor', cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Gagal membaca frame dari webcam.")
        break

    # MIRROR KAMERA (Flip horizontal)
    frame = cv2.flip(frame, 1)

    # 5. Deteksi objek dengan YOLO
    results = model(frame, verbose=False)
    
    # Gunakan frame asli, jangan pakai results[0].plot()
    annotated_frame = frame.copy()

    # 6. Filter & Gambar Bounding Box khusus barang meja
    detected_items = []
    for box in results[0].boxes:
        class_id = int(box.cls)
        class_name = model.names[class_id]
        confidence = float(box.conf)
        
        # Kalau barang masuk daftar DESK_CLASSES, baru kita proses dan gambar
        if class_name in DESK_CLASSES and confidence >= 0.30:  # threshold 30% untuk kurangi false positive
            detected_items.append(class_name)
            
            # Ambil koordinat untuk gambar kotak
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            
            # Ambil warna khusus untuk class ini
            color = get_color(class_id)
            
            # Gambar kotak deteksi dengan warna khusus
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            
            # Gambar label nama barang di atas kotaknya
            label = f"{class_name} {confidence:.2f}"
            cv2.putText(annotated_frame, label, (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Hilangkan duplikat untuk hitungan jenis barang di UI
    unique_items = list(set(detected_items))
    jumlah_barang = len(detected_items)

    # 7. Logika Smart Workspace
    now = datetime.now()
    jam_sekarang = now.hour
    waktu_str = f"{jam_sekarang:02d}:{now.minute:02d}"

    status_text = ""
    status_color = (0, 255, 0)

    if jumlah_barang > MAX_BARANG_RAPI:
        status_text = f"BERANTAKAN ({jumlah_barang} barang)"
        status_color = (0, 0, 255)
    elif jumlah_barang > 0 and jam_sekarang >= JAM_KERJA_AKHIR:
        status_text = "BARANG TERTINGGAL!"
        status_color = (0, 165, 255)
    elif jumlah_barang > 0:
        status_text = f"Rapi ({jumlah_barang} barang)"
        status_color = (0, 255, 0)
    else:
        status_text = "Meja Kosong"
        status_color = (255, 255, 0)

    # 8. Gambar UI Status di layar (Background Hitam Atas)
    cv2.rectangle(annotated_frame, (0, 0), (640, 100), (0, 0, 0), -1)
    cv2.putText(annotated_frame, f"Waktu: {waktu_str}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(annotated_frame, f"Status: {status_text}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
    
    barang_str = ", ".join(unique_items) if unique_items else "Tidak ada"
    cv2.putText(annotated_frame, f"Barang: {barang_str}", (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    # 9. Tampilkan di layar
    cv2.imshow('Smart Workspace Monitor', annotated_frame)

    # 10. Handle keyboard input
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        filename = f"screenshot_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(filename, annotated_frame)

# 11. Bersihkan
cap.release()
cv2.destroyAllWindows()
