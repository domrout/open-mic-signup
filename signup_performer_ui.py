import urwid
from functools import partial
from sqlalchemy.orm import sessionmaker
import data.performer as performer
from data.performer import Performer

Session = sessionmaker()

class SignupPerformerUI(object):
    """Form to sign up a new performer for the first time"""
    def __init__(self, callback, manager):
        self.callback = callback
        self.title = "Sign Up"
        self.shortcuts = None
        self.ui()
        self.manager = manager

    def done(self, _):
        """Gets the current list of suggestions and feeds to the suggestion list"""
        session = Session() # Get a database session
        performer = Performer(name=self.name.get_edit_text(),
            email=self.email.get_edit_text(), 
            mobile = self.mobile.get_edit_text())

        session.add(performer)
        session.commit()
        self.callback(performer)

    def ui(self, performer = None):
        """Create the interface for the form"""  
        self.done_button = urwid.Button(u"Done")
        urwid.connect_signal(self.done_button, 'click', self.done)

        # Create basic display fields
        if performer:
            self.name = urwid.Edit(u"Name: ", performer.name)
            self.email = urwid.Edit(u"Email: ", performer.email)
            self.mobile = urwid.Edit(u"Mobile: ", performer.mobile)
        else:
            self.name = urwid.Edit(u"Name: ")
            self.email = urwid.Edit(u"Email: ")
            self.mobile = urwid.Edit(u"Mobile: ")


        listwalker = urwid.SimpleFocusListWalker([
            self.name,
            self.email,
            self.mobile,
            self.done_button
            ])

        widget_list = urwid.ListBox(listwalker)
        self.widget = urwid.Padding(widget_list, "center", ("relative", 50))
