from supabase import create_client, Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# Initialize Supabase client
url: str = "https://kbplgyruwwcqzurimbtg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImticGxneXJ1d3djcXp1cmltYnRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE1OTEwMjksImV4cCI6MjAyNzE2NzAyOX0.byS4R7u5YKG_0ud4pUU60mKVM1KIrE7qpTxmYgVNY_M"
supabase: Client = create_client(url, key)

# Initialize FastAPI app
app = FastAPI()

# Define Pydantic model for BlogPost
class BlogPost(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    author: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    published: bool

# Endpoint to create a new blog post
@app.post("/posts/", response_model=BlogPost)
def create_post(post: BlogPost):
    data = supabase.table("blog_posts").insert(post.dict()).execute()
    if data.data:
        return data.data[0]
    else:
        raise HTTPException(status_code=400, detail="Post could not be created")

# Endpoint to read all blog posts
@app.get("/posts/", response_model=List[BlogPost])
def read_posts():
    data = supabase.table("blog_posts").select("*").execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=404, detail="Posts not found")

# Endpoint to read a specific blog post by ID
@app.get("/posts/{post_id}", response_model=BlogPost)
def read_post(post_id: int):
    data = supabase.table("blog_posts").select("*").eq("id", post_id).execute()
    if data.data:
        return data.data[0]
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Endpoint to update a blog post by ID
@app.put("/posts/{post_id}", response_model=BlogPost)
def update_post(post_id: int, post: BlogPost):
    data = supabase.table("blog_posts").update(post.dict()).eq("id", post_id).execute()
    if data.data:
        return data.data[0]
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Endpoint to delete a blog post by ID
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    data = supabase.table("blog_posts").delete().eq("id", post_id).execute()
    if data.data:
        return {"message": "Post deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")
