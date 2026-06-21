from fastapi import FastAPI, HTTPException, Response, Depends
import model as mdl
from database import engine, SessionLocal
from sqlalchemy.orm import Session 
import db_models

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=list[mdl.NoteResponse])
async def home_page(db: Session = Depends(get_db)):
    notes = db.query(db_models.Note).all()
    return notes

@app.get("/notes/{id}", response_model=mdl.NoteResponse)
async def view_note(id: int, db: Session = Depends(get_db)):

    note = (db.query(db_models.Note).filter(db_models.Note.id == id).first())
    if note is None:
        raise HTTPException(status_code=404, detail="Not Found")
    
    return note

@app.post("/notes", response_model=mdl.NoteResponse, status_code=201)
async def create_note(note: mdl.NoteCreate, db: Session = Depends(get_db)):

    new_note = db_models.Note(
        notes_title=note.notes_title,
        content=note.content)

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note
    
@app.patch("/notes/{id}", response_model=mdl.NoteResponse)
async def update_note(id: int, note: mdl.NoteUpdate, db: Session = Depends(get_db)):

    note_to_update = (db.query(db_models.Note).filter(db_models.Note.id == id).first())
         
    if note_to_update is None:
        raise HTTPException(status_code=404, detail="Not Found")
    
    if note.notes_title is not None:
        note_to_update.notes_title = note.notes_title

    if note.content is not None:
        note_to_update.content = note.content

    db.commit()

    db.refresh(note_to_update)

    return note_to_update

@app.delete("/notes/{id}")
async def delete_note(id: int, db: Session = Depends(get_db)):
    note = (db.query(db_models.Note).filter(db_models.Note.id == id).first())

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Not Found"
        )
    
    db.delete(note)

    db.commit()

    return Response(status_code=204)