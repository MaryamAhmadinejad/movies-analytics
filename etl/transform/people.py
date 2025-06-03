from etl.utils import load_json, save_json
from etl.extract.consts import RAW_TOP_RATED_MOVIES_CREDITS_PATH


def extract_unique_people(input_data, gender_map) -> list:
    people = []
    seen_people_id = set()
    for movie in input_data:
        full_crew = movie.get('cast', []) + movie.get('crew', [])
        for c in full_crew:
            c_id = c['id']
            person = {
                'id': c_id,
                'original_name': c['original_name'],
                'name': c['name'],
                'gender': gender_map.get(str(c['gender']), 'Unknown')
            }
            if c_id not in seen_people_id:
                people.append(person)
                seen_people_id.add(c_id)
    return people


if __name__ == '__main__':
    movies = load_json(RAW_TOP_RATED_MOVIES_CREDITS_PATH)
    gender_map = load_json('data/processed/gender_map.json')
    people = extract_unique_people(movies, gender_map)
    print(f"✅ Extracted {len(people)} unique people.")
    save_json(people, 'data/processed/people.json')
