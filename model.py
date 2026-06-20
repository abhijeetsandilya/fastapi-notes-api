from typing import Optional
from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    notes_title : str = Field(min_length=1, max_length=100)
    content : Optional[str] = None

class NoteUpdate(BaseModel):
    notes_title : str | None = None
    content : str | None = None

class NoteResponse(BaseModel):
    id: int
    notes_title: str
    content: str