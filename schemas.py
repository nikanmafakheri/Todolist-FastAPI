from pydantic import BaseModel

class ItemSchema(BaseModel):
  id : int
  name : str 
  description : str
  
  class config:
    orm_mode = True