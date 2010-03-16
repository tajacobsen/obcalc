"""Tools easing the work with OpenBabel

Copyright (C) 2010 by Troels Kofoed Jacobsen
Code released under GPLv2. See COPYING for details.
"""
import numpy as np
import openbabel as ob
from ase import Atom, Atoms, units

from obcalc.obwrap import forces_ni

def get_forces(mol):
    N =  mol.NumAtoms()
    f = np.zeros((N, 3))
    for i in range(N):
        for j in range(3):
            f[i, j] = forces_ni(mol, i, j)

    return f

def add_bonds(mol):
    """Automatically add bonds to molecule"""

    mol.ConnectTheDots()
    mol.PerceiveBondOrders()

    return mol

def atoms_to_obmol(atoms, bonds=None):
    """Convert an Atoms object to an OBMol object.

    Parameters
    ==========
    atoms: Atoms
    bonds: list of lists of 3xint
        Define bonds between atoms such as:
            [[begin atom index, end atom index, bond order],
             ...
            ]
        If None the OpenBabel will try to construct the bonds
        automatically.
    """
    mol = ob.OBMol()
    for atom in atoms:
        a = mol.NewAtom()
        a.SetAtomicNum(int(atom.number))
        a.SetVector(atom.position[0], atom.position[1], atom.position[2])

    if bonds is None:
        mol = add_bonds(mol)
    else:
        for bond in bonds:
            mol.AddBond(bond[0] + 1, bond[1] + 1, bond[2])

    return mol

def obmol_to_atoms(mol, return_bonds=False):
    """Convert an OBMol object to an Atoms object.

    Parameters
    ==========
    mol: OBMol
    return_bonds: bool
        If True, a list of list of 3xint describing the bonds will be returned.
    """
    atoms = Atoms()
    for i in range(mol.NumAtoms()):
        obatom = mol.GetAtom(i + 1)
        atoms.append(Atom(obatom.GetAtomicNum(),
                          [obatom.GetX(),
                           obatom.GetY(),
                           obatom.GetZ()]
                         )
                    )

    if return_bonds:
        return atoms, bonds
    else:
        return atoms

def get_bonds(mol):
    if isinstance(mol, Atoms):
        mol = atoms_to_obmol(mol)

    bonds = []
    for i in range(mol.NumBonds()):
        obbond = mol.GetBond(i)
        bond = [obbond.GetBeginAtomIdx() - 1,
                obbond.GetEndAtomIdx() - 1,
                obbond.GetBondOrder()]
        bonds.append(bond)
    return bonds
