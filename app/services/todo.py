import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo
from app.models.user import User
from app.repositories.todo import todo_repository
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate


class TodoService:
    async def get_all(self, session: AsyncSession, current_user: User) -> list[TodoResponse]:
        todos = await todo_repository.get_all_by_owner(session, current_user.id)
        return [TodoResponse.model_validate(t) for t in todos]

    async def get_one(
        self, session: AsyncSession, todo_id: uuid.UUID, current_user: User
    ) -> TodoResponse:
        todo = await self._get_owned_todo(session, todo_id, current_user)
        return TodoResponse.model_validate(todo)

    async def create(
        self, session: AsyncSession, data: TodoCreate, current_user: User
    ) -> TodoResponse:
        todo = await todo_repository.create(session, data, current_user.id)
        return TodoResponse.model_validate(todo)

    async def update(
        self, session: AsyncSession, todo_id: uuid.UUID, data: TodoUpdate, current_user: User
    ) -> TodoResponse:
        todo = await self._get_owned_todo(session, todo_id, current_user)
        updated = await todo_repository.update(session, todo, data)
        return TodoResponse.model_validate(updated)

    async def delete(
        self, session: AsyncSession, todo_id: uuid.UUID, current_user: User
    ) -> None:
        todo = await self._get_owned_todo(session, todo_id, current_user)
        await todo_repository.delete(session, todo)

    async def _get_owned_todo(
        self, session: AsyncSession, todo_id: uuid.UUID, current_user: User
    ) -> Todo:
        todo = await todo_repository.get_by_id(session, todo_id)
        if todo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        if todo.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return todo


todo_service = TodoService()