import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(path)

os.environ.update({'db_name': os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", 'data/payroll.db'))})

import company
