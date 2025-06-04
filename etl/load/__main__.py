from etl.load.insert_genres_data import load_to_sqlite as load_genres_data
from etl.load.insert_people_data import load_to_sqlite as load_people_data
from etl.load.insert_movies_data import load_to_sqlite as load_movies_data


load_genres_data()
load_people_data()
load_movies_data()
