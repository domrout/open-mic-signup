from sqlalchemy import Column, Integer, String, Table, ForeignKey


from sqlalchemy.orm import relationship

from data.base import Base

from datetime import datetime as dt
import datetime

class PerformanceStart(Base):
    __tablename__ = "performance_starts"
    id = Column(Integer, primary_key = True)
    performance_id = Column(Integer, ForeignKey('performances.pid'))
    time = Column('time', String)
    
class PerformanceEnd(Base):
    __tablename__ = "performance_ends"
    id = Column(Integer, primary_key = True)
    performance_id = Column(Integer, ForeignKey('performances.pid'))
    time = Column('time', String)



class Performance(Base):
    __tablename__ = "performances"

    pid = Column(Integer, primary_key=True)
    performer = Column(Integer, ForeignKey("performers.id"))
    setlist_id = Column(Integer, ForeignKey('setlists.id'))

    starts = relationship(PerformanceStart, backref="performance")
    ends = relationship(PerformanceEnd, backref="performance")
  

    # def __init__(self, pid, performer, setlist):
    #     self.pid = pid
    #     self.setlist = setlist
    #     self.performer = performer
    #     self.starts = [dt.now()]
    #     self.ends = [dt.now()]

    def running(self):
        return len(self.starts) != len(self.ends)

    def total_time(self):
        starts = self.starts
        if len(self.starts) > len(self.ends):
            ends = self.ends + [PerformanceEnd(time=dt.now())]
        else:
            ends = self.ends

        return sum([end.time-start.time for start, end in zip(starts, ends)], datetime.timedelta())

    def toggle(self):
        if self.running():
            self.stop()
        else:
            self.start()

    def start(self):
        if not self.running():
            time = PerformanceStart(time = dt.now())
            self.starts.append(time)

    def stop(self):
        if self.running():
            time = PerformanceEnd(time = dt.now())
            self.ends.append(time)

    def __str__(self):
        status = ""
        if self.running():
            status = "(Now Playing)"
        seconds = int(self.total_time().total_seconds())

        if seconds > 0:
            return "%s: %s seconds %s" % (self.performer.name, 
                seconds, 
                status)
        else:
            return "%s %s" % (self.performer.name, 
                status)

if __name__ == "__main__":
    from data import Session
    # Do an actual write.
    session = Session()

    dom = Performer(name="Dominic Rout", email="dom.rout@gmail.com", mobile = "07427549166")
    al_g = Performer(name="Al Gordon", email="alg@example.com", mobile = "1234123412312")
    al_p = Performer(name="Al Pearson", email="alp@example.com", mobile = "12341231123412312")

    session.add(dom)
    session.add(al_g)
    session.add(al_p)

    found_al = session.query(Performer).filter(Performer.name.like("%Al%")).first() 
    print(found_al)