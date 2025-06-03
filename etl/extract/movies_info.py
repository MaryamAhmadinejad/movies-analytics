import requests
from etl.utils import load_json, save_json
from etl.extract.consts import TMDB_BASE_API_URL_V3, TMDB_API_KEY, RAW_TOP_RATED_MOVIES_LIST_DATA_PATH, RAW_TOP_RATED_MOVIES_INFO_PATH


def fetch_movie_info(movie_id: int, movie_name: str) -> dict:
    print(f'🎬 Fetching info for movie ID {movie_id}: {movie_name}...')
    url = f'{TMDB_BASE_API_URL_V3}/movie/{movie_id}'
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"❌ Failed to fetch info for {movie_name} ({movie_id}): {e}")
        return {}


def enrich_movies_total_info() -> list:
    top_movies = load_json(RAW_TOP_RATED_MOVIES_LIST_DATA_PATH)
    movies_info = []
    for top_movie in top_movies:
        movie_id = top_movie['id']
        movie_name = top_movie['title']
        info = fetch_movie_info(movie_id, movie_name)
        movies_info.append(info)
    return movies_info


if __name__ == '__main__':
    movies = enrich_movies_total_info()
    save_json(movies, RAW_TOP_RATED_MOVIES_INFO_PATH)
