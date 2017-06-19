# coding: utf-8
header = """# Copyright (C) 2016  Carmelo Mordini
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
import numpy as np
import matplotlib.cm as cm

docstring = """\"\"\"
Convenience module to store a sampling of the matplotlib's colormaps
without reyling on the whole matplotlib as a dependency.
The dictionary is inspired to matplotlib.cm.cmap_d but the entries are pure numpy arrays with
a sample of positions between 0 and 1, and the corresponding colors in RGBA format.
This is intended to be used as:

>>> pos, vals = mpl_cmap_d[name]
>>> cmap = pg.colormap.ColorMap(pos, vals)
>>> display.setColorMap(cmap)
\"\"\"
"""
import contextlib

@contextlib.contextmanager
def printoptions(*args, **kwargs):
    original = np.get_printoptions()
    np.set_printoptions(*args, **kwargs)
    yield 
    np.set_printoptions(**original)

def set_mpl_colormap(name, samples):  
    mpl_cmap = cm.get_cmap(name, samples)
    pos = np.linspace(0, 1, samples)
    vals = mpl_cmap(pos)
    return pos, vals


# names = ('gist_stern', 'RdBu_r')
module_name = 'mpl_cmaps.py'

names = cm.cmap_d.keys()
samples = 11

grays = ['gray', 'gray_r', 'Greys', 'Greys_r']

with printoptions(formatter={'float': '{: 0.4f}'.format}, threshold=samples*4):
    file = "from numpy import array\n\n"
    file += "mpl_cmap_d = \\\n{\n"
    for name in names:
        ns = 2 if name in grays else samples
        pos, vals = set_mpl_colormap(name, ns)
        entry = "'{:s}':\n".format(name)
        entry += "(\n{0:s},\n{1:s}\n),\n".format(pos.__repr__(), vals.__repr__())
        # vals.__repr__()
        file +=entry
    file +="}"
# print(file)

with open(module_name, 'w') as f:
    f.write(header)
    f.write(docstring)
    f.write(file)
