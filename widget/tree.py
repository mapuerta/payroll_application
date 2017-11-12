import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Tree(Gtk.Window):
    def __init__(self, model, title=False):
	Gtk.Window.__init__(self, title=title)
	self.set_default_size(350, 500)
	self.set_border_width(10)
	self.model = model
	self.conten = Gtk.Grid()
        self.conten.set_column_homogeneous(True)
        self.conten.set_row_homogeneous(True)
        self.add(self.conten)
	self.treeview = None
	self.data_model_store = None
	self._add_list_store()
	#~ self.load_data()
	self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.conten.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.scrollable_treelist.add(self.treeview)
	self.show_all()


    def _add_list_store(self):
	type_list = []
	columns_list = []
	for name, fields in self.model._columns.items():
	    type_list.append(fields.type)
	    columns_list.append(fields.String)
	self.data_model_store = Gtk.ListStore(str, str, bool)
	self.treeview = Gtk.TreeView.new_with_model(self.data_model_store)
	self.load_data()
	for i, column_title in enumerate(columns_list):
	    print column_title
	    renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
	    self.treeview.append_column(column)

    def load_data(self):
	software_list = [("Firefox", "22",  True),
                 ("Eclipse", "2004", True),
                 ("Pitivi", "2004", False),
                 ("Pitivi", "2004", False),
                 ("Pitivi", "2004", False),
                 ("Pitivi", "2004", False),
                 ("Pitivi", "2004", False),
                 ("Frostwire", "2004", True)]
	for software_ref in software_list:
            self.data_model_store.append(list(software_ref))

class Fieldtest(object):
    def __init__(self, String, selection=[("M", "Masculino"), ("F", "Femenino")],
		 digits=2, comodel_name="model", size=5, required=False, type=int):
	self.String = String
	self.selection = selection
	self.digits = digits
	self.comodel_name = comodel_name
	self.size = size
	self.required = required
	self.type = type

class modelA:
    _columns = {
    "user": Fieldtest("Usuario", type=str),
    "cedula": Fieldtest("Cedula", type=str),
    "gerente": Fieldtest("Gerente", type=bool),
    }

tree = Tree(modelA())
tree.connect("delete-event", Gtk.main_quit)
tree.show_all()
Gtk.main()
