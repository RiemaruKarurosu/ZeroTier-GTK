import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw
from gi.repository import Gtk

class PreferencesSettings:

    def __init__ (self,zerotier_window,application):
        self.window_zerotier = zerotier_window
        window = Adw.PreferencesWindow(application=application)
        page = Adw.PreferencesPage()
        group = Adw.PreferencesGroup()
        group.set_title("Zerotier Service")
        print(zerotier_window.get_service_status())
        self.create_action_rows(group,"Zerotier start","The app needs this to work",self.on_switch_state_start,zerotier_window.on_check_lib(),True)
        self.create_action_rows(group,"Zerotier start on boot","Start zerotier service on boot -NOT WORKING- go to terminal and type: sudo systemctl enable zerotier-one",self.on_switch_state_enable,zerotier_window.get_service_status(),False)
        page.add(group)
        window.add(page)
        window.present()


    # Needs other way to do this
    def on_switch_state_start(self,switch,state):
        if switch.get_active():
            if not self.window_zerotier.on_service_set(1):
                switch.disconnect_by_func(self.on_switch_state_start)
                switch.set_active(False)
                switch.connect("state-set",self.on_switch_state_start)
                return True
        else:
            if not self.window_zerotier.on_service_set(2):
                switch.disconnect_by_func(self.on_switch_state_start)
                switch.set_active(True)
                switch.connect("state-set",self.on_switch_state_start)
                return True



    def on_switch_state_enable(self,switch,state):
        if switch.get_active():
            self.window_zerotier.get_service_status()
            self.window_zerotier.on_service_set(3)
            print('encendido 1')
            pass
        else:
            self.window_zerotier.get_service_status()
            self.window_zerotier.on_service_set(4)
            print('apagado 1')
            pass

    def create_action_rows(self,group,title,subtitle,activation,status,active):
        start = Adw.ActionRow.new()
        start.set_title(title)
        start.set_subtitle(subtitle)

        switch = Gtk.Switch()

        switch.set_active(status)
        switch.set_sensitive(active)

        switch.set_halign(Gtk.Align.END)
        switch.set_valign(Gtk.Align.CENTER)
        switch.connect("notify::active",activation)

        start.add_suffix(switch)
        group.add(start)

        
