from sqlalchemy import create_engine
from models import Base


DB_PATH = 'sqlite:///database/imdb.db'


def init_db(db_path=DB_PATH):
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    print('✅ Database and tables created!')


if __name__ == '__main__':
    init_db()
