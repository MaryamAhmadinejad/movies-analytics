from etl.utils import load_json
from database.models import Person
from database.session import SessionLocal


def load_to_sqlite():
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
