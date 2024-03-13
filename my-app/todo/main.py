from fastapi import FastAPI
from todo import router

app = FastAPI()
app.include_router(router=router)

@app.get('/')
async def greet() -> dict:
    return {'message': 'hello world'}

