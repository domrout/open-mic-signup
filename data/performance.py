from datetime import datetime as dt
import datetime
class Performance(object):
    def __init__(self, pid, performer, setlist):
        self.pid = pid
        self.setlist = setlist
        self.performer = performer
        self.starts = [dt.now()]
        self.ends = [dt.now()]

    def running(self):
        return len(self.starts) != len(self.ends)

    def total_time(self):
        starts = self.starts
        if len(self.starts) > len(self.ends):
            ends = self.ends + [dt.now()]
        else:
            ends = self.ends
        return sum([end-start for start, end in zip(starts, ends)], datetime.timedelta())

    def toggle(self):
        if self.running():
            self.stop()
        else:
            self.start()

    def start(self):
        if not self.running():
            self.starts.append(dt.now())

    def stop(self):
        if self.running():
            self.ends.append(dt.now())

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
