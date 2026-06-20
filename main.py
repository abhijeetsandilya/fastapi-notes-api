from fastapi import FastAPI, HTTPException, Response
import model as mdl

app = FastAPI()

data = [
    {"id": 1,
     "notes_title": "Notes_1",
     "content": "hola, como estas?"
     },
     {"id": 2,
     "notes_title": "Notes_2",
     "content": "estoy Bien, y tu?"        
     }
]

@app.get("/")
async def home_page():
    return data

@app.get("/notes/{id}", response_model=mdl.NoteResponse)
async def view_note(id: int):
    for i in data:
        if i["id"] == id:
            return i  
         
    raise HTTPException(status_code=404, detail="Not Found")

@app.post("/notes", response_model=mdl.NoteResponse, status_code=201)
async def create_note(note: mdl.NoteCreate):

    new_note = {
        "id": data[-1]["id"] + 1,
        "notes_title": note.notes_title,
        "content": note.content
    }

    data.append(new_note)

    return new_note
    
@app.patch("/notes/{id}", response_model=mdl.NoteResponse)
async def update_note(id: int, note: mdl.NoteUpdate):

    for i in data:
        if i["id"] == id:
            
            if note.notes_title is not None:
                i["notes_title"] = note.notes_title

            if note.content is not None:
                i["content"] = note.content

            return i

    raise HTTPException(status_code=404, detail="Not Found")

@app.delete("/notes/{id}")
async def delete_note(id: int):
    for i in data:
        if i["id"] == id:
            data.remove(i)
            return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Not Found")