import json
from typing import List

from sqlalchemy import URL, create_engine, text, VARCHAR, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


MYSQL_DRIVER = "mysql+mysqlconnector"
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "XXXXXXXXXXX"
MYSQL_HOST_NAME = "localhost"
MYSQL_PORT = 3306
DB_NAME = "imdb"


url_object = URL.create(
    MYSQL_DRIVER,
    username=MYSQL_USERNAME,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST_NAME,
    port=MYSQL_PORT,
)
engine = create_engine(url_object)


with engine.connect() as conn:
    conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
    conn.execute(text(f"CREATE DATABASE {DB_NAME}"))

url_object = URL.create(
    MYSQL_DRIVER,
    username=MYSQL_USERNAME,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST_NAME,
    port=MYSQL_PORT,
    database=DB_NAME,
)
engine = create_engine(url_object)

class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movie"

    id: Mapped[str] = mapped_column(VARCHAR(8), primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(128))
    year : Mapped[int] = mapped_column(Integer())
    runtime : Mapped[int] = mapped_column(Integer())
    parental_guide : Mapped[str] = mapped_column(VARCHAR(8))
    gross_us_canada : Mapped[int] = mapped_column(Integer(), nullable=True)
    rank : Mapped[int] = mapped_column(Integer())
    genres: Mapped[List["GenreMovie"]] = relationship(back_populates="movie")
    casts: Mapped[List["Cast"]] = relationship(back_populates="movie")
    crews: Mapped[List["Crew"]] = relationship(back_populates="movie")


class Person(Base):
    __tablename__ = "person"

    id: Mapped[str] = mapped_column(VARCHAR(8), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(32))
    casts: Mapped[List["Cast"]] = relationship(back_populates="person")
    crews: Mapped[List["Crew"]] = relationship(back_populates="person")


class Cast(Base):
    __tablename__ = "cast"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    movie: Mapped["Movie"] = relationship(back_populates="casts")
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"))
    person: Mapped["Person"] = relationship(back_populates="casts")


class Crew(Base):
    __tablename__ = "crew"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    movie: Mapped["Movie"] = relationship(back_populates="crews")
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"))
    person: Mapped["Person"] = relationship(back_populates="crews")
    role : Mapped[str] = mapped_column(VARCHAR(8))


class GenreMovie(Base):
    __tablename__ = "genre_movie"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    movie: Mapped["Movie"] = relationship(back_populates="genres")
    genre: Mapped[str] = mapped_column(VARCHAR(16))


Base.metadata.create_all(bind=engine)

session = Session(engine)

###########################################
### INSERT MOVIES
###########################################
with open('movies.json') as user_file:
  file_contents = user_file.read()
  parsed_json_1 = json.loads(file_contents)

for movie in parsed_json_1:
    new_data = Movie(
        id=movie['id'],
        title=movie['title'],
        year=movie['year'],
        runtime=movie['runtime'],
        parental_guide=movie['parental_guide'],
        gross_us_canada=movie['gross_us_canada'],
        rank=movie['rank'],
    )
    session.add(new_data)


###########################################
### INSERT GENRES
###########################################
with open('genres.json') as user_file:
  file_contents = user_file.read()
  parsed_json = json.loads(file_contents)

for genre in parsed_json:
    movie = session.get(Movie, genre['movie_id'])
    new_data = GenreMovie(
        movie=movie,
        genre=genre['genre']
    )
    session.add(new_data)


###########################################
### INSERT PEOPLE
###########################################
with open('people.json') as user_file:
  file_contents = user_file.read()
  parsed_json = json.loads(file_contents)

for person in parsed_json:
    person_record = session.get(Person, person['person_id'])
    if not person_record:
        new_data = Person(
            id = person['person_id'],
            name = person['name']
        )
        session.add(new_data)


###########################################
### INSERT CASTS
###########################################
with open('casts.json') as user_file:
  file_contents = user_file.read()
  parsed_json = json.loads(file_contents)

for cast in parsed_json:
    movie = session.get(Movie, cast['movie_id'])
    person = session.get(Person, cast['person_id'])
    new_data = Cast(
        movie=movie,
        person=person
    )
    session.add(new_data)


###########################################
### INSERT CREWS
###########################################
with open('crews.json') as user_file:
  file_contents = user_file.read()
  parsed_json = json.loads(file_contents)

for crew in parsed_json:
    movie = session.get(Movie, crew['movie_id'])
    person = session.get(Person, crew['person_id'])
    new_data = Crew(
        movie=movie,
        person=person,
        role=crew['role']
    )
    session.add(new_data)

###########################################

session.commit()
