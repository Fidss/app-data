from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import os

app = FastAPI()

# Mengambil kredensial dari Environment Variables Vercel
SUPABASE_URL = os.environ.get("https://jvfwzykpxnplmjyddjds.supabase.co")
SUPABASE_KEY = os.environ.get("sb_publishable_AvmigZp4g0aaZgpQ1cH3YA_NNBHa_XF")

# Inisialisasi client Supabase
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

class ItemCreate(BaseModel):
    name: str
    image_url: str
    quantity: int

class ItemUpdate(BaseModel):
    quantity: int

@app.get("/api/items")
def get_items():
    if not supabase:
        raise HTTPException(status_code=500, detail="Konfigurasi Supabase tidak ditemukan")
    response = supabase.table("items").select("*").order("id", desc=True).execute()
    return response.data

@app.post("/api/items")
def add_item(item: ItemCreate):
    response = supabase.table("items").insert(item.dict()).execute()
    return response.data[0]

@app.put("/api/items/{item_id}")
def update_quantity(item_id: int, item: ItemUpdate):
    response = supabase.table("items").update({"quantity": item.quantity}).eq("id", item_id).execute()
    return response.data[0]
