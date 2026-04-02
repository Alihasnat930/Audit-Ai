import nbformat 
from nbformat.v4 import new_markdown_cell, new_code_cell 
path = 'notebooks/model_experiments.ipynb' 
nb = nbformat.read(path, as_version=4) 
nb.cells.insert(1, intro) 
