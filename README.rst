Copyright (C) 2010 Troels Kofoed Jacobsen

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Installation
============
It may be necessary to edit customize.py to point to openbabel include and
library dirs.

Global installation:
python2 setup.py install

User installation
python2 setup.py install --home=$HOME/opt
export PYTHONPATH=$HOME/opt/lib/python:$PYTHONPATH

NOTE: This compilation precedure is only necessary as the upstream openbabel
python wrapper does not wrap vector3. If/when this is fixed, the C code can be
removed. See the following bug for details:
http://sourceforge.net/tracker/?func=detail&aid=2969937&group_id=40728&atid=428740
        
Introduction
============

OpenBabel is a chemical toolbox designed to speak the many languages of
chemical data. It's an open, collaborative project allowing anyone to search,
convert, analyze, or store data from molecular modeling, chemistry,
solid-state materials, biochemistry, or related areas.  

The obcalc.OBForceField calculator use the force fields (currently UFF and
ghemical) included in OpenBabel.

To use this calculator you need to have the OpenBabel python bindings
installed:

- Arch Linux: python2-openbabel

OpenBabel: http://www.openbabel.org

OBForceField Calculator Class
=============================

OBForceField(force_field='UFF', bonds=None)

Here is a detailed list of all the keywords for the calculator:

================ ========= ================  =================================================
keyword          type      default value     description
================ ========= ================  =================================================
``force_field``  ``str``   ``'UFF'``         Force field ('UFF', 'ghemical', 'GAFF', 'MMFF94')
``bonds``        ``list``  ``None``          List of bonds in molecule given as:
                                             [[begin atom idx, end atom idx, bond order], ...]
                                             If None OpenBabel will try to guess it. 
``txt``          ``str``   ``None``          Which file to write output too.  Defaults to
                                             stdout ('-').
================ ========= ================  =================================================

Examples
========

Automatic bond detection 
------------------------

Here is an example of how to calculate the total energy CO::
        
  #!/usr/bin/env python2
  from ase import molecule
  from obcalc import OBForceField
  
  atoms = molecule('CO')

  calc = OBForceField()
  atoms.set_calculator(calc)
  e = atoms.get_potential_energy()

Adding bonds manually
---------------------

If we want to relax e.g. CO2 starting with a very large interatomic distances,
OpenBabel will not detect the bonds and we have to put them manually::

  #!/usr/bin/env python2
  from ase import Atoms, QuasiNewton
  from obcalc import OBForceField

  atoms = Atoms('OCO', [[0.0, 0.0, 0.0],
                        [3.0, 0.0, 0.0],
                        [6.0, 0.0, 0.0]])

  calc = OBForceField()
  atoms.set_calculator(calc)
  relax = QuasiNewton(atoms)
  relax.run(fmax=0.05)
  # This results in a even larger interatomic distances
  # Therefore we add two double bonds

  bonds = [[0, 1, 2], # Double bond between atom 0 and atom 1
           [1, 2, 2]] # Double bond between atom 1 and atom 2
  calc = OBForceField(bonds=bonds)
  atoms.set_calculator(calc)
  relax = QuasiNewton(atoms)
  relax.run(fmax=0.05)
  # This gives the expected results

Building molecules
==================
The code also contains a function which builds an atoms object from a SMILES
string. To build an azobenzene molecule you could do::

  #!/usr/bin/env python2
  from obcalc.tools import build_molecule
  atoms = build_molecule('C1=CC=CC=C1N=NC2=CC=CC=C2')

Or if you would build ethanol, you could do::

  atoms = build_molecule('CCO')

See the wikipedia article for info:
http://en.wikipedia.org/wiki/Simplified_molecular_input_line_entry_specification
