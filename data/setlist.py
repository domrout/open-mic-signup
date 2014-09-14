from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from data.base import Base

from datetime import datetime as dt
from data.performance import Performance


class SetList(Base):
    __tablename__ = 'setlists'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    performances = relationship(Performance, backref="setlist")

    def __init__(self, date=dt.today()):

        super(SetList, self).__init__()


        self.date = date
        self.last_performance = None # No-one playing just now.

    def start(self, performance):
        """Calls start() on the selected performance and stops all others"""
        self.last_performance = None
        for index, _performance in enumerate(self.performances):
            if _performance == performance:
                _performance.start()
                self.last_performance = _performance
            else:
                _performance.stop()

    def start_at(self, index):
        """Calls start() on the performance at selected index and stop all others"""
        self.last_performance = None
        for _index, performance in enumerate(self.performances):
            if _index == index:
                performance.start()
                self.last_performance = performance
            else:
                performance.stop()

    def stop(self):
        """Ends all performances"""
        for _performance in self.performances:
            _performance.stop()

    def next(self):
        """Returns the next performance in the list or None if we're at the end"""
        if self.last_performance == None:
            return self[0] # No previous performance. Go for the first one.

        index = self.performances.index(self.last_performance)
        if index + 1 < len(self.performances):
            return self.performances[index + 1]
        else:
            return None

    def signup(self, performer):
        """Creates a new performance object for the given performer and adds to end of list"""
        # # Generate an ID for the current performance
        # try:
        #     performer_id = max(p.pid for p in self) + 1
        # except ValueError: # empty list
        #     performer_id = 0

        # Create the performance object
        performance = Performance(performer = performer, setlist = self)
        # self.performances.append(performance) # Add to list

        return performance

    def find_by_pid(self, pid):
        """Search for the given performance ID and return the Performance and index
        @return: (index, Performance)"""
        # Linear search for index. lists are small so doesn't matter.
        index = [p.pid for p in self].index(pid)
        return index, self[index]

