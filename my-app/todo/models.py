from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Form

class Todo(BaseModel):
    id: Optional[int] = Field(None) 
    name: str 
    surname: str
    age: int
    email: str

    @classmethod
    def as_form(cls, id: int = Form(None), name: str = Form(...),
                surname: str = Form(...), age: int = Form(...),
                email: str = Form(..., pattern='[A-Za-z]{1,}@(hotmail|gmail|outlook|misena).(com|es|co)')):
        
        return cls(id=id, name=name, surname=surname, age=age, email=email)

 