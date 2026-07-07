from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.critic_service import CriticService


app = FastAPI(
    title="Movie Recommendation API",
    description="A starter API for a PyTorch-powered movie recommendation demo.",
    version="0.1.0",
)

service = CriticService()


class MovieResponse(BaseModel):
    movie_id: int
    title: str
    genres: list[str]


class RatingRequest(BaseModel):
    user_id: str = Field(min_length=1)
    movie_id: int
    rating: float = Field(ge=0.5, le=5.0)


class RatingResponse(BaseModel):
    user_id: str
    movie_id: int
    rating: float


@app.get("/")
def root():
    return {
        "message": "Movie Recommendation API is running",
        "docs": "/docs",
    }


@app.get("/movies", response_model=list[MovieResponse])
def list_movies():
    return service.list_movies()


@app.post("/ratings", response_model=RatingResponse)
def add_rating(request: RatingRequest):
    try:
        return service.add_rating(
            user_id=request.user_id,
            movie_id=request.movie_id,
            rating=request.rating,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.get("/users/{user_id}/ratings", response_model=list[RatingResponse])
def get_user_ratings(user_id: str):
    return service.get_user_ratings(user_id)


@app.get("/users/{user_id}/recommendations", response_model=list[MovieResponse])
def recommend_movies(user_id: str, limit: int = 5):
    return service.recommend(user_id=user_id, limit=limit)