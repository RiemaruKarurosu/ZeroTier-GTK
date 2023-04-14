# main.py
#
# Copyright 2023 Rivack Mares
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi
import libzt

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import ZerotierGtkWindow

class AdwActionRowsManager:
    def __init__(self):
        self.action_rows = []

    def create_action_row(self, title, subtitle):
        action_row = Adw.ActionRow()
        action_row.props.title = title
        action_row.props.subtitle = subtitle
        self.action_rows.append(action_row)
        return action_row

    def get_action_rows(self):
        return self.action_rows


class ZerotierGtkApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='org.gnome.zerotiergtk',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)

        self.action_rows_manager = AdwActionRowsManager()


        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

    def on_start_Zerotier(self):
        node = libzt.ZeroTierNode()
        node.node_start()
        print(node.get_id())

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = ZerotierGtkWindow(application=self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='zerotier-gtk',
                                application_icon='org.gnome.zerotiergtk',
                                developer_name='Zerotier-GTK',
                                version='0.1.1-alpha',
                                developers=['Tomás Ralph'],
                                copyright='© 2023 Zerotier-GUI',
                                issue_url='https://github.com/RiemaruKarurosu/ZeroTier-GUI')
        about.present()


    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')
        #preferences = Adw

    def create_action_rows(self, window):
        """Create the action rows and add them to the window."""
        # Get the AdwPreferencesGroup from the window
        preferences_group = window.get_preferences()

        # Create and add an AdwActionRow for each item in the list
        items = ['item1', 'item2', 'item3']  # replace with your list of items
        for item in items:
            action_row = Adw.ActionRow()
            label = Gtk.Label(label=item)
            action_row.set_title_widget(label)

            switch = Gtk.Switch()
            switch.set_active(True)
            action_row.set_action_widget(switch)

            preferences_group.add(action_row)
        preferences_group.show_all()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = ZerotierGtkApplication()
    return app.run(sys.argv)
