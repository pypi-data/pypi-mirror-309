from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
from ultralytics import YOLO
import os
import uuid
import uvicorn

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Path absolut untuk direktori statis, template, dan uploads
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Konfigurasi static, template, dan uploads
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Load model YOLO
MODEL_PATH = os.path.join(BASE_DIR, "best_2.pt")
model = YOLO(MODEL_PATH)

# Pastikan folder uploads ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Halaman utama untuk upload gambar."""
    return templates.TemplateResponse("index.html", {"request": {}})

@app.post("/upload/")
async def upload_image(
    file: UploadFile = File(...),
    confidence: float = Form(0.5),
    iou: float = Form(0.5)
):
    """Endpoint untuk upload gambar dan melakukan deteksi objek."""
    # Simpan gambar ke folder sementara
    file_id = str(uuid.uuid4())
    image_path = os.path.join(UPLOAD_FOLDER, f"{file_id}_{file.filename}")
    with open(image_path, "wb") as f:
        f.write(await file.read())

    # Lakukan deteksi dengan YOLO
    image = Image.open(image_path)
    results = model.predict(source=image, save=False, conf=confidence, iou=iou)

    # Simpan hasil deteksi
    result_image = results[0].plot()
    result_image_pillow = Image.fromarray(result_image)
    result_path = os.path.join(UPLOAD_FOLDER, f"result_{file_id}.jpg")
    result_image_pillow.save(result_path)

    # Ekstrak informasi deteksi dengan penomoran
    detections = results[0].boxes.data.cpu().numpy()
    detection_data = [
        {
            "id": idx + 1,  # Tambahkan nomor urut
            "class": results[0].names[int(detection[5])],
            "confidence": float(detection[4]),
            "coordinates": [float(detection[0]), float(detection[1]), float(detection[2]), float(detection[3])],
        }
        for idx, detection in enumerate(detections)
    ]

    return {
        "image_url": f"/uploads/result_{file_id}.jpg",  # URL file hasil deteksi
        "detections": detection_data,
    }

def main():
    """Entry point untuk menjalankan aplikasi."""
    uvicorn.run("my_label_tool.app:app", host="127.0.0.1", port=8000, reload=True)
