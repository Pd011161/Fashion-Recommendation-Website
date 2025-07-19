from fastapi import FastAPI, UploadFile, File
from app.database_query import db_query
from app.retriver import search_vector_db
from app.generate_description import generate_description_base64
from app.classify_fashion_search import classify_fashion_type
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import uuid
import os, time
from fastapi.staticfiles import StaticFiles
from PIL import Image
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



BASE_URL = "http://localhost:8000"

STATIC_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "datalake")
)


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือ ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextQuery(BaseModel):
    query: str
def get_shirt_image_url(img_id):
    return f"{BASE_URL}/static/shirt/{img_id}.jpg"

def get_pants_image_url(img_id):
    return f"{BASE_URL}/static/pants/{img_id}.jpg"

@app.get("/products/shirt")
def get_shirts():
    sql = "SELECT * FROM shirt"
    items = db_query(sql, ()) or []
    results = []
    for item in items:
        results.append({
            "id": item['id'],
            "name": item['Name'],
            "url": get_shirt_image_url(item['id']),
            "th_desc": item['TH_Description'],
            "en_desc": item['EN_Description'],
        })
    return {"results": results}



@app.get("/products/pants")
def get_shirts():
    sql = "SELECT * FROM pants"
    items = db_query(sql, ()) or []
    print("DEBUG items:", items)
    results = []
    for item in items:
        results.append({
            "id": item['id'],
            "name": item['Name'],
            "url": get_pants_image_url(item['id']),
            "th_desc": item['TH_Description'],
            "en_desc": item['EN_Description'],
        })
    return {"results": results}



@app.post("/recommend-by-text")
def recommend_by_text(payload: TextQuery):
    """
    รับข้อความ > LLM ช่วย classify (shirt/pants) > เลือก collection/table
    > search vector db > query db > return results
    """
    query = payload.query
    que_type = classify_fashion_type(query)  # 'shirt' หรือ 'pants'
    if que_type == "เสื้อ":
        col_name = 'shirt_collection'
        table_name = "shirt"
        top_ids = search_vector_db(col_name, query)
        print("top_ids:", top_ids)
        results = []
        for idx in top_ids:
            item_list = db_query(f"SELECT * FROM {table_name} WHERE id=?", (idx,))
            if item_list:
                item = item_list[0]   # <-- ดึง dict ตัวแรก
                results.append({
                    "id": item['id'],
                    "name": item['Name'],
                    "url": get_shirt_image_url(item['id']),
                    "th_desc": item['TH_Description'],
                    "en_desc": item['EN_Description'],
                })
        print('results:', results)
        return {"results": results}
    
    elif que_type == "กางเกง":
        col_name = 'pants_collection'
        table_name = "pants"
        top_ids = search_vector_db(col_name, query)
        print("top_ids:", top_ids)
        results = []
        for idx in top_ids:
            item_list = db_query(f"SELECT * FROM {table_name} WHERE id=?", (idx,))
            if item_list:
                item = item_list[0]   # <-- ดึง dict ตัวแรก
                results.append({
                    "id": item['id'],
                    "name": item['Name'],
                    "url": get_pants_image_url(item['id']),
                    "th_desc": item['TH_Description'],
                    "en_desc": item['EN_Description'],
                })
        print('results:', results)
        return {"results": results}
    
    else:
        print('anomaly-que_type:', que_type)
        return {"results": [], "error": "ไม่สามารถระบุประเภทสินค้าได้"}

    
    
# def wait_until_image_ready(image_url, timeout=8):
#     for _ in range(timeout):
#         try:
#             print("Checking:", image_url)
#             r = requests.get(image_url)
#             if r.status_code == 200:
#                 return True
#         except Exception as e:
#             print("wait image err:", e)
#         time.sleep(1)
#     return False


UPLOAD_DIR = os.path.join(STATIC_DIR, "upload")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/recommend-by-image")
async def recommend_by_image(file: UploadFile = File(...)):
    print("START recommend_by_image")
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # --- Resize รูปก่อน
    try:
        img = Image.open(file_path)
        img = img.convert("RGB")
        print("RESIZED")
        img.thumbnail((600, 600))
        print("SAVED file:", file_path)
        img.save(file_path, "JPEG")
    except Exception as e:
        print("Error resizing image:", e)

    image_url = f"{BASE_URL}/static/upload/{filename}"

    # if not wait_until_image_ready(image_url):
    #     return {"results": [], "error": "static file ยังโหลดไม่ได้"}

    # print("STATIC OK")
    # ---- เรียก LLM
    print("CALL LLM:", image_url)
    caption = generate_description_base64(file_path)
    print('caption:', caption)

    que_type = classify_fashion_type(caption)  # 'shirt' หรือ 'pants'
    if que_type == "เสื้อ":
        col_name = 'shirt_collection'
        table_name = "shirt"
        top_ids = search_vector_db(col_name, caption)
        print("top_ids:", top_ids)
        results = []
        for idx in top_ids:
            item_list = db_query(f"SELECT * FROM {table_name} WHERE id=?", (idx,))
            if item_list:
                item = item_list[0]   # <-- ดึง dict ตัวแรก
                results.append({
                    "id": item['id'],
                    "name": item['Name'],
                    "url": get_shirt_image_url(item['id']) ,  # <<<<<< หรือ get_shirt_image_url(item['id']) ถ้ามีฟังก์ชันนี้
                    "th_desc": item['TH_Description'],
                    "en_desc": item['EN_Description'],
                })
        print('results:', results)
        return {"results": results}
    
    elif que_type == "กางเกง":
        col_name = 'pants_collection'
        table_name = "pants"
        top_ids = search_vector_db(col_name, caption)
        print("top_ids:", top_ids)
        results = []
        for idx in top_ids:
            item_list = db_query(f"SELECT * FROM {table_name} WHERE id=?", (idx,))
            if item_list:
                item = item_list[0]   # <-- ดึง dict ตัวแรก
                results.append({
                    "id": item['id'],
                    "name": item['Name'],
                    "url": get_pants_image_url(item['id']),  # <<<<<< หรือ get_pants_image_url(item['id']) ถ้ามีฟังก์ชันนี้
                    "th_desc": item['TH_Description'],
                    "en_desc": item['EN_Description'],
                })
        print('results:', results)
        return {"results": results}
    
    else:
        print('anomaly-que_type:', que_type)
        return {"results": [], "error": "ไม่สามารถระบุประเภทสินค้าได้"}
