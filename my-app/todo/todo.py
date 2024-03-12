from fastapi import APIRouter, Path, HTTPException, status, Request, Depends
from pydantic_core import PydanticCustomError
from typing import List, Dict, Optional
from fastapi.templating import Jinja2Templates
from models import Todo


todo_list = []

templates = Jinja2Templates(directory='templates/') # Here we set the templates folder

router = APIRouter()



@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def append(request: Request, todo: Todo = Depends(Todo.as_form)) -> Todo:
    todo_list.append(todo)
    return templates.TemplateResponse('todo.html', {'request': request, 
                                                    'todos': todo_list})


@router.get('/todo') 
async def retrieve(request: Request) -> Todo:
    return templates.TemplateResponse(
        'todo.html', {'request': request, 'todos': todo_list}
    )

@router.get('/todo_get/{todo_name}')
async def get_todo_name(todo_name: str = Path(..., title='This is the search by name')) -> Todo:
    name = [i for i in todo_list if i.name == todo_name]
    if not name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The user was not found')
    return name[0]


@router.put('/todo/{todo_id}')
async def update(todo_data: Todo, todo_id: int = Path(title='The ID of the todo to be updated')) -> dict:
    for i, n in enumerate(todo_list):
        if n.id == todo_id:
            todo_list[i] = todo_data
            return {'message': 'The user has been updated.'}
    

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='The user was not found.')


@router.delete('/todo_del_id/{todo_id}')
async def delete_user(todo_id: int = Path(title='Deleting user through id path.')) -> dict:
    for index, value in enumerate(todo_list):
        if value.id == todo_id:
            del todo_list[index]
            return {'message': 'The user has been deleted correctly.'}

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='The user was not found.')


@router.delete('/todo_del')
async def delete_user_complete() -> dict:
    todo_list.clear()
    return {
        "message": "The database has been deleted."
    }     


"""curl -X 'GET' 'http://127.0.0.1:8000/hello' -H 'accept: application/json'"""
# 'curl' is the command used for transfering data with URLs
# '-H' 'accept: application/json' = This is a custom http header that expects a json data response.

"""curl -X 'POST' `
'http://127.0.0.1:8000/todo' `
-H 'accept: application/json' `
-H 'Content-Type: application/json' `
-d '{
"id": 1,
"item": "First Todo is to finish this book!"
}'"""

# On this one we have another header constriction and '-d' as the given values.
