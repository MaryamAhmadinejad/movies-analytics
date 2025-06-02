import json
import requests
from consts import TMDB_BASE_API_URL_V3, TMDB_API_KEY, RAW_TOP_RATED_MOVIES_LIST_DATA_PATH, RAW_TOP_RATED_MOVIES_INFO_PATH


def fetch_movie_credits(movie_id: int, movie_name: str) -> dict:
    print(f'🎬 Fetching credits for movie ID {movie_id}: {movie_name}...')
    url = f'{TMDB_BASE_API_URL_V3}/movie/{movie_id}/credits'
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            'cast': data.get('cast', []),
            'crew': data.get('crew', [])
        }
    except requests.RequestException as e:
        print(f"❌ Failed to fetch credits for {movie_name} ({movie_id}): {e}")
        return {'cast': [], 'crew': []}


def enrich_movies_with_credits() -> list:
    with open(RAW_TOP_RATED_MOVIES_LIST_DATA_PATH, 'r', encoding='utf-8') as f:
        top_movies = json.load(f)
    for top_movie in top_movies:
        movie_id = top_movie['id']
        movie_name = top_movie['title']
        credits = fetch_movie_credits(movie_id, movie_name)
        top_movie['cast'] = credits['cast']
        top_movie['crew'] = credits['crew']
    return top_movies


def save_movies_data(movies: list) -> None:
    print(f'✅ Got {len(movies)} movies info.')
    with open(RAW_TOP_RATED_MOVIES_INFO_PATH, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    print("✅ movies info saved!")


if __name__ == '__main__':
    movies = enrich_movies_with_credits()
    save_movies_data(movies)
