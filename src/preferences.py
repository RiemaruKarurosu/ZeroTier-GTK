import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw
from gi.repository import Gtk
from zerotier_gtk.zerotierlib import *


class PreferencesSettings:

    zerotier = ZeroTierNetwork()

    def __init__(self, zerotier_window, application):
        self.window_zerotier = zerotier_window
        window = Adw.PreferencesWindow(application=application)
        page = Adw.PreferencesPage()

        # Token Input
        token_group = Adw.PreferencesGroup()
        token_group.set_title("Token Input")
        self.create_token_input_row(token_group, "X-ZT1-Auth Token", self.on_token_input_changed)
        page.add(token_group)

        # Zerotier Service
        service_group = Adw.PreferencesGroup()
        service_group.set_title("Zerotier Service")
        print(zerotier_window.get_service_status())
        self.create_action_rows(service_group, "Zerotier start", "The app needs this to work", self.on_switch_state_start,
                                zerotier_window.on_check_lib(), True)
        self.create_action_rows(service_group, "Zerotier start on boot",
                                "Start zerotier service on boot -NOT WORKING- go to terminal and type: sudo systemctl enable zerotier-one",
                                self.on_switch_state_enable, zerotier_window.get_service_status(), False)
        page.add(service_group)

        window.add(page)
        window.present()

    def on_switch_state_start(self, switch, state):
        active = switch.get_active()
        service_code = 1 if active else 2

        if not self.window_zerotier.on_service_set(service_code):
            switch.disconnect_by_func(self.on_switch_state_start)
            switch.set_active(not active)
            switch.connect("state-set", self.on_switch_state_start)
            return True
        return False

    def on_switch_state_enable(self, switch, state):
        active = switch.get_active()
        service_code = 3 if active else 4

        self.window_zerotier.get_service_status()
        print(self.window_zerotier.on_service_set(service_code))
        self.window_zerotier.get_service_status()
        print('encendido 1' if active else 'apagado 1')
        return True

    def create_action_rows(self, group, title, subtitle, activation, status, active):
        start = Adw.ActionRow.new()
        start.set_title(title)
        start.set_subtitle(subtitle)

        switch = Gtk.Switch()

        switch.set_active(status)
        switch.set_sensitive(active)

        switch.set_halign(Gtk.Align.END)
        switch.set_valign(Gtk.Align.CENTER)
        switch.connect("notify::active", activation)

        start.add_suffix(switch)
        group.add(start)

    def create_token_input_row(self, group, title, change_callback):
        token_row = Adw.EntryRow.new()
        token_row.set_title(title)
        if self.zerotier.api_token:
            token_row.set_text(self.zerotier.api_token)
        token_row.connect("changed", self.on_token_input_changed)

        group.add(token_row)

    def verify_token(self, token):
        return self.zerotier.check_token(token)

    def on_token_input_changed(self, entry):
        token = entry.get_text()
        if self.verify_token(token):
            print(f"Token verificado: {token}")
            self.zerotier.api_token = token
            self.zerotier.save_token()
        else:
            print("Token no válido. Por favor, introduce un token válido.")

    def show_info_dialog(self, button):
        dialog = Gtk.MessageDialog(
            transient_for=None,
            flags=0,
            type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            message_format="Información adicional aquí."
        )
        dialog.run()
        dialog.destroy()
