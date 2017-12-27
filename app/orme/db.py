import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

DATABASE_CONNSTRING = "postgresql://%s:%s@%s/%s" % (os.environ["DATABASE_USER"],
                                                    os.environ["DATABASE_PASSWORD"],
                                                    os.environ["DATABASE_HOST"],
                                                    os.environ["DATABASE_NAME"],
                                                    )
engine = create_engine(DATABASE_CONNSTRING, isolation_level="READ UNCOMMITTED")
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
