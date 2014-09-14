import urwid
from functools import partial
from data.performer import Performer
from data import Session

class SignupPerformerUI(object):
    """Form to sign up a new performer for the first time"""
    def __init__(self, callback, manager):
        self.callback = callback
        self.title = "Sign Up"
        self.shortcuts = None
        self.ui()
        self.manager = manager

    def _target(self, session):
        """Get the performer object to save"""
        return Performer()

    def done(self, _):
        """Saves the current performer details"""
        session = Session() # Get a database session

        performer = self._target(session)
        performer.name   = self.name.get_edit_text()
        performer.email  = self.email.get_edit_text()
        performer.mobile = self.mobile.get_edit_text()

        session.add(performer)
        session.commit()
        self.callback(None, performer)


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

        self.widget.keypress = self.listen_tab(self.widget.keypress)

    def listen_tab(self, parent):
        def keypress(size, key):
            if key == "tab":
                key = "down"
            return parent(size, key)
        return keypress


class EditPerformerUI(SignupPerformerUI):
    """Edits the attributes on an existing performer"""
    def __init__(self, performer, callback, manager):
        self.callback = callback
        self.title = "Edit Performer"
        self.shortcuts = None
        self.performer = performer
        self.ui(performer)
        self.manager = manager

    def _target(self, session):
        """Get the selected performer using the current session"""
        return session.query(Performer) \
            .filter(Performer.id == self.performer.id).first()

