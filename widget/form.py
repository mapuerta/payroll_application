import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

COLSPAM = 4
COLS = 4

class Form(Gtk.Window):

    def __init__(self, model, title=False):
	Gtk.Window.__init__(self, title=title)
	self.witgets = []
	self.model = model
	grid = Gtk.Grid()
        self.add(grid)
	self.conten = grid
	self.rows = 0
	self.cols = 0
	self.add_basic_buttons()

    def add_basic_buttons(self):
	box = Gtk.Box(spacing=6)
	create = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_SAVE))
	update = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_EDIT))
	box.pack_start(create, True, True, 0)
	box.pack_start(update, True, True, 0)
	self.conten.add(box)
	self.new_line()
	
    def set_cols(self, position):
	self.cols += position
	if self.cols >= 4:
	   self.cols = 0
	   self.rows += 1 
	
    def new_witget(self, widget):
	self.witgets.append(widget)
	self.conten.attach(widget.widget, self.cols, self.rows, 1, 1)
	self.set_cols(1)

    def new_line(self):
	self.cols = 0
	self.rows += 2

    def on_save(self):
	values = {}
	for widget in self.witgets:
	    values.update({widget.field_name: getattr(widget, "get_value")})
	#~ self.model.create(value)
	

