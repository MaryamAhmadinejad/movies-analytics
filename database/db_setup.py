from database.session import engine
from database.models import Base


def init_db():
    Base.metadata.create_all(engine)
    print('✅ Database and tables created!')


if __name__ == '__main__':
    init_db()
