from dataclasses import dataclass


@dataclass
class Movie:
    movie_id: int
    title: str
    genres: list[str]


@dataclass
class Rating:
    user_id: str
    movie_id: int
    rating: float


class CriticService:
    def __init__(self):
        self.movies = [
            Movie(1, "The Matrix", ["Action", "Sci-Fi"]),
            Movie(2, "Toy Story", ["Animation", "Comedy"]),
            Movie(3, "The Godfather", ["Crime", "Drama"]),
            Movie(4, "Jurassic Park", ["Adventure", "Sci-Fi"]),
            Movie(5, "Groundhog Day", ["Comedy", "Romance"]),
            Movie(6, "Alien", ["Horror", "Sci-Fi"]),
            Movie(7, "Good Will Hunting", ["Drama"]),
            Movie(8, "The Princess Bride", ["Adventure", "Comedy"]),
            Movie(9, "Heat", ["Crime", "Action"]),
            Movie(10, "Finding Nemo", ["Animation", "Adventure"]),
        ]

        self.ratings: list[Rating] = []

    def list_movies(self) -> list[Movie]:
        return self.movies

    def add_rating(self, user_id: str, movie_id: int, rating: float) -> Rating:
        if rating < 0.5 or rating > 5:
            raise ValueError("Rating must be between 0.5 and 5.0")

        movie_exists = any(movie.movie_id == movie_id for movie in self.movies)
        if not movie_exists:
            raise ValueError(f"Movie {movie_id} does not exist")

        existing = next(
            (
                saved_rating
                for saved_rating in self.ratings
                if saved_rating.user_id == user_id and saved_rating.movie_id == movie_id
            ),
            None,
        )

        if existing:
            existing.rating = rating
            return existing

        new_rating = Rating(user_id=user_id, movie_id=movie_id, rating=rating)
        self.ratings.append(new_rating)
        return new_rating

    def get_user_ratings(self, user_id: str) -> list[Rating]:
        return [rating for rating in self.ratings if rating.user_id == user_id]

    def recommend(self, user_id: str, limit: int = 5) -> list[Movie]:
        user_ratings = self.get_user_ratings(user_id)
        rated_movie_ids = {rating.movie_id for rating in user_ratings}

        liked_movie_ids = {
            rating.movie_id for rating in user_ratings if rating.rating >= 4.0
        }

        liked_genres = set()
        for movie in self.movies:
            if movie.movie_id in liked_movie_ids:
                liked_genres.update(movie.genres)

        unrated_movies = [
            movie for movie in self.movies if movie.movie_id not in rated_movie_ids
        ]

        ranked = sorted(
            unrated_movies,
            key=lambda movie: len(set(movie.genres).intersection(liked_genres)),
            reverse=True,
        )

        return ranked[:limit]