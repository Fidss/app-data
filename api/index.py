from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Path untuk file JSON lokal (akan otomatis terbuat di dalam folder api)
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# Fungsi untuk inisialisasi file JSON jika belum ada
def init_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

# Fungsi bantuan untuk baca dan tulis JSON
def read_data():
    init_db()
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Model Data
class ItemCreate(BaseModel):
    name: str
    image_url: str
    quantity: int

class ItemUpdate(BaseModel):
    quantity: int

@app.get("/api/items")
def get_items():
    return read_data()

@app.post("/api/items")
def add_item(item: ItemCreate):
    data = read_data()
    
    # Bikin ID otomatis (Mencari ID terbesar yang ada + 1)
    new_id = 1 if not data else max(i["id"] for i in data) + 1
    
    new_item = {
        "id": new_id,
        "name": item.name,
        "image_url": item.image_url,
        "quantity": item.quantity
    }
    
    # Masukkan data baru di urutan paling atas (index 0)
    data.insert(0, new_item)
    write_data(data)
    return new_item

@app.put("/api/items/{item_id}")
def update_quantity(item_id: int, item: ItemUpdate):
    data = read_data()
    
    for i in range(len(data)):
        if data[i]["id"] == item_id:
            data[i]["quantity"] = item.quantity
            write_data(data)
            return data[i]
            
    raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    
