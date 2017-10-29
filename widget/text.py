import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from widget import Widget

class DialogText(Gtk.Dialog):
    def __init__(self, parent, last_value):
	Gtk.Dialog.__init__(self, "Texto", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
	self.last_value = last_value
	box = self.get_content_area()
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_size_request(-1, 80)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
	if last_value:
	    self.textbuffer.set_text(last_value)
        scrolledwindow.add(self.textview)
	box.add(scrolledwindow)
	self.set_default_size(350, 250)
        self.show_all()

    def get_value(self):
	start = self.textbuffer.get_start_iter()
	end = self.textbuffer.get_end_iter()
	return  self.textbuffer.get_text(start, end, True)
	

class Text(Widget):

    def __init__(self, field, **kwargs):
	super(Text, self).__init__(Gtk.Entry(), field)
	special_widgetk = kwargs.get("widget")
	if special_widgetk == "textbox":
	    self.new_widget.set_editable(False)
	    icon_name = Gtk.STOCK_EDIT
	    self.new_widget.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
						    icon_name)
	    self.new_widget.connect("icon-press", self.on_open_menu)

    def on_open_menu(self, *args):
	last_value = self.new_widget.get_text()
	dialog = DialogText(self.parent, last_value)
        response = dialog.run()
	if response == Gtk.ResponseType.OK:
	    self.new_widget.set_text(dialog.get_value())
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
             dialog.destroy()
