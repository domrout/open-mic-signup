#!/usr/bin/python

import urwid, sqlite3, datetime
from datetime import datetime as dt
from functools import partial
from data.setlist import SetList
from performers_ui import PerformersUI
from ui_helpers import *
import data.performer
import suggestion_ui
import signup_performer_ui
from page_manager import PageManager


class SetListMenuUI(object):
    """User interface to display and rearrange a performance list for the open mic"""
    def __init__(self, setlist, manager):
        """Initialise the UI"""
        self.listwalker = urwid.SimpleFocusListWalker([])
        self.setlist = setlist
        self.grabbed_index = None
        self.manager = manager
        self.title = "Open Space"

        # Store shortcuts which can be used in the chrome to make life easier.
        self.shortcuts = urwid.Columns([urwid.Text("a - Add"), 
            urwid.Text("n - Next"), 
            urwid.Text("s - Start"),
            urwid.Text("p - Pause"),
            urwid.Text("m - Members"),
            urwid.Text("enter - Move")])

        # Create the needed widget
        self.widget = urwid.ListBox(self.listwalker)
        self.widget.keypress = self.listen(self.widget.keypress)


    def _performance_row(self, performance):   
        """Create a row for display of a performance. 

            A call to grab with the specific performance is used as the callback"""
        button = MenuButton(str(performance), partial(self.grab, performance))
        return urwid.AttrMap(button, None, focus_map='reversed')

    def update_loop(self, main_loop, _= None):
        """Repeatedly update so that times stay correct"""
        self.update()
        main_loop.set_alarm_in(1, self.update_loop)

    def update(self):
        """Just completely replace everything in the listwalker to reflect 
            current state. It's just the easiest way."""
        _, focus = self.listwalker.get_focus()

        del self.listwalker[:] # Remove everything
        # Create again
        for index, performance in enumerate(self.setlist):
            self.listwalker.append(self._performance_row(performance))

        if focus != None:
            self.listwalker.set_focus(focus) # Restore correct selection

    def start(self):
        """Starts the currently selected performance"""
        _, selected_index = self.listwalker.get_focus()

        self.setlist.start_at(selected_index)
        self.update()

    def stop(self):
        """Ends all performances"""
        self.setlist.stop()
        self.update()

    def delete(self):
        """Removes the currently selected performance from the list"""
        if len(self.setlist):
            _, focus = self.listwalker.get_focus()

            del self.listwalker[focus] # Remove everything
            del self.setlist[focus]

    def grab(self, performance, _):
        """Grabs the specified performance"""        
        self.grabbed_index = self.setlist.index(performance)

    def nudge(self, offset):
        """Nudges item at grabbed_index by offset if possible"""
        index = self.grabbed_index + offset

        if index >= 0 and index < len(self.setlist):
            performance = self.setlist[self.grabbed_index]

            # Delete old index
            del self.setlist[self.grabbed_index]

            # Update the index and reinsert
            self.grabbed_index = index
            self.setlist.insert(index, performance)

            # Fix focus
            self.listwalker.set_focus(index)
            self.update()

    def signup(self, performer):
        """Signs up a new performer to the list and updates"""
        self.setlist.signup(performer)
        self.update()

    def listen(self, parent):
        def keypress(size, key):
            """Hijack keys to support required actions"""
            if self.grabbed_index != None:
                # Grab the current performer and start moving them about.
                if key == "up":
                    self.nudge(-1)
                    return None
                elif key == "down":
                    self.nudge(1)
                    return None
                elif key == "enter":
                    self.grabbed_index = None
                    return None

            elif key in ('s'):
                # Get current selection playing
                self.start()
                return None
            elif key in ('p'):
                # Pause current performance.
                self.stop()
                return None
            elif key in ('d', 'backspace', 'delete'):
                # Pause current performance.
                self.delete()
                return None
            elif key in ('m', 'M'):
                # Show member's list
                self.manager.push(
                    PerformersUI(self.manager.pop, 
                    self.manager)) 
                return None
            elif key in ("n"):
                # Move to next performer in the list
                next_performer = self.setlist.next()
                self.setlist.start(next_performer)
                self.update()
                return None
            elif key in ("a"):
                # Add a new performer
                ui = suggestion_ui.SuggestionUI(self.manager.pop_callback(self.signup), 
                    self.manager)
                self.manager.push(ui)
            else:
                return parent(size, key)

        return keypress

if __name__ == "__main__":
    # Create some example performers
    setlist = SetList()

    for performer in [data.performer.Performer(name="Dominic Rout", email="", mobile = "213123123"),
        data.performer.Performer(name="Al G", email="alg@example.com", mobile = "1234123412312"),
        data.performer.Performer(name="Al P", email="alp@example.com", mobile = "12341231123412312")]:
        setlist.signup(performer)

    manager = PageManager()
    ui = SetListMenuUI(setlist, manager)
    manager.push(ui)
    ui.update_loop(manager.loop) 
    manager.run()
