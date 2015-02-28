#!/usr/bin/env python2
from ase.structure import molecule
from obcalc import OBForceField

atoms = molecule('CO')

calc = OBForceField()
atoms.set_calculator(calc)
e = atoms.get_potential_energy()
