"""
Project: flask-rest
Author: Saj Arora
Description: Sets the pylibs director as one of the search paths for
python runtime to find libraries that are requested in this app
"""
import sys

sys.path.insert(0, './pylibs')