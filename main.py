from ultralytics import YOLO
import cv2
from datetime import datetime

# ============================================
#   SMART WORKSPACE MONITOR
#   Deteksi Barang di Meja Kerja dengan YOLO
# ============================================


print("=" * 50)
print("   SMART WORKSPACE MONITOR")
print("=" * 50)
print("Memuat model YOLOv8... (pertama kali akan download ~6MB)")

# 1. Load model YOLOv8 Nano (ringan & cepat)
model = YOLO('yolov8s.pt')

# Tampilkan semua kelas yang bisa dideteksi
print("Kelas COCO yang tersedia:")
for i, name in model.names.items():
    print(f"{i}: {name}")
# 2. Daftar barang meja kerja yang ingin dideteksi
DESK_CLASSES = [
    'laptop',           # Laptop
    'mouse',            # Mouse
    'keyboard',         # Keyboard
    'cell phone',       # HP
    'book',             # Buku
    'cup',              # Cangkir
    'bottle',           # Botol
    'chair',            # Kursi
    'backpack',         # Tas
    'scissors',         # Gunting
    'remote',           # Remote
    'tv',               # Monitor (kadang terdeteksi sebagai TV)
    'potted plant',     # Tanaman hias
    'vase',             # Vas bunga
    'toothbrush',       # Sikat gigi (kadang mirip pulpen)
    'suitcase',         # Koper/tas kerja
    'handbag',          # Tas tangan
    'tie',              # Dasi
    'umbrella',         # Payung
    'frisbee',          # (kadang mirip piring)
    'skateboard',       # (kadang mirip tablet)
]

# 3. Konfigurasi
JAM_KERJA_AKHIR = 17  # Jam 5 sore
MAX_BARANG_RAPI = 4   # Maksimal barang agar dianggap "rapi"

# 4. Buka webcam
print("Membuka webcam...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Tidak bisa membuka webcam!")
    print("Pastikan webcam tidak dipakai aplikasi lain.")
    exit()

print("Sistem aktif! Arahkan kamera ke meja kerja Anda.")
print("Tekan 'q' untuk keluar, tekan 's' untuk screenshot.")
print("-" * 50)

while True:
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Gagal membaca frame dari webcam.")
        break

    # 5. Deteksi objek dengan YOLO
    results = model(frame, verbose=False)

    # 6. Filter hanya barang meja kerja
    detected_items = []
    for box in results[0].boxes:
        class_name = model.names[int(box.cls)]
        confidence = float(box.conf)
        if class_name in DESK_CLASSES and confidence > 0.15:
            detected_items.append(class_name)

    # Hilangkan duplikat untuk hitungan jenis barang
    unique_items = list(set(detected_items))
    jumlah_barang = len(detected_items)
    jumlah_jenis = len(unique_items)

    # 7. Logika Smart Workspace
    now = datetime.now()
    jam_sekarang = now.hour
    menit_sekarang = now.minute
    waktu_str = f"{jam_sekarang:02d}:{menit_sekarang:02d}"

    status_text = ""
    status_color = (0, 255, 0)  # Hijau (default: OK)

    # Logika A: Meja berantakan
    if jumlah_barang > MAX_BARANG_RAPI:
        status_text = f"BERANTAKAN ({jumlah_barang} barang)"
        status_color = (0, 0, 255)  # Merah

    # Logika B: Barang tertinggal setelah jam kerja
    elif jumlah_barang > 0 and jam_sekarang >= JAM_KERJA_AKHIR:
        status_text = "BARANG TERTINGGAL!"
        status_color = (0, 165, 255)  # Oranye

    # Logika C: Meja rapi
    elif jumlah_barang > 0:
        status_text = f"Rapi ({jumlah_barang} barang)"
        status_color = (0, 255, 0)  # Hijau

    # Logika D: Meja kosong
    else:
        status_text = "Meja Kosong"
        status_color = (255, 255, 0)  # Cyan

    # 8. Gambar tampilan di layar
    annotated_frame = results[0].plot()

    # Background kotak status
    cv2.rectangle(annotated_frame, (0, 0), (640, 100), (0, 0, 0), -1)

    # Tampilkan waktu
    cv2.putText(annotated_frame, f"Waktu: {waktu_str}", 
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Tampilkan status
    cv2.putText(annotated_frame, f"Status: {status_text}", 
                (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)

    # Tampilkan daftar barang
    barang_str = ", ".join(unique_items) if unique_items else "Tidak ada"
    cv2.putText(annotated_frame, f"Barang: {barang_str}", 
                (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    # 9. Tampilkan di layar
    cv2.imshow('Smart Workspace Monitor', annotated_frame)

    # 10. Handle keyboard input
    key = cv2.waitKey(1) & 0xFF
    
    # Tekan 'q' untuk keluar
    if key == ord('q'):
        print("\nProgram dihentikan oleh pengguna.")
        break
    
    # Tekan 's' untuk screenshot
    elif key == ord('s'):
        filename = f"screenshot_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(filename, annotated_frame)
        print(f"Screenshot disimpan: {filename}")

# 11. Bersihkan
cap.release()
cv2.destroyAllWindows()
print("Smart Workspace Monitor dimatikan.")