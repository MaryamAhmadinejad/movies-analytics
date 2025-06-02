import json
import requests
from consts import TMDB_BASE_API_URL, TMDB_API_KEY, TMDB_GENRES_LIST_API_PATH_V3, RAW_GENRES_DATA_PATH


def fetch_genres_from_api():
    print("⏳ Fetching genres from TMDb API...")
    API_URL = f'{TMDB_BASE_API_URL}{TMDB_GENRES_LIST_API_PATH_V3}'
    response = requests.get(API_URL, params={
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    })
    response.raise_for_status()
    data = response.json().get("genres", [])
    # save data
    with open(RAW_GENRES_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, separators=(", ", ": "))
    print(f"✅ Saved {len(data)} genres to {RAW_GENRES_DATA_PATH}")
    return data


def load_or_fetch_genres():
    try:
        with open("data/raw/genres_list.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        print('✅ Data Exist!')
        return data
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"⚠️  Error reading existing file: {error}")
        data = fetch_genres_from_api()
        return data


if __name__ == "__main__":
    genres = load_or_fetch_genres()
    print(f"\n✅ Loaded {len(genres)} genres:\n{genres[:3]}\n")
