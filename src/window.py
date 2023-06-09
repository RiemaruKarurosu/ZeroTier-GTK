# window.py
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

from gi.repository import Adw
from gi.repository import Gtk
from zerotier_gtk.zerotierlib import *

@Gtk.Template(resource_path='/org/gnome/zerotiergtk/window.ui')
class ZerotierGtkWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ZerotierGtkWindow'

    my_infobar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ztlib = ZeroTierNetwork()

    def on_check_lib(self):
        if self.ztlib.zt_status():
            self.my_infobar.set_visible(False)
            return True
        else:
            self.my_infobar.set_visible(True)
            return False

    def on_service_set(self,status):
        status = self.ztlib.service(status)
        self.on_check_lib()
        return status

    def get_service_status(self):
        return self.ztlib.zt_enable_status()

        
