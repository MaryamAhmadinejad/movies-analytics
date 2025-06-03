import requests
from etl.utils import load_json, save_json
from etl.extract.consts import TMDB_BASE_API_URL_V3, TMDB_API_KEY, RAW_TOP_RATED_MOVIES_LIST_DATA_PATH, RAW_TOP_RATED_MOVIES_CREDITS_PATH


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
    top_movies = load_json(RAW_TOP_RATED_MOVIES_LIST_DATA_PATH)
    movies_credits = []
    for top_movie in top_movies:
        movie_id = top_movie['id']
        movie_name = top_movie['title']
        credits = fetch_movie_credits(movie_id, movie_name)
        movie_credits = {
            "movie_id": top_movie['id'],
            "movie_title": top_movie['title'],
            "cast": credits['cast'],
            "crew": credits['crew']
        }
        movies_credits.append(movie_credits)
    return movies_credits


if __name__ == '__main__':
    movies = enrich_movies_with_credits()
    save_json(movies, RAW_TOP_RATED_MOVIES_CREDITS_PATH)
