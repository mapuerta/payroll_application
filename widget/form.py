import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Form(Gtk.Window):

    def __init__(self, model, title=False):
	Gtk.Window.__init__(self, title=title)
	self.set_default_size(350, 500)
	self.witgets = []
	self.model = model
	grid = Gtk.Grid()
	grid.set_row_spacing(3)
	grid.set_column_spacing(3)
	self.set_border_width(6)
        self.add(grid)
	self.conten = grid
	self.rows = 0
	self.cols = 0
	self.add_basic_buttons()
	self.conten.set_column_homogeneous(True)

    def add_basic_buttons(self):
	box = Gtk.Box(spacing=6)
	create = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_SAVE))
	update = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_EDIT))
	box.pack_start(create, False, False, 1)
	box.pack_start(update, False, False, 1)
	self.conten.attach(box, 0, 0, 1, 10)
	self.new_line()

    def set_cols(self, position):
	self.cols += position
	if self.cols >= 4:
	    self.cols = 0
	    self.rows += 1

    def new_witget(self, widget):
	widget.set_paren(self)
	widget.set_model(self.model)
	self.witgets.append(widget)
	self.conten.attach(widget.widget, self.cols, self.rows, 1, 1)
	self.set_cols(1)

    def new_line(self):
	self.cols = 0
	self.rows += 10

    def on_save(self):
	values = {}
	for widget in self.witgets:
	    values.update({widget.field_name: widget.on_save})
	self.model.create(value)


