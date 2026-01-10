from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import uvicorn

from items_views import router as items_router
from users.views import router as user_router


app = FastAPI()
app.include_router(items_router)
app.include_router(user_router)




@app.get("/")
def hello_user():
    return {
        "message": "First function hello!"
    }
    
 
@app.get("/hello/")
def hello(name: str = "World"):
     name = name.strip().title()
     return {
         "message": f"Hello {name}"
     }
 
 

 

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)