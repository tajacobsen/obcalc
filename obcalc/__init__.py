"""
This module contains an interface to the Force Fields available in the
OpenBabel library ( http://openbabel.org/ ).

The OpenBabel Python interface is described in

O'Boyle et al., Chem. Cent. J., 2, 5 (2008), doi:10.1186/1752-153X-2-5

Copyright (C) 2010 Troels Kofoed Jacobsen
Code released under GPLv2 (or later). See COPYING for details.
"""
import sys
import time

import numpy as np
import openbabel as ob
from ase import units, Atom, Atoms

from obcalc.tools import atoms_to_obmol, get_forces, get_bonds

class OBForceField:
    """OpenBabel Force Field calculator

    Currently supporting ghemical and UFF force fields:
    UFF:
        http://openbabel.org/wiki/OBForceFieldUFF
        J. Am. Chem. Soc. 1992, Vol. 114, No. 25, 10024-10035
    ghemical:
        http://openbabel.org/wiki/OBForceFieldGhemical
        http://www.uku.fi/~thassine/projects/ghemical/

    """
    def __init__(self, force_field='UFF', bonds=None, txt=None):
        """Construct OpenBabel Force Field Calculator object.

        Parameters
        ==========
        force_field: str
            One of 'UFF', 'ghemical', 'GAFF', 'MMFF94'
        bonds: list of lists of 3xint
            Define bonds between atoms such as:
                [[begin atom index, end atom index, bond order],
                 ...
                ]
            If None the calculator will try to construct the bonds
            automatically.
        txt: str
            Which file to write output too. Defaults to stdout ('-').
        """

        self.force_field = force_field
        self.atoms = None
        self.bonds = bonds

        self.energy = None
        self.force = None

        if txt is None:
            self.txt = None
        elif txt == '-':
            self.txt = sys.stdout
        else:
            self.txt = open(txt, 'w')

    def get_potential_energy(self, atoms=None, force_consistent=False):
        """Return total energy"""
        self.calculate(atoms)
        return self.energy

    def get_forces(self, atoms=None):
        """Return the forces.

        Forces are currently calculated using finite differences, as openbabel
        does not expose the GetGradient function.
        """
        self.calculate(atoms)
        return self.forces

    def get_stress(self, atoms):
        """Return the stress."""
        raise NotImplementedError

    def set_atoms(self, atoms):
        self.atoms = atoms.copy()

    def calculation_required(self, atoms, quantities):
        if self.energy is None or self.forces is None:
            return True
        if len(atoms) != len(self.atoms) or \
           (atoms.numbers != self.atoms.numbers).any() or \
           (atoms.get_positions() != self.atoms.get_positions()).any():
            return True
        else:
            return False

    def calculate(self, atoms):
        if atoms is None:
            atoms = self.atoms

        if self.calculation_required(atoms, ['energy', 'forces']):
            mol = atoms_to_obmol(atoms, self.bonds)
            ff = ob.OBForceField.FindForceField(self.force_field)
            if ff is None:
                print "Could not find force field: %s" % (self.force_field,)
            ff.Setup(mol)
            energy = ff.Energy()
            ff.GetCoordinates(mol)
            forces = get_forces(mol)

            if ff.GetUnit() == 'kJ/mol':
                energy *= units.kJ / units.mol
                forces *= units.kJ / units.mol
            elif ff.GetUnit() == 'kcal/mol':
                energy *= units.kcal / units.mol
                forces *= units.kcal / units.mol
            else:
                raise NotImplementedError

            self.energy = energy
            self.forces = forces

            self.atoms = atoms.copy()

            # Print output
            if self.txt is not None:
                print >> self.txt, time.asctime()

                self.print_positions()
                print >> self.txt, ''

                self.print_bonds(mol)
                print >> self.txt, ''

                self.print_energy()
                print >> self.txt, ''

                self.print_forces()
                print >> self.txt, '\n'

    def print_positions(self):
        symbols = self.atoms.get_chemical_symbols()
        print >> self.txt, 'Positions:'
        for a, pos_c in enumerate(self.atoms.get_positions()):
            symbol = symbols[a]
            print >> self.txt, '%3d %-2s %9.4f %9.4f %9.4f' % \
                    ((a, symbol) + tuple(pos_c))

    def print_bonds(self, mol):
        symbols = self.atoms.get_chemical_symbols()
        order_to_symbol = ['', '-', '=', '#']
        print >> self.txt, 'Bonds:'
        print >> self.txt, ' ' * (3 + 1 + 5 + 1) + '%-5s %-5s %-5s' % \
                ('Start', 'End', 'Order')
        bonds = get_bonds(mol)
        for a, bond in enumerate(bonds):
            symbol0 = symbols[bond[0]]
            symbol1 = symbols[bond[1]]
            order = order_to_symbol[bond[2]]
            print >> self.txt, '%3d %2s%1s%-2s %5i %5i %5i' % \
                           ((a, symbol0, order, symbol1) + tuple(bond))


    def print_energy(self):
        print >> self.txt, 'Energy in eV:\t%.4f' % self.energy

    def print_forces(self):
        symbols = self.atoms.get_chemical_symbols()
        print >> self.txt, 'Forces in eV/Ang:'
        for a, symbol in enumerate(symbols):
            print >> self.txt, '%3d %-2s %10.5f %10.5f %10.5f' % \
                    ((a, symbol) + tuple(self.forces[a]))

