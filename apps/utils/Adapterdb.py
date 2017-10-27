import os, glob, imp

DATABASE = os.environ.get('db_name')

def init_connector_db(adapter="sqlite"):
    modules = {}
    class_connector = "{0}Connector".format(adapter.title())
    file_connector = "{0}_connector".format(adapter)
    path = os.path.dirname(os.path.realpath(__file__))
    for path in glob.glob(os.path.join(path, '..', 'connectors/[!_]*.py')):
        name, ext = os.path.splitext(os.path.basename(path))
        modules[name] = imp.load_source(name, path)
    instance_connector = getattr(modules[file_connector], class_connector)(DATABASE)
    return instance_connector
