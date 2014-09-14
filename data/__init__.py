from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///:memory:', echo=False)
engine = create_engine('sqlite:///openspace.sqlite3', echo=False)

from data.base import Base
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)



