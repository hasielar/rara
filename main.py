from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Define Pydantic model for BlogPost
class BlogPost(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    author: str

# Simulated in-memory database (replace with Supabase integration)
blog_posts = []

# Endpoint to create a new blog post
@app.post("/posts/", response_model=BlogPost)
def create_post(post: BlogPost):
    blog_posts.append(post)
    return post

# Endpoint to read all blog posts
@app.get("/posts/", response_model=List[BlogPost])
def read_posts():
    return blog_posts

# Endpoint to read a specific blog post by ID
@app.get("/posts/{post_id}", response_model=BlogPost)
def read_post(post_id: int):
    for post in blog_posts:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

# Endpoint to update a blog post by ID
@app.put("/posts/{post_id}", response_model=BlogPost)
def update_post(post_id: int, post: BlogPost):
    for idx, existing_post in enumerate(blog_posts):
        if existing_post.id == post_id:
            blog_posts[idx] = post
            return post
    raise HTTPException(status_code=404, detail="Post not found")

# Endpoint to delete a blog post by ID
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    for idx, post in enumerate(blog_posts):
        if post.id == post_id:
            del blog_posts[idx]
            return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")
