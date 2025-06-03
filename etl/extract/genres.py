import requests
from etl.utils import load_json, save_json
from etl.extract.consts import TMDB_BASE_API_URL_V3, TMDB_API_KEY, TMDB_GENRES_LIST_API_PATH, RAW_GENRES_DATA_PATH


def fetch_genres_from_api():
    print('⏳ Fetching genres from TMDb API...')
    API_URL = f'{TMDB_BASE_API_URL_V3}{TMDB_GENRES_LIST_API_PATH}'
    response = requests.get(API_URL, params={
        'api_key': TMDB_API_KEY,
        'language': 'en-US'
    })
    response.raise_for_status()
    data = response.json().get('genres', [])
    return data


def load_or_fetch_genres():
    try:
        data = load_json(RAW_GENRES_DATA_PATH)
        print('✅ Data Exist!')
        return data
    except FileNotFoundError as error:
        print(f'⚠️  Error reading existing file: {error}')
        data = fetch_genres_from_api()
        save_json(data, RAW_GENRES_DATA_PATH)
        print(f'✅ Saved {len(data)} genres to {RAW_GENRES_DATA_PATH}')
        return data


if __name__ == '__main__':
    genres = load_or_fetch_genres()
    print(f'\n✅ Loaded {len(genres)} genres:\n{genres[:3]}\n')
