import requests
import time
from etl.utils import save_json
from etl.extract.consts import TMDB_BASE_API_URL_V3, TMDB_API_KEY, TMDB_TOP_RATED_MOVIES_LIST_API_PATH, RAW_TOP_RATED_MOVIES_LIST_DATA_PATH


def get_top_rated_movies(pages: int) -> list[dict]:
    movies = []
    for page in range(1, pages + 1):
        print(f'Fetching page {page}...')
        url = f'{TMDB_BASE_API_URL_V3}{TMDB_TOP_RATED_MOVIES_LIST_API_PATH}'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US',
            'page': page
        }
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        movies.extend(data.get('results', []))
        time.sleep(0.25)
    return movies


if __name__ == '__main__':
    top_movies = get_top_rated_movies(pages=13)
    save_json(top_movies, RAW_TOP_RATED_MOVIES_LIST_DATA_PATH)
