# window.py
#
# Copyright 2024 Riemaru
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
from zerotiergtk.zerotierlib import *

class NewNetwork(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(application=app, title="Nueva Ventana")
        self.set_default_size(200, 100)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(box)

        self.entry = Gtk.Entry()
        box.append(self.entry)

        button = Gtk.Button(label="Acción y Cerrar")
        button.connect("clicked", self.on_button_clicked)
        box.append(button)

    def on_button_clicked(self, widget):
        texto = self.entry.get_text()
        print("Texto ingresado:", texto)
        self.close()

@Gtk.Template(resource_path='/org/zerotier/ZerotierGTK/window.ui')
class ZerotiergtkWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ZerotiergtkWindow'

    my_infobar = Gtk.Template.Child()
    action_row = Gtk.Template.Child()
    addnetwork = Gtk.Template.Child()
    refresh = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action_rows = []
        self.ztlib = ZeroTierNetwork()
        self.refresh.connect("clicked", self.on_refresh_clicked)

    def on_check_lib(self):
        if self.ztlib.zt_status():
            self.my_infobar.set_visible(False)
            self.on_row_action()
            return True
        else:
            self.my_infobar.set_visible(True)
            return False

    def on_service_set(self, status):
        status = self.ztlib.service(status)
        self.on_check_lib()
        return status

    def on_refresh_clicked(self, widget):
        self.on_row_action()

    def get_service_status(self):
        return self.ztlib.zt_enable_status()

    def remove_all_children(self):
        print(self.action_row.get_title())
        print(self.action_row.get_description())
        print(self.action_row.get_title())
        for i in self.action_rows:
            print(i)
            self.action_row.remove(i)

    def on_row_action(self):
        self.remove_all_children()
        networks = self.ztlib.get_networks()

        for network in networks:
            action_row = self.action_row

            if network["status"] == 'OK':
                status = 'emblem-default'
            elif network["status"] == 'ACCESS_DENIED':
                status = 'emblem-important'
            else:
                status = 'dialog-error'

            start = Adw.ActionRow.new()
            start.set_title(network["name"])
            start.set_subtitle(f"NetID: { network['nwid'] } Ip: {network['assignedAddresses']} Status: { network['status'] } ")
            start.set_icon_name(status)

            switch = Gtk.Switch()
            button = Gtk.Button()
            button.set_icon_name("preferences-system")
            button.set_valign(Gtk.Align.CENTER)

            switch.set_halign(Gtk.Align.END)
            switch.set_valign(Gtk.Align.CENTER)
            #switch.connect("notify::active")

            start.add_suffix(switch)
            start.add_suffix(button)

            action_id = network["id"]
            self.action_rows.append(start)
            action_row.add(start)
            action_row.set_name(action_id)


