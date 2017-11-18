import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from widget import Widget
from PIL import Image
import tempfile
import os
import base64

class Binary(Widget):

    def __init__(self, field):
	super(Binary, self).__init__(Gtk.Frame(), field)
	self.new_widget.set_label_align(0.5, 0.5)
	self.new_widget.set_shadow_type(Gtk.ShadowType.IN)
	self.button = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_OPEN))
	self.button.connect("clicked", self.on_open_menu)
	self.box.set_orientation(Gtk.Orientation(1))
	self.box.add(self.button)
	self.filter = Gtk.FileFilter()
	self.filter.add_pattern(field.filter_file)
	self.binary_data = None
        
    def on_open_menu(self, *args):
	dialog = Gtk.FileChooserDialog(
	    "Please select an image file", self.parent, Gtk.FileChooserAction.OPEN,
	    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN,
	     Gtk.ResponseType.OK))
	dialog.add_filter(self.filter)
	response = dialog.run()
	if response == Gtk.ResponseType.OK:
	    if self.new_widget.get_child():
		self.new_widget.remove(self.new_widget.get_child())
	    path = dialog.get_filename()
	    self.on_load(path)
	dialog.destroy()

    def on_load_image(self, path):
	path = self.resize_image(path)
	image = Gtk.Image.new_from_file(path)
	try:
	    image.set_from_file(path)
	    self.new_widget.add(image)
	    image.show()
	    self.new_widget.show_all()
	except:
	    pass

    def resize_image(self, path):
	file, ext = os.path.splitext(path)
	filename = os.path.basename(file)+"tmp"+ext
	filename = os.path.join(tempfile.gettempdir(), filename)
	size = 250, 250
	width, height = size
	im = Image.open(path)
	im.thumbnail(size)
	im.save(filename)
	self.binary_data = (base64.encodestring(im.tobytes()),
	                    ext.replace(".", ''))
	return filename

    def on_load_file(self, path, ext):
	document = open(path, "rb").readline()
	self.binary_data = (base64.encodestring(document), ext)
	image = Gtk.Image.new_from_stock(Gtk.STOCK_FILE, 5)
	image.set_pixel_size(125)
	self.new_widget.add(image)
	image.show()
	self.new_widget.show_all()

    def on_load(self, path):
	ext_imge = ["png", "jpg"]
	file, ext = os.path.splitext(path)
	ext = ext.replace(".", '')
	if ext in ext_imge:
	    return self.on_load_image(path)
	else:
	    return self.on_load_file(path, ext)

    def get_value(self):
	return self.binary_data
