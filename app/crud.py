from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Book, Review
from .schemas import BookCreate, ReviewCreate

class BookCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_books(self):
        result = await self.session.execute(select(Book))
        return result.scalars().all()

    async def get_book(self, book_id: int):
        return await self.session.get(Book, book_id)

    async def create_book(self, book: BookCreate):
        new_book = Book(**book.dict())
        self.session.add(new_book)
        await self.session.commit()
        return new_book

    async def update_book(self, book_id: int, book: BookCreate):
        existing_book = await self.get_book(book_id)
        for field, value in book.dict().items():
            setattr(existing_book, field, value)
        await self.session.commit()
        return existing_book

    async def delete_book(self, book_id: int):
        book = await self.get_book(book_id)
        await self.session.delete(book)
        await self.session.commit()

class ReviewCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_review(self, review: ReviewCreate):
        new_review = Review(**review.dict())
        self.session.add(new_review)
        await self.session.commit()
        return new_review
