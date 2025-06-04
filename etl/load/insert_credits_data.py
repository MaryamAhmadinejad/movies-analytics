from etl.utils import load_json
from database.models import Person, Cast, Crew
from database.session import SessionLocal


def load_people_to_db():
    people = load_json('data/processed/people.json')
    with SessionLocal() as session:
        for person_dict in people:
            person = Person(
                id=person_dict['id'],
                name=person_dict['name'],
                gender=None if person_dict['gender'] == 'Unknown' else person_dict['gender']
            )
            session.merge(person)
        session.commit()
    print(f"✅ Loaded {len(people)} people (insert/update safe).")


def load_casts_and_crews_to_db():
    data = load_json('data/raw/top_movies_credits.json')
    with SessionLocal() as session:
        for d in data:
            movie_id = d['movie_id']
            for cast in d['cast']:
                cs = Cast(
                    id=cast['cast_id'],
                    movie_id=movie_id,
                    person_id=cast['id']
                )
                session.merge(cs)
            for crew in d['crew']:
                cr = Crew(
                    id=crew['credit_id'],
                    movie_id=movie_id,
                    person_id=crew['id'],
                    role=crew['job']
                )
                session.merge(cr)
        session.commit()
    print("✅ Loaded movies credits (insert/update safe).")
