import urwid
from functools import partial
import data.performer as performer
from data.performer import Performer
from confirm_ui import ConfirmUI
from signup_performer_ui import SignupPerformerUI, EditPerformerUI
from ui_helpers import *
from page_manager import *

from data import Session

class PerformersUI(object):
    """Shows a list of registered performers to allow management of them"""
    def __init__(self, callback, manager):
        self.listwalker = urwid.SimpleFocusListWalker([])

        self.widget = urwid.ListBox(self.listwalker)

        # Store the context
        self.manager = manager
        self.callback = callback

        self.title = "Performers"
        self.shortcuts = urwid.Columns([urwid.Text("a - Add"), 
            urwid.Text("d - delete"), 
            urwid.Text("e - edit")])

        # Load the performers from the database
        self.session = Session()
        self.load()

        # Watch for events
        self.widget.keypress = self.listen(self.widget.keypress )

    def load(self, _ = None):
        """Load performers from the database"""
        # DO A QUERY
        self.session = Session()
        self.performers = self.session.query(Performer).all()
        self.update()

    def update(self):
        """Just completely replace everything in the listwalker to reflect 
            current state. It's just the easiest way."""
        del self.listwalker[:] # Remove everything
        # Create again
        for index, performer in enumerate(self.performers):
            self.listwalker.append(self._row(performer))

    def delete(self, selection):
        """Shows confirm dialog for removing user from database"""

        def _delete():
            """Removes the selected performer from the database"""
            self.session.delete(selection)
            self.session.commit()
            self.load()

        confirm_ui = ConfirmUI(self.manager.pop_callback(_delete), 
            self.manager.pop, 
            self.manager)
        self.manager.push(confirm_ui)

    def add(self):
        """Show the screen to create a new performer"""
        self.manager.push(SignupPerformerUI(self.manager.pop_callback(self.load), 
                self.manager))

    def edit(self, _, performer):
        """Show the edit screen for the given performer"""
        self.manager.push(EditPerformerUI(performer, 
                self.manager.pop_callback(self.load), 
                self.manager))

    def _row(self, performer):
        """Create a row for that button which can be selected."""
        button = urwid.Button(performer.name)
        urwid.connect_signal(button, "click", self.edit, performer)
        return button

    def listen(self, parent):
        def keypress(size, key):
            """Listen for keys and send event for deletion, addition etc"""
            selected = None
            if len(self.performers):
                selected = self.performers[self.listwalker.get_focus()[1]]

            if key == 'd' and selected:
                self.delete(selected)             
            elif key == 'a':
                self.add()
            elif key == 'e' and selected:
                self.edit(None, selected)
            else:
                return parent(size, key)
        return keypress

if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine('sqlite:///:memory:', echo=False)
    Session.configure(bind=engine) 
    performer.Base.metadata.create_all(engine)

    # Do an actual write.
    session = Session()
    # Add some test data 
    dom = Performer(name="Dominic Rout", email="", mobile = "213123123")
    al_g = Performer(name="Al G", email="alg@example.com", mobile = "1234123412312")
    al_p = Performer(name="Al P", email="alp@example.com", mobile = "12341231123412312")

    session.add(dom)
    session.add(al_g)
    session.add(al_p)

    session.commit()

    def exit():
        raise urwid.ExitMainLoop()
    manager = PageManager()
    ui = PerformersUI(exit, manager)

    manager.push(ui)

    manager.run()

# def select_performer():
#         heading = urwid.BigText("Add Performer", urwid.font.HalfBlock5x4Font())
#         heading = urwid.Padding(heading, 'center', width="clip")
#         heading = urwid.Filler(heading, 'top')
#         heading = urwid.BoxAdapter(heading, 5)

#         suggestion_listwalker = urwid.SimpleFocusListWalker([
#             urwid.Button("Dominic"),
#             urwid.Button("Rout")
#             ])

#         def update_suggestions(edit, text):
#             performers = [p for p in all_performers if text in p[0]]
#             del suggestion_listwalker[:]
#             for performer in performers:
#                 suggestion_listwalker.append(urwid.Button(performer))

#         suggestion_list = urwid.ListBox(suggestion_listwalker)
#         name_edit = urwid.Edit("Name ")
#         email_edit = urwid.Edit("Email ")
#         listwalker = urwid.SimpleFocusListWalker([
#             name_edit,
#             urwid.BoxAdapter(suggestion_list, 5),
#             email_edit
#             ])
#         form_list = urwid.ListBox(listwalker)

#         urwid.connect_signal(name_edit, 'change', update_suggestions)

#         frame = urwid.Frame(header = heading, 
#             body=urwid.Padding(form_list, "center", ("relative", 50)))
#         loop = urwid.MainLoop(frame, unhandled_input=exit)
#         loop.run()

