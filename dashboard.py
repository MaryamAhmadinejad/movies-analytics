import pandas as pd
import streamlit as st
from sqlalchemy import URL, create_engine, select, text


MYSQL_DRIVER = "mysql+mysqlconnector"
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "XXXXXXXXXXX"
MYSQL_HOST_NAME = "localhost"
MYSQL_PORT = 3306
DB_NAME = "imdb"

url_object = URL.create(
    MYSQL_DRIVER,
    username=MYSQL_USERNAME,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST_NAME,
    port=MYSQL_PORT,
    database=DB_NAME,
)

engine = create_engine(url_object)


#############################################################################################################
with engine.connect() as conn:
    result = conn.execute(text(f"SELECT DISTINCT genre FROM genre_movie;"))
genres_list = pd.DataFrame(result.all())

with engine.connect() as conn:
    result = conn.execute(text(f"SELECT DISTINCT name FROM cast INNER JOIN person ON cast.person_id = person.id;"))
casts_list = pd.DataFrame(result.all())


#############################################################################################################
#############################################################################################################
#############################################################################################################
st.title("part1")
st.header("section1")

min_year = 1000
max_year = 2024

start_year = st.selectbox(
    label = "start year",
    options = [x for x in range(min_year, max_year)],
)
end_year = st.selectbox(
    label = "end year",
    options = [x for x in reversed(range(min_year, max_year))],
)

with engine.connect() as conn:
    result = conn.execute(text(f"SELECT * FROM movie WHERE year BETWEEN {start_year} AND {end_year};"))
df = pd.DataFrame(result.all(), columns=result.keys())

st.dataframe(df)


#############################################################################################################
#############################################################################################################
#############################################################################################################
st.title("part1")
st.header("section2")

min_runtime = 45
max_runtime = 239

start_runtime = st.selectbox(
    label = "start runtime",
    options = [x for x in range(min_runtime, max_runtime)],
)
end_runtime = st.selectbox(
    label = "end runtime",
    options = [x for x in reversed(range(min_runtime, max_runtime))],
)

with engine.connect() as conn:
    result = conn.execute(text(f"SELECT * FROM movie WHERE runtime BETWEEN {start_runtime} AND {end_runtime};"))
df = pd.DataFrame(result.all(), columns=result.keys())

st.dataframe(df)

#############################################################################################################
#############################################################################################################
#############################################################################################################
st.title("part1")
st.header("section4")

genre_name_movies = st.selectbox(
    label = "genre1",
    options = genres_list,
)

with engine.connect() as conn:
    result = conn.execute(text(f"SELECT movie.id, movie.title, movie.year, movie.runtime, movie.parental_guide, movie.gross_us_canada FROM genre_movie INNER JOIN movie ON movie.id = genre_movie.movie_id WHERE genre = '{genre_name_movies}';"))

df = pd.DataFrame(result.all(), columns=result.keys())
st.dataframe(df)

#############################################################################################################
#############################################################################################################
#############################################################################################################
st.title("part2")
st.header("section1")

with engine.connect() as conn:
    result = conn.execute(text(f"SELECT title, gross_us_canada FROM movie ORDER BY movie.gross_us_canada DESC LIMIT 10;"))

chart_data = pd.DataFrame(result.all()).set_index('title')
st.bar_chart(chart_data)


#############################################################################################################
#############################################################################################################
#############################################################################################################
st.title("part2")
st.header("section2")

with engine.connect() as conn:
    result = conn.execute(text(f"SELECT name, COUNT(movie_id) AS number_of_movies FROM cast INNER JOIN person ON cast.person_id = person.id GROUP BY name ORDER BY number_of_movies DESC, name LIMIT 5;"))

casts_data = pd.DataFrame(result.all()).set_index('name')
st.bar_chart(casts_data)

#############################################################################################################
#############################################################################################################
#############################################################################################################
st.title("part3")


genre_name_gross = st.selectbox(
    label = "genre",
    options = genres_list,
)

with engine.connect() as conn:
    result = conn.execute(text(f"SELECT title, gross_us_canada FROM genre_movie INNER JOIN movie ON movie.id = genre_movie.movie_id WHERE genre_movie.genre = '{genre_name_gross}' LIMIT 10;"))
df = pd.DataFrame(result.all()).set_index('title')

st.bar_chart(df)

