import urwid

class ConfirmUI(object):
    """Shows a list of registered performers to allow management of them"""
    def __init__(self, callback_yes, callback_no, manager):
        # Store the context
        self.manager = manager

        # Set the chrome
        self.title = "Really Delete?"
        self.shortcuts = None

        # Create the UI
        self.question = urwid.Text("Are you sure you want to delete?")
        self.yes = urwid.Button("Yes")
        self.no = urwid.Button("No")

        buttons = urwid.Columns([self.yes, self.no])
        self.widget = urwid.Padding(
            urwid.Filler(
                urwid.Pile([self.question, buttons])
            ), 
            "center", ("relative", 50)
        )

        # Plug in the events
        urwid.connect_signal(self.yes, "click", callback_yes)
        urwid.connect_signal(self.no, "click", callback_no)