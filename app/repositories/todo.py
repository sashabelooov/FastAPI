import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoRepository:
    async def get_by_id(self, session: AsyncSession, todo_id: uuid.UUID) -> Todo | None:
        result = await session.execute(select(Todo).where(Todo.id == todo_id))
        return result.scalar_one_or_none()

    async def get_all_by_owner(self, session: AsyncSession, owner_id: uuid.UUID) -> list[Todo]:
        result = await session.execute(select(Todo).where(Todo.owner_id == owner_id))
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, data: TodoCreate, owner_id: uuid.UUID) -> Todo:
        todo = Todo(**data.model_dump(), owner_id=owner_id)
        session.add(todo)
        await session.commit()
        await session.refresh(todo)
        return todo

    async def update(self, session: AsyncSession, todo: Todo, data: TodoUpdate) -> Todo:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(todo, field, value)
        await session.commit()
        await session.refresh(todo)
        return todo

    async def delete(self, session: AsyncSession, todo: Todo) -> None:
        await session.delete(todo)
        await session.commit()


todo_repository = TodoRepository()