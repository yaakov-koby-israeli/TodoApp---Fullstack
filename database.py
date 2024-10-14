import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base #create db object 4 interaction

# IF USING SQLITE3
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# IF USING POSTGRESQL
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost/TodoAplicationDatabase'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# IF USING MYSQL
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:12345678@127.0.0.1:3306/TodoApplicationDatabase'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)# false 4 not allowing db perform auto actions

Base = sqlalchemy.orm.declarative_base()