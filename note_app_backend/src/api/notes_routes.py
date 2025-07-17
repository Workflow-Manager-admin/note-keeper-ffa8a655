from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models
from .database_models import Note
from .db import get_db
from .auth_routes import get_current_user

router = APIRouter(prefix="/notes", tags=["notes"])

# PUBLIC_INTERFACE
@router.post("/", response_model=models.NoteOut, summary="Create Note")
def create_note(note: models.NoteCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Create a new note for the current user.
    """
    db_note = Note(
        user_id=user.id,
        title=note.title,
        content=note.content
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# PUBLIC_INTERFACE
@router.get("/", response_model=List[models.NoteOut], summary="List Notes")
def list_notes(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    q: Optional[str] = Query(None, description="Search query for note title or content"),
):
    """
    List all notes for the current user. Optionally search by title/content.
    """
    query = db.query(Note).filter(Note.user_id == user.id)
    if q:
        query = query.filter((Note.title.ilike(f"%{q}%")) | (Note.content.ilike(f"%{q}%")))
    return query.order_by(Note.updated_at.desc()).all()

# PUBLIC_INTERFACE
@router.get("/{note_id}", response_model=models.NoteOut, summary="Get Note")
def get_note(note_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Get a single note by ID.
    """
    note = db.query(Note).filter_by(id=note_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# PUBLIC_INTERFACE
@router.put("/{note_id}", response_model=models.NoteOut, summary="Update Note")
def update_note(note_id: int, note_in: models.NoteUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Update a note by ID.
    """
    note = db.query(Note).filter_by(id=note_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note_in.title is not None:
        note.title = note_in.title
    if note_in.content is not None:
        note.content = note_in.content
    db.commit()
    db.refresh(note)
    return note

# PUBLIC_INTERFACE
@router.delete("/{note_id}", status_code=204, summary="Delete Note")
def delete_note(note_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Delete a note by ID.
    """
    note = db.query(Note).filter_by(id=note_id, user_id=user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
