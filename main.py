from supabase import create_client, Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Initialize Supabase client
url: str = "https://ufbqvjyfkiqdctvdvzsr.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYnF2anlma2lxZGN0dmR2enNyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTIyOTgzMDAsImV4cCI6MjAyNzg3NDMwMH0.zT8tWhhi3xM-7WysTAAW7fUj-iUIMaQHvjnO13eXgCE"
supabase: Client = create_client(url, key)

# Initialize FastAPI app
app = FastAPI()

# Define Pydantic model for BlogPost
class BlogPost(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    author: str

# Endpoint to create a new blog post
@app.post("/posts/")
def create_post(post: BlogPost):
    data = supabase.table("blog_posts").insert(post.dict()).execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=400, detail="Post could not be created")

# Endpoint to read all blog posts
@app.get("/posts/")
def read_posts():
    data = supabase.table("blog_posts").select("*").execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=404, detail="Posts not found")

# Endpoint to read a specific blog post
@app.get("/posts/{post_id}")
def read_post(post_id: int):
    data = supabase.table("blog_posts").select("*").eq("id", post_id).execute()
    if data.data:
        return data.data[0]
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Endpoint to update a blog post
@app.put("/posts/{post_id}")
def update_post(post_id: int, post: BlogPost):
    data = supabase.table("blog_posts").update(post.dict()).eq("id", post_id).execute()
    if data.data:
        return {"message": "Post updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Endpoint to delete a blog post
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    data = supabase.table("blog_posts").delete().eq("id", post_id).execute()
    if data.data:
        return {"message": "Post deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")
