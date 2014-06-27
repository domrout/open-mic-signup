from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, String
Base = declarative_base()

class Performer(Base):
    """Represents a talented musician or poet or comedy!"""
    __tablename__ = 'performers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    mobile = Column(String)

    def __repr__(self):
       return "<Performer(name='%s', email='%s', mobile='%s')>" % (
                            self.name, self.email, self.mobile)

    # def __init__(self, name, email, mobile):
    #   self.name = name
    #   self.email = email
    #   self.mobile = mobile
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///:memory:', echo=True)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    # Do an actual write.
    session = Session()

    dom = Performer(name="Dominic Rout", email="dom.rout@gmail.com", mobile = "07427549166")
    al_g = Performer(name="Al Gordon", email="alg@example.com", mobile = "1234123412312")
    al_p = Performer(name="Al Pearson", email="alp@example.com", mobile = "12341231123412312")

    session.add(dom)
    session.add(al_g)
    session.add(al_p)

    found_al = session.query(Performer).filter(Performer.name.like("%Al%")).first() 
    print found_al