from gi.repository import Adw
from gi.repository import Gtk

class PreferencesDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Preferencias", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(250, 150)

    def on_preference_action(self, action, parameter):
        builder = Gtk.Builder()
        builder.add_from_file("preferences_dialog.glade")

        dialog = builder.get_object("preferences_dialog")
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            # Realizar acciones necesarias cuando se guarda o acepta
            print("Preferencias guardadas")

        dialog.destroy()
