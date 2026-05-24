from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import os
from typing import Optional

app = FastAPI()

# CORS untuk frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.environ.get("SUPABASE_URL") or "https://jvfwzykpxnplmjyddjds.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp2Znd6eWtweG5wbG1qeWRkamRzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk2MzAyMjcsImV4cCI6MjA5NTIwNjIyN30.dZURW1c9YGFOXWBigwTJEmCe0wPk6a0lseImpY4Wo0Q"

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
    name: Optional[str] = None
    image_url: Optional[str] = None
    quantity: Optional[int] = None

@app.get("/api/items")
def get_items():
    if not supabase:
        raise HTTPException(status_code=500, detail="Koneksi ke Supabase gagal.")
    try:
        response = supabase.table("items").select("*").order("id", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase Error: {str(e)}")

@app.post("/api/items")
def add_item(item: ItemCreate):
    if not supabase:
        raise HTTPException(status_code=500, detail="Koneksi ke Supabase gagal.")
    try:
        response = supabase.table("items").insert(item.dict()).execute()
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(status_code=400, detail="Supabase tidak mengembalikan data.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Supabase Error: {str(e)}")

@app.put("/api/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate):
    if not supabase:
        raise HTTPException(status_code=500, detail="Koneksi ke Supabase gagal.")
    try:
        # Filter hanya field yang tidak None
        update_data = {k: v for k, v in item.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="Tidak ada data yang diupdate.")
        
        response = supabase.table("items").update(update_data).eq("id", item_id).execute()
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(status_code=404, detail="Item tidak ditemukan.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Supabase Error: {str(e)}")

@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
    if not supabase:
        raise HTTPException(status_code=500, detail="Koneksi ke Supabase gagal.")
    try:
        response = supabase.table("items").delete().eq("id", item_id).execute()
        if response.data:
            return {"message": "Item berhasil dihapus", "deleted_id": item_id}
        else:
            raise HTTPException(status_code=404, detail="Item tidak ditemukan.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Supabase Error: {str(e)}")
