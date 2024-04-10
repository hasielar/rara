from typing import Optional
from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from redis import Redis
from supabase_py import create_client, Client

app = FastAPI()
redis_conn = Redis()

class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    posted_at: datetime
    scheduled_at: Optional[datetime]

# Initialize Supabase client
url: str = "https://ufbqvjyfkiqdctvdvzsr.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYnF2anlma2lxZGN0dmR2enNyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTIyOTgzMDAsImV4cCI6MjAyNzg3NDMwMH0.zT8tWhhi3xM-7WysTAAW7fUj-iUIMaQHvjnO13eXgCE"
supabase: Client = create_client(url, key)

def create_post(post: Post):
    data = supabase.table("blog_posts").insert(post.dict(exclude={"id"})).execute()
    post.id = data.inserted[0]
    return post

@app.post("/posts/")
async def create_post_endpoint(post: Post):
    return create_post(post)

@app.get("/posts/{post_id}")
async def get_post_endpoint(post_id: int):
    post = supabase.table("blog_posts").select("*").eq("id", post_id).execute().data[0]
    return post

@app.put("/posts/{post_id}")
async def update_post_endpoint(post_id: int, post: Post):
    post_dict = post.dict()
    post_dict["updated_at"] = datetime.utcnow()
    supabase.table("blog_posts").update(post_dict).eq("id", post_id).execute()
    return {"message": "Post updated successfully"}

@app.get("/posts/")
async def get_posts_endpoint():
    posts = supabase.table("blog_posts").select("*").execute().data
    return posts

@app.delete("/posts/{post_id}")
async def delete_post_endpoint(post_id: int):
    post = supabase.table("blog_posts").delete().eq("id", post_id).execute()
    if post.deleted == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
