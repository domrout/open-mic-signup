import urwid, serial
from functools import partial
from data.performer import Performer
from data import Session

SERIAL_PORT = "/dev/ttyACM0"

class SignupPerformerUI(object):
    """Form to sign up a new performer for the first time"""
    def __init__(self, callback, manager):
        self.callback = callback
        self.title = "Sign Up"
        self.shortcuts = None
        self.ui()
        self.manager = manager

        #self.serial = serial.Serial(SERIAL_PORT)
        #self.serial.nonblocking()

        #self.manager.loop.watch_file(self.serial, 
        #                             self.handle_serial)

    def _target(self, session):
        """Get the performer object to save"""
        return Performer()

    def handle_serial(self):
        """Deal with a bit of input from the serial port"""
        with open("test.log", "a") as f:
            try:
                line = self.serial.readline().strip()
                if line.startswith(b"saw"):
                    card = line.lstrip(b"saw").strip()

                    self.nfc.set_edit_text(card)
            except serial.serialutil.SerialException:
                pass
            except OSError:
                pass
            

    def done(self, _):
        """Saves the current performer details"""
        session = Session() # Get a database session

        performer = self._target(session)
        performer.name   = self.name.get_edit_text()
        performer.email  = self.email.get_edit_text()
        performer.mobile = self.mobile.get_edit_text()
        performer.nfc = self.nfc.get_edit_text()

        session.add(performer)
        session.commit()
        self.callback(None, performer)


    def ui(self, performer = None):
        """Create the interface for the form"""  
        self.done_button = urwid.Button("Done")
        urwid.connect_signal(self.done_button, 'click', self.done)

        # Create basic display fields
        if performer:
            self.name = urwid.Edit("Name: ", performer.name)
            self.email = urwid.Edit("Email: ", performer.email)
            self.mobile = urwid.Edit("Mobile: ", performer.mobile)
            self.nfc = urwid.Edit("NFC: ", performer.nfc)

        else:
            self.name = urwid.Edit("Name: ")
            self.email = urwid.Edit("Email: ")
            self.mobile = urwid.Edit("Mobile: ")
            self.nfc = urwid.Edit("NFC UID: ")

        listwalker = urwid.SimpleFocusListWalker([
            self.name,
            self.email,
            self.mobile,
            #self.nfc,
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

