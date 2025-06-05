from etl.utils import load_json
from database.models import Genre, Movie, GenreMovie
from database.session import SessionLocal


def load_genres_to_db():
    genres = load_json('data/raw/genres_list.json')
    with SessionLocal() as session:
        for g in genres:
            session.merge(Genre(id=g["id"], title=g["name"]))
        session.commit()
    print(f"✅ Loaded {len(genres)} genres (insert/update safe).")


def load_movies_to_db():
    movies = load_json('data/raw/top_movies_info.json')
    with SessionLocal() as session:
        for movie_dict in movies:
            movie = Movie(
                id=movie_dict['id'],
                title=movie_dict['title'],
                runtime=int(movie_dict['runtime']),
                release_year=int(movie_dict['release_date'][:4]),
                origin_country=movie_dict['origin_country'][0],
                original_language=movie_dict['original_language'],
                budget=int(movie_dict['budget']),
                revenue=int(movie_dict['revenue']),
                vote_count=int(movie_dict['vote_count']),
                vote_average=float(movie_dict['vote_average']),
            )
            session.merge(movie)
            for genre in movie_dict['genres']:
                g_m = GenreMovie(
                    movie_id=movie_dict['id'],
                    genre_id=genre['id']
                )
                session.merge(g_m)
        session.commit()
    print(f"✅ Loaded {len(movies)} movies (insert/update safe).")
