import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
py_foundry_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(root_dir)
sys.path.append(py_foundry_dir)
