from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, field_validator
from contextlib import asynccontextmanager

from sqlalchemy import Column, Integer, String, Float, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///./demo.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)



AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)


Base = declarative_base()


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    salery = Column(Float, index=True)
    
    
async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    salery: float
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value: str):
        if not value.startswith("+"):
            raise ValueError("Phone number must start with '+' ")
        if not value[1:].isdigit():
            raise ValueError("Phone number must contain digits only after '+' ")
        
        return value
    


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    salery: float
    
    model_config = {"from_attributes": True}
    
    
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
        
        
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield
    
app = FastAPI(lifespan=lifespan)


@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        salery=user.salery
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user