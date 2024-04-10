from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import supabase

url = "https://ufbqvjyfkiqdctvdvzsr.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYnF2anlma2lxZGN0dmR2enNyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTIyOTgzMDAsImV4cCI6MjAyNzg3NDMwMH0.zT8tWhhi3xM-7WysTAAW7fUj-iUIMaQHvjnO13eXgCE"

supabase_client = supabase.create_client(url, key)

class BlogPost(BaseModel):
    """
    A Pydantic model representing a blog post.

    Attributes:
        id (int, optional): The ID of the blog post.
        author (str): The author of the blog post.
        title (str): The title of the blog post.
        content (str): The content of the blog post.
        created_at (datetime): The date and time the blog post was created.
        updated_at (datetime): The date and time the blog post was last updated.
        posted_at (datetime): The date and time the blog post was posted.
        scheduled_at (datetime): The date and time the blog post is scheduled to be posted.
    """
    id: Optional[int] = None
    author: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    posted_at: datetime
    scheduled_at: datetime

    class Config:
        """
        Pydantic configuration for the BlogPost model.

        Attributes:
            orm_mode (bool): Whether to enable ORM mode, allowing Pydantic to automatically convert database rows to BlogPost instances.
        """
        orm_mode = True

@app.post("/blog_posts/", response_model=BlogPost)
async def create_blog_post(blog_post: BlogPost):
    """
    Create a new blog post.

    Args:
        blog_post (BlogPost): The blog post to create.

    Returns:
        BlogPost: The created blog post.
    """
    result = supabase_client.from("blog_posts").insert(blog_post.dict()).execute()
    return result.data[0]

@app.get("/blog_posts/{blog_id}", response_model=BlogPost)
async def get_blog_post(blog_id: int):
    """
    Retrieve a blog post by ID.

    Args:
        blog_id (int): The ID of the blog post to retrieve.

    Returns:
        BlogPost: The retrieved blog post.
    """
    result = supabase_client.from("blog_posts").select("*").eq("id", blog_id).execute()
    return result.data[0]

@app.get("/blog_posts/", response_model=List[BlogPost])
async def get_all_blog_posts():
    """
    Retrieve all blog posts.

    Returns:
        List[BlogPost]: A list of all blog posts.
    """
    result = supabase_client.from("blog_posts").select("*").execute()
    return result.data

@app.put("/blog_posts/{blog_id}", response_model=BlogPost)
async def update_blog_post(blog_id: int, blog_post: BlogPost):
    """
    Update a blog post by ID.

    Args:
        blog_id (int): The ID of the blog post to update.
        blog_post (BlogPost): The updated blog post.

    Returns:
        BlogPost: The updated blog post.
    """
    result = supabase_client.from("blog_posts").update(blog_post.dict()).eq("id", blog_id).execute()
    return result.data[0]

@app.delete("/blog_posts/{blog_id}")
async def delete_blog_post(blog_id: int):
    """
    Delete a blog post by ID.

    Args:
        blog_id (int): The ID of the blog post to delete.

    Returns:
        dict: A dictionary containing a message indicating that the blog post was deleted.
    """
    result = supabase_client.from("blog_posts").delete().eq("id", blog_id).execute()
    return {"message": "Blog post deleted"}
