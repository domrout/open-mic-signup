import urwid

class PageManager(object):
    """Contains the main loop object and frames for Open Space application.

        UI objects are managed using a stack. 
    """
    def __init__(self):
        self.frame = None
        self.loop = None
        self.stack = []

    def push(self, ui):
        """Shows the given UI object on top of the others."""
        self.stack.append(ui)
        self._show_ui(ui)

    def pop(self, _ = None):
        """Shows the previous UI object"""
        self.stack.pop()

        # Show the previous page if there is one.
        if len(self.stack):
            ui = self.stack[-1]
            self._show_ui(ui)
        else:
            # Or exit if there's no previous page.
            raise urwid.ExitMainLoop()

    def pop_callback(self, callback, *args, **kwargs):
        """Wrap the given callback to:
            - Close the current UI when fired
            - Ignore first parameter (widget)
        """
        def _callback(*xargs, **xkwargs):
            self.pop()
            # Try with and without first paramater
            aargs = args + xargs
            akwargs = dict(kwargs.items())
            akwargs.update(xkwargs)

            try:
                callback(*aargs, **akwargs)
            except TypeError:
                callback(*aargs[1:], **akwargs)

        return _callback

    def _show_ui(self, ui):
        if ui.title != None:
            title = ui.title
        else:
            title = "Open Space"

        heading = urwid.BigText(title, urwid.font.HalfBlock5x4Font())
        heading = urwid.Padding(heading, 'center', width="clip")
        heading = urwid.Filler(heading, 'top')
        heading = urwid.BoxAdapter(heading, 5)

        self.frame = urwid.Frame(header = heading, body=ui.widget, footer = ui.shortcuts)
        # else:
        #     self.frame.contents["body"] = ui.widget
        #     self.frame.contents["heading"] = heading
        #     self.frame.contents["footer"] = ui.shortcuts

        if not self.loop:
            self.loop = urwid.MainLoop(self.frame, unhandled_input=self.handle_q)
        else:
            self.loop.widget = self.frame

    def handle_q(self, key):
        if key in ("q", "Q"):
            self.pop()

    def run(self):
        self.loop.run()