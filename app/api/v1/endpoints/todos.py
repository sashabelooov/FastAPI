import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo import todo_service

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=list[TodoResponse])
async def get_all(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> list[TodoResponse]:
    return await todo_service.get_all(session, current_user)


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_one(
    todo_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> TodoResponse:
    return await todo_service.get_one(session, todo_id, current_user)


@router.post("/", response_model=TodoResponse, status_code=201)
async def create(
    data: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> TodoResponse:
    return await todo_service.create(session, data, current_user)


@router.patch("/{todo_id}", response_model=TodoResponse)
async def update(
    todo_id: uuid.UUID,
    data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> TodoResponse:
    return await todo_service.update(session, todo_id, data, current_user)


@router.delete("/{todo_id}", status_code=204)
async def delete(
    todo_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> None:
    await todo_service.delete(session, todo_id, current_user)