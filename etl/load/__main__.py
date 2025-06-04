from etl.load.insert_movies_data import load_genres_to_db, load_movies_to_db
from etl.load.insert_credits_data import load_people_to_db, load_casts_and_crews_to_db


load_genres_to_db()
load_movies_to_db()
load_people_to_db()
load_casts_and_crews_to_db()
