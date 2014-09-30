import urwid
from functools import partial
import data.performer as performer
from data.performer import Performer
from ui_helpers import *
from signup_performer_ui import SignupPerformerUI
from page_manager import *
from data import Session

class SuggestionListUI(object):
    """Shows a list of suggested performers and allows selection amongst them"""
    def __init__(self, callback, parent):
        self.listwalker = urwid.SimpleFocusListWalker([])

        self.widget = urwid.ListBox(self.listwalker)
        self.widget.keypress = self.listen(self.widget.keypress)

        self.callback = callback
        self.parent = parent
        self.suggestions = []

    def update(self, suggestions = []):
        """Just completely replace everything in the listwalker to reflect 
            current state. It's just the easiest way."""
        del self.listwalker[:] # Remove everything
        # Create again
        for index, performer in enumerate(suggestions):
            self.listwalker.append(self._row(performer))

        self.suggestions = suggestions

    def _row(self, performer):
        """Create a row for that button which can be selected."""
        button = urwid.Button(performer.name)
        urwid.connect_signal(button, "click", self.callback, performer)
        return button

    def focus_changed(self):
        """List selection changed, update display"""
        focus = self.listwalker.get_focus()[1]
        if focus != None:
            if focus >= 0 and focus < len(self.suggestions):
                selection = self.suggestions[focus]
                self.parent.update_attrs(selection)

    def listen(self, parent):
        def keypress(size, key):
            """Listen for up and down keys and send event for change of focus"""
            if key in ("up", "down"):
                response = parent(size, key)
                self.focus_changed()             
                return response
            return parent(size, key)
        return keypress

class SuggestionUI(object):
    def __init__(self, callback, manager):
        self.callback = callback
        self.performer = None
        self.title = "Select Performer"
        self.shortcuts = None
        self.manager = manager
        self.ui()

    def update(self, _, text):
        """Gets the current list of suggestions and feeds to the suggestion list"""
        session = Session() # Get a database session
        # DO A QUERY
        suggestions = session.query(Performer).filter(Performer.name.like("%"+text+"%")).all()
        # Show all suggested performers
        self.suggestion_list.update(suggestions)

        # Select the first suggestion
        if len(suggestions):
            self.update_attrs(suggestions[0]) 

    def update_attrs(self, performer):
        """Shows the current performer attributes"""
        self.name.set_text("Name: "+ performer.name)
        self.email.set_text("Email: "+ performer.email)
        self.mobile.set_text("Mobile: "+ performer.mobile)

    def sign_up(self, _):
        """Begin the sign up process"""
        signup = SignupPerformerUI(self.manager.pop_callback(self.callback), 
            self.manager)
        self.manager.push(signup)

    def ui(self):
        """Create the interface for the form"""
        self.suggestion_list = SuggestionListUI(self.callback, self)
        
        self.query = urwid.Edit("Search: ")

        urwid.connect_signal(self.query, 'change', self.update)

        self.sign_up_button = urwid.Button("Sign up new performer")
        urwid.connect_signal(self.sign_up_button, 'click', self.sign_up)

        # Create basic display fields
        self.name = urwid.Text(  "Name: -------------")
        self.email = urwid.Text( "Email: ------------")
        self.mobile = urwid.Text("Mobile: -----------")

        self.divider = urwid.Text("\n"+("="*40)+"\n")
        # Create a backup "simple mode"
        self.free_add = urwid.Edit("Just this once: ")
        self.free_add.keypress = self.listen_free_add(self.free_add.keypress)

        listwalker = urwid.SimpleFocusListWalker([
            self.sign_up_button,
            self.query,
            urwid.BoxAdapter(self.suggestion_list.widget, 5),
            self.name,
            self.email,
            self.mobile,
            self.divider,
            self.free_add
            ])

        widget_list = urwid.ListBox(listwalker)
        self.widget = urwid.Padding(widget_list, "center", ("relative", 50))

    def listen_free_add(self, parent):
        def keypress(size, key):
            """Listen for return a"""
            if key in ("return", "enter"):
                performer = Performer(name=self.free_add.get_edit_text())
                self.callback(performer)
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
    ui = SuggestionUI(exit, manager)

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