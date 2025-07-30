from fastapi import FastAPI , Depends , HTTPException
from models import Item
from schemas import ItemBase , ItemCreate , ItemRead
from database import SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()  

@app.get("/")
def read_root():
  return {"msg" : "first page"}

@app.post("/items/", response_model=ItemCreate)
def create_item(item : ItemCreate, db : Session = Depends(get_db)):
  db_item = Item(**item.model_dump())
  db.add (db_item)
  db.commit()
  db.refresh(db_item)
  return db_item

@app.get("/items/{item_id}", response_model=ItemRead)
def read_item(item_id: int , db : Session = Depends(get_db)):
  item = db.query(Item).filter(Item.id == item_id).first()
  if not item:
    raise HTTPException(status_code=404)
  return item
  
@app.get("/items/", response_model= list[ItemRead])
def read_item(db : Session = Depends(get_db)):
  return db.query(Item).all()