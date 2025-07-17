from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# PUBLIC_INTERFACE
class UserCreate(BaseModel):
    """Request model for user registration."""
    username: str = Field(..., description="Unique username for the user")
    password: str = Field(..., description="Password for the user (plaintext, will be hashed)")

# PUBLIC_INTERFACE
class UserLogin(BaseModel):
    """Request model for user login."""
    username: str = Field(..., description="User's username")
    password: str = Field(..., description="User's password")

# PUBLIC_INTERFACE
class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"

# PUBLIC_INTERFACE
class NoteCreate(BaseModel):
    """Request model to create a note."""
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content of the note")

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Request model to update a note."""
    title: Optional[str] = Field(None, description="Title of the note")
    content: Optional[str] = Field(None, description="Content of the note")

# PUBLIC_INTERFACE
class NoteOut(BaseModel):
    """Response model for a Note."""
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
