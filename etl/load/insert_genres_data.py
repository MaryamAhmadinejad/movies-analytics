from etl.utils import load_json
from database.models import Genre
from database.session import SessionLocal


def load_to_sqlite():
    genres = load_json('data/raw/genres_list.json')
    with SessionLocal() as session:
        for g in genres:
            session.merge(Genre(id=g["id"], title=g["name"]))
        session.commit()
    print(f"✅ Loaded {len(genres)} genres (insert/update safe).")
