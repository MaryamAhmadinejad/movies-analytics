import time
import json
import requests
from bs4 import BeautifulSoup


def convert_runtime_to_minutes(runtime_str):
    try:
        time_object = time.strptime(runtime_str, '%Hh %MM')
    except:
        try:
            time_object = time.strptime(runtime_str, '%Hh')
        except:
            time_object = time.strptime(runtime_str, '%MM')
    hours = int(time_object.tm_hour)
    minutes = int(time_object.tm_min)
    total_minutes = hours*60 + minutes
    return total_minutes


base_url = 'https://www.imdb.com'
url = f'{base_url}/chart/top'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.5'}


def crawl_movie_detail_page(movie_href, movie_rank):
    movie_url = f'{base_url}{movie_href}'
    movie_id = movie_href.rsplit('/')[2].replace('tt','')
    response = requests.get(movie_url, headers=headers)
    content = BeautifulSoup(response.text, 'html.parser')
    title = (content.select_one('h1 > span').text.encode('ascii', 'ignore')).decode("utf-8")
    lis = content.select('div.sc-52d569c6-0 ul.ipc-inline-list.baseAlt > li')
    year = int(lis[0].text)
    runtime = convert_runtime_to_minutes(lis[-1].text)
    raw_parental_guide = lis[1].text if len(lis) == 3 else 'Unrated'
    parental_guide = 'Unrated' if raw_parental_guide == 'Not Rated' else raw_parental_guide
    gross_us_canada_li = content.select_one('li[data-testid="title-boxoffice-grossdomestic"] > div li')
    gross_us_canada = int(gross_us_canada_li.text.replace(',', '').replace('$', '')) if gross_us_canada_li else None
    movie_info = {
        'id': movie_id,
        'rank': movie_rank,
        'title': title,
        'year': year,
        'runtime': runtime,
        'parental_guide': parental_guide,
        'gross_us_canada': gross_us_canada,
    }
    movies.append(movie_info)
    ##
    genres = content.select('.ipc-chip-list--baseAlt.ipc-chip-list > .ipc-chip-list__scroller > a')
    for genre in genres:
        genre_info = {
            'movie_id': movie_id,
            'genre': genre.text,
        }
        genre_movies.append(genre_info)
    ##
    metadata = content.select('ul.ipc-metadata-list.ipc-metadata-list--dividers-all.title-pc-list.ipc-metadata-list--baseAlt > li')
    directors = metadata[0].select('a.ipc-metadata-list-item__list-content-item')
    for director in directors:
        person_id = director.get("href").rsplit('/')[2].replace('nm', '')
        director_name = (director.text.encode('ascii', 'ignore')).decode("utf-8")
        person_info = {
            'person_id': person_id,
            'name': director_name,
        }
        people.append(person_info)
        crew_info = {
            'movie_id': movie_id,
            'person_id': person_id,
            'role': 'Director',
        }
        crews.append(crew_info)
    writers = metadata[1].select('a.ipc-metadata-list-item__list-content-item')
    for writer in writers:
        person_id = writer.get("href").rsplit('/')[2].replace('nm', '')
        writer_name = (writer.text.encode('ascii', 'ignore')).decode("utf-8")
        person_info = {
            'person_id': person_id,
            'name': writer_name,
        }
        people.append(person_info)
        crew_info = {
            'movie_id': movie_id,
            'person_id': person_id,
            'role': 'Writer',
        }
        crews.append(crew_info)
    stars = metadata[2].select('a.ipc-metadata-list-item__list-content-item')
    for star in stars:
        person_id = star.get("href").rsplit('/')[2].replace('nm','')
        star_name = (star.text.encode('ascii', 'ignore')).decode("utf-8")
        person_info = {
            'person_id': person_id,
            'name': star_name,
        }
        people.append(person_info)
        cast_info = {
            'movie_id': movie_id,
            'person_id': person_id,
        }
        casts.append(cast_info)


# MOVIES LIST PAGE
response = requests.get(url, headers=headers)
content = BeautifulSoup(response.text, 'html.parser')
movies_selectors = content.select('tbody.lister-list > tr')
movies = []
genre_movies = []
people = []
crews = []
casts = []

rank = 0
for movie in movies_selectors:
    rank += 1
    movie_href = movie.select_one('td.titleColumn > a').get("href")
    crawl_movie_detail_page(movie_href, rank)


with open("movies.json", "w") as json_movies_file:
    json.dump(movies, json_movies_file, indent=4)

with open("genres.json", "w") as json_genres_file:
    json.dump(genre_movies, json_genres_file, indent=4)

with open("people.json", "w") as json_people_file:
    json.dump(people, json_people_file, indent=4)

with open("crews.json", "w") as json_crews_file:
    json.dump(crews, json_crews_file, indent=4)

with open("casts.json", "w") as json_casts_file:
    json.dump(casts, json_casts_file, indent=4)
