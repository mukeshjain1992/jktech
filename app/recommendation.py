class RecommendationSystem:
    def recommend_books(self, books, genre: str):
        # Simple content-based filtering based on genre
        return [book for book in books if book.genre == genre]
