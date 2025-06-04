from typing import List, Optional
from sqlalchemy import VARCHAR, Integer, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(32))

    movies: Mapped[List["GenreMovie"]] = relationship(back_populates="genre")


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(128))
    release_year: Mapped[int] = mapped_column(Integer())
    original_language: Mapped[str] = mapped_column(VARCHAR(8))
    runtime: Mapped[int] = mapped_column(Integer())
    budget: Mapped[int] = mapped_column(Integer())
    revenue: Mapped[int] = mapped_column(Integer())
    vote_count: Mapped[int] = mapped_column(Integer())
    vote_average: Mapped[float] = mapped_column(Float())

    genres: Mapped[List["GenreMovie"]] = relationship(back_populates="movie")
    casts: Mapped[List["Cast"]] = relationship(back_populates="movie")
    crews: Mapped[List["Crew"]] = relationship(back_populates="movie")


class GenreMovie(Base):
    __tablename__ = "genre_movie"

    movie_id: Mapped[str] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)

    movie: Mapped["Movie"] = relationship(back_populates="genres")
    genre: Mapped["Genre"] = relationship(back_populates="movies")


class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(32))
    gender: Mapped[Optional[str]] = mapped_column(VARCHAR(16), nullable=True)

    casts: Mapped[List["Cast"]] = relationship(back_populates="person")
    crews: Mapped[List["Crew"]] = relationship(back_populates="person")


class Cast(Base):
    __tablename__ = "casts"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"))

    movie: Mapped["Movie"] = relationship(back_populates="casts")
    person: Mapped["Person"] = relationship(back_populates="casts")


class Crew(Base):
    __tablename__ = "crews"

    id: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    role: Mapped[str] = mapped_column(VARCHAR(8))

    movie: Mapped["Movie"] = relationship(back_populates="crews")
    person: Mapped["Person"] = relationship(back_populates="crews")
