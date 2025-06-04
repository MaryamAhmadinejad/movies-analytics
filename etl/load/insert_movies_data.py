from etl.utils import load_json
from database.models import Movie
from database.session import SessionLocal


def load_to_sqlite():
    movies = load_json('data/raw/top_movies_info.json')
    with SessionLocal() as session:
        for movie_dict in movies:
            movie = Movie(
                id=movie_dict['id'],
                title=movie_dict['title'],
                runtime=int(movie_dict['runtime']),
                release_year=int(movie_dict['release_date'][:4]),
                original_language=movie_dict['original_language'],
                budget=int(movie_dict['budget']),
                revenue=int(movie_dict['revenue']),
                vote_count=int(movie_dict['vote_count']),
                vote_average=float(movie_dict['vote_average']),
            )
            session.merge(movie)
        session.commit()
    print(f"✅ Loaded {len(movies)} movies (insert/update safe).")
