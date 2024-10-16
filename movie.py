from typing import List, Optional

import pydantic


class RatingsMissingError(Exception):
    """Custom error that is raised when both IMDb and Rotten Tomatoes ratings are missing."""

    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message
        super().__init__(message)


class IMDbRatingFormatError(Exception):
    """Custom error that is raised when IMDb rating doesn't have the right format."""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class Director(pydantic.BaseModel):
    name: str
    verified: bool


class Movie(pydantic.BaseModel):
    """Represents a movie"""

    title: str
    director: str
    producer: str
    box_office: float
    imdb_rating: Optional[str]
    rotten_tomatoes_rating: Optional[str]
    genre: Optional[str]
    director_details: Optional[Director]

    @pydantic.root_validator(pre=True)
    @classmethod
    def check_ratings(cls, values):
        """Make sure there is either an IMDb rating or Rotten Tomatoes rating defined."""
        if "imdb_rating" not in values and "rotten_tomatoes_rating" not in values:
            raise RatingsMissingError(
                title=values["title"],
                message="Movie should have either an IMDb rating or Rotten Tomatoes rating.",
            )
        return values

    @pydantic.validator("imdb_rating")
    def imdb_rating_valid(cls, value) -> None:
        """Validator to check whether IMDb rating is valid"""
        if not (0 <= float(value) <= 10):
            raise IMDbRatingFormatError(
                value=value, message="IMDb rating should be between 0 and 10."
            )
        return value


def main() -> None:
    """Main function."""

    movies: List[Movie] = [
        Movie(
            title="Inception",
            director="Christopher Nolan",
            producer="Emma Thomas",
            box_office=829895144.00,
            imdb_rating="8.8",
            rotten_tomatoes_rating="87%",
            genre="Sci-Fi",
            director_details=Director(name="Christopher Nolan", verified=True)
        ),]
    
    print(movies[0])


if __name__ == "__main__":
    main()
