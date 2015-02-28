#!/usr/bin/env python2
from ase import Atoms
from ase.optimize import QuasiNewton
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
