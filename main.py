from supabase import create_client, Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# https://docs.render.com/deploy-fastapi

url: str = "https://kbplgyruwwcqzurimbtg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImticGxneXJ1d3djcXp1cmltYnRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE1OTEwMjksImV4cCI6MjAyNzE2NzAyOX0.byS4R7u5YKG_0ud4pUU60mKVM1KIrE7qpTxmYgVNY_M"

supabase: Client = create_client(url, key)

app = FastAPI()

class ChocolateBar(BaseModel):
    id: Optional[int] = None
    company: Optional[str] = None
    specific_bean_origin_or_bar_name: Optional[str] = None
    ref: Optional[int] = None
    review_date: Optional[int] = None
    cocoa_percent: Optional[str] = None
    company_location: Optional[str] = None
    rating: Optional[float] = None
    bean_type: Optional[str] = None
    broad_bean_origin: Optional[str] = None

@app.post("/items/")
def create_item(item: ChocolateBar):
    data = supabase.table("chocolate").insert(item.dict()).execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=400, detail="Item could not be created")
        
@app.get("/items/")
def read_items():
    data = supabase.table("chocolate").select("*").execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=404, detail="Items not found")
    
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ChocolateBar):
    data = supabase.table("chocolate").update(item.dict()).eq("id", item_id).execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    data = supabase.table("chocolate").delete().eq("id", item_id).execute()
    if data.data:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
