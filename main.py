from supabase import create_client, Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from typing import List, Optional

# Initialize Supabase client
url: str = "https://kbplgyruwwcqzurimbtg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImticGxneXJ1d3djcXp1cmltYnRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE1OTEwMjksImV4cCI6MjAyNzE2NzAyOX0.byS4R7u5YKG_0ud4pUU60mKVM1KIrE7qpTxmYgVNY_M"
supabase: Client = create_client(url, key)

app = FastAPI()

# Pydantic model for Blog Post
class BlogPost(BaseModel):
    id: Optional[int]
    title: str
    content: str
    author: str

# Endpoint to create a new blog post
@app.post("/posts/", response_model=BlogPost)
def create_post(post: BlogPost):
    try:
        # Validate the incoming data using the BlogPost model
        post_data = post.dict()
        new_post = supabase.table("blog_posts").insert(post_data).execute()

        if new_post.data:
            return post  # Return the created blog post
        else:
            raise HTTPException(status_code=500, detail="Failed to create post")
    
    except ValidationError as e:
        # Handle validation errors (e.g., missing required fields)
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")

# Endpoint to read all blog posts
@app.get("/posts/", response_model=List[BlogPost])
def read_posts():
    posts_data = supabase.table("blog_posts").select("*").execute()

    if posts_data.data:
        return posts_data.data
    else:
        raise HTTPException(status_code=404, detail="No posts found")

# Endpoint to read a specific blog post
@app.get("/posts/{post_id}", response_model=BlogPost)
def read_post(post_id: int):
    post_data = supabase.table("blog_posts").select("*").eq("id", post_id).execute()

    if post_data.data:
        return post_data.data[0]
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Endpoint to update a blog post
@app.put("/posts/{post_id}", response_model=BlogPost)
def update_post(post_id: int, post: BlogPost):
    try:
        updated_post = supabase.table("blog_posts").update(post.dict()).eq("id", post_id).execute()

        if updated_post.data:
            return post  # Return the updated blog post
        else:
            raise HTTPException(status_code=404, detail="Post not found")

    except ValidationError as e:
        # Handle validation errors during update
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")

# Endpoint to delete a blog post
@app.delete("/posts/{post_id}", response_model=dict)
def delete_post(post_id: int):
    deleted_post = supabase.table("blog_posts").delete().eq("id", post_id).execute()

    if deleted_post.data:
        return {"message": "Post deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")
