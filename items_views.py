from typing import Annotated
from fastapi import APIRouter,Path
   


router = APIRouter(prefix="/items", tags=["Items"])
   
   
@router.get("/")
def list_item():
    return [
        "item_1",
        "item_2"
    ]
    
    
@router.get("/latets/")
def get_latets_item():
    return {
        "item": {"id": "0", "name": "latets"}
    }
    
    
@router.get("/{item_id}/")
def get_item_by_id(item_id: Annotated[int , Path(ge=1, lt=1_000_000)]):
    return {
        "item": {
            "id": item_id
        }
    }

