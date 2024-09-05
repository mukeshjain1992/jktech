from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .crud import BookCRUD, ReviewCRUD
from .llama3 import Llama3Model
from .recommendation import RecommendationSystem
from .schemas import BookCreate, ReviewCreate
from .config import DATABASE_URL

app = FastAPI()

# Create async engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Dependency for getting the DB session
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Initialize Llama3 and Recommendation Systems
llama_model = Llama3Model()
recommendation_system = RecommendationSystem()

# API Endpoints

@app.post("/books", response_model=BookCreate)
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_session)):
    book_crud = BookCRUD(session)
    summary = llama_model.generate_summary(book.title)  # Generate summary
    book.summary = summary
    return await book_crud.create_book(book)

@app.get("/books", response_model=List[BookCreate])
async def get_books(session: AsyncSession = Depends(get_session)):
    book_crud = BookCRUD(session)
    return await book_crud.get_books()

@app.get("/books/{book_id}", response_model=BookCreate)
async def get_book(book_id: int, session: AsyncSession = Depends(get_session)):
    book_crud = BookCRUD(session)
    book = await book_crud.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}")
async def update_book(book_id: int, book: BookCreate, session: AsyncSession = Depends(get_session)):
    book_crud = BookCRUD(session)
    return await book_crud.update_book(book_id, book)

@app.delete("/books/{book_id}")
async def delete_book(book_id: int, session: AsyncSession = Depends(get_session)):
    book_crud = BookCRUD(session)
    return await book_crud.delete_book(book_id)

@app.post("/books/{book_id}/reviews", response_model=ReviewCreate)
async def create_review(book_id: int, review: ReviewCreate, session: AsyncSession = Depends(get_session)):
    review_crud = ReviewCRUD(session)
    return await review_crud.create_review(review)

@app.get("/recommendations")
async def get_recommendations(genre: str, session: AsyncSession = Depends(get_session)):
    book_crud = BookCRUD(session)
    books = await book_crud.get_books()
    return recommendation_system.recommend_books(books, genre)
