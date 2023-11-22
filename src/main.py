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
from zerotier_gtk.zerotierlib import *
from zerotier_gtk.preferences import *

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import ZerotierGtkWindow
from zerotier_gtk.zerotierlib import *


class ZerotierGtkApplication(Adw.Application):

    ztlib = ZeroTierNetwork()

    def __init__(self):
        super().__init__(application_id='org.gnome.zerotiergtk',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)




    def do_activate(self):
        self.zerotier_window = self.props.active_window
        if not self.zerotier_window:
            self.zerotier_window = ZerotierGtkWindow(application=self)
            self.zerotier_window.on_check_lib()
        self.zerotier_window.present()

    def on_about_action(self, widget, _):
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Zerotier-GTK',
                                application_icon='org.gnome.zerotiergtk',
                                developer_name='NOT FOR ACTUAL USE',
                                version='1.4.3 - ALPHA',
                                developers=['Riemaru Karurosu'],
                                copyright='© 2023 Zerotier-GUI',
                                issue_url='https://github.com/RiemaruKarurosu/ZeroTier-GTK/issues')
        about.present()

    def on_preferences_action(self, widget, _):
        preferences = PreferencesSettings(self.zerotier_window, self)




    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    app = ZerotierGtkApplication()
    return app.run(sys.argv)
