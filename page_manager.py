import urwid

class PageManager(object):
    """Contains the main loop object and frames for Open Space application."""
    def __init__(self):
        self.frame = None
        self.loop = None

    def show_ui(self, ui):
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
            self.loop = urwid.MainLoop(self.frame)
        else:
            self.loop.widget = self.frame
    def run(self):
        self.loop.run()