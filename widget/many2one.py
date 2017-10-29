import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from widget import Widget


class Related(Widget):

    def __init__(self, field, domain=False):
	self._domain = domain or []
	super(Related, self).__init__(Gtk.Entry(), field)
	icon_name = "system-search-symbolic"
	self.new_widget.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
            icon_name)
	self.new_widget.connect("icon-press", self.on_search)
        
    def on_search(self, *args):
	#~ ids = self._model.search(self._domain)
	pass
	
    def show_view(self, data):
	pass

    def validate(self):
	pass

