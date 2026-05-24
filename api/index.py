from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import os

app = FastAPI()

# Ambil kredensial dari Environment Variables Vercel
SUPABASE_URL = os.environ.get("https://jvfwzykpxnplmjyddjds.supabase.co")
SUPABASE_KEY = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp2Znd6eWtweG5wbG1qeWRkamRzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk2MzAyMjcsImV4cCI6MjA5NTIwNjIyN30.dZURW1c9YGFOXWBigwTJEmCe0wPk6a0lseImpY4Wo0Q")

# Inisialisasi client Supabase
try:
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    else:
        supabase = None
except Exception as e:
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
        raise HTTPException(status_code=500, detail="Koneksi ke Supabase gagal. Periksa Environment Variables Anda.")
    try:
        response = supabase.table("items").select("*").order("id", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil data: {str(e)}")

@app.post("/api/items")
def add_item(item: ItemCreate):
    try:
        response = supabase.table("items").insert(item.dict()).execute()
        return {
            "data": response.data
        }
    except Exception as e:
        return {
            "error": str(e)
        }

@app.put("/api/items/{item_id}")
def update_quantity(item_id: int, item: ItemUpdate):
    if not supabase:
        raise HTTPException(status_code=500, detail="Koneksi ke Supabase gagal.")
    try:
        response = supabase.table("items").update({"quantity": item.quantity}).eq("id", item_id).execute()
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(status_code=404, detail="Item tidak ditemukan untuk diupdate.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
