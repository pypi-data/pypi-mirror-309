"""a light wrapper for spglib"""
import collections

import numpy as np
import spglib as spg
from ase.atoms import Atoms

from vibes.konstanten import symprec as default_symprec
from vibes.structure.convert import to_spglib_cell


def cell_to_Atoms(lattice, scaled_positions, numbers, info=None):
    """
    Convert from spglib cell to Atoms

    Parameters
    ----------
    lattice: np.ndarray
        The lattice vectors of the structure
    scaled_positions: np.ndarray
        The scaled positions of the atoms
    numbers: list
        Atomic numbers of all the atoms in the cell
    info: dict
        additional information on the structure

    Returns
    -------
    ase.atoms.Atoms:
        The ASE Atoms object representation of the material

    """
    atoms_dict = {
        "cell": lattice,
        "scaled_positions": scaled_positions,
        "numbers": numbers,
        "pbc": True,
        "info": info,
    }

    return Atoms(**atoms_dict)


def get_symmetry_dataset(
    atoms: Atoms, index_maps: bool = False, symprec: float = 1e-5
) -> collections.namedtuple:
    """
    Return the spglib symmetry dataset

    Parameters
    ----------
    atoms: ase.atoms.Atoms
        The structure to get the dataset of
    index_maps: bool
        Optionally include index maps for the symmetry operations (expensive)
    symprec: float
        The tolerance for determining symmetry and the space group

    Returns
    -------
    AttributeDict
        The symmetry_dataset for the structure including cartesian rotations and
        translations as namedtuple

    """
    spg_cell = to_spglib_cell(atoms)
    data = spg.get_symmetry_dataset(spg_cell, symprec=symprec)

    uwcks, count = np.unique(data["wyckoffs"], return_counts=True)
    data["wyckoffs_unique"] = [(w, c) for (w, c) in zip(uwcks, count)]

    # add euivalent atoms
    ats, count = np.unique(data["equivalent_atoms"], return_counts=True)
    data["equivalent_atoms_unique"] = [(a, c) for (a, c) in zip(ats, count)]

    # add cartesian rotations and translations
    cell = atoms.cell
    rotations = data["rotations"]
    rotations_cart = [cell.T @ (rot @ cell.reciprocal()) for rot in rotations]
    rotations_cart = np.array(rotations_cart).round(decimals=15)  # remove 0s
    data["rotations_cartesian"] = rotations_cart

    translations = data["translations"]
    translations_cart = [trl @ cell for trl in translations]
    translations_cart = np.array(translations_cart).round(decimals=15)  # remove 0s
    data["translations_cartesian"] = translations_cart

    if index_maps:  # attach index map
        kw = {
            "rotations_cartesian": rotations_cart,
            "translations_cartesian": translations_cart,
        }
        data["index_maps"] = _get_index_maps(atoms, **kw)

    return collections.namedtuple("spg_dataset", data.keys())(**data)


def _get_index_maps(
    atoms: Atoms, rotations_cartesian, translations_cartesian
) -> np.ndarray:
    """
    create index maps for structure in atoms for the given symmetry operations

    Args:
    ----
        atoms: the structure, e.g., primitive cell
        rotations: rotations matrices IN CARTESIAN COORDS
        translations: translation vectors IN CARTESIAN COORDS

    Returns:
    -------
        array containing index maps for each symmetry operation (rot, trl)

    """
    from vibes.helpers.supercell import map_indices

    pos_cart = atoms.positions.copy()

    index_maps = np.zeros([len(rotations_cartesian), len(atoms)], dtype=int)

    for ii, (rc, tc) in enumerate(zip(rotations_cartesian, translations_cartesian)):
        atoms_transformed = atoms.copy()
        atoms_transformed.positions = (rc @ pos_cart.T).T + tc

        index_map = map_indices(atoms, atoms_transformed)
        index_maps[ii, :] = index_map

    return index_maps


def get_index_maps(atoms: Atoms, spg_data: collections.namedtuple) -> np.ndarray:
    """
    return index maps for structure in Atoms and symmetry operations in spg_data

    Args:
    ----
        atoms: the structure
        spg_data: spg data obtained from `get_symmetry_dataset`

    Returns:
    -------
        the index maps

    """
    kw = {
        "rotations_cartesian": spg_data.rotations_cartesian,
        "translations_cartesian": spg_data.translations_cartesian,
    }
    return _get_index_maps(atoms, **kw)

def map_unique_to_atoms(atoms, symprec=default_symprec):
    """
    Map each symmetry unique atom to other atoms as used by phonopy PDOS

    Parameters
    ----------
    atoms: ase.atoms.Atoms
        The structure to get the dataset of
    symprec: float
        The tolerance for determining symmetry and the space group

    Returns
    -------
    mapping: np.ndarray
        The mapping of symmetry unique atoms to other atoms

    """
    ds = get_symmetry_dataset(atoms, symprec=symprec)

    uniques = np.unique(ds.equivalent_atoms)

    mapping = [[] for _ in range(len(uniques))]

    for ii, index in enumerate(ds.equivalent_atoms):
        for jj, unique in enumerate(uniques):
            if index == unique:
                mapping[jj].append(ii)

    return mapping


def get_spacegroup(atoms, symprec=default_symprec):
    """
    Return spglib spacegroup

    Parameters
    ----------
    atoms: ase.atoms.Atoms
        The structure to get the dataset of
    symprec: float
        The tolerance for determining symmetry and the space group

    Returns
    -------
    str:
        The spglib space group

    """
    return spg.get_spacegroup(to_spglib_cell(atoms), symprec=symprec)


def refine_cell(atoms, symprec=default_symprec):
    """
    Refine the structure

    Parameters
    ----------
    atoms: ase.atoms.Atoms
        The structure to get the dataset of
    symprec: float
        The tolerance for determining symmetry and the space group

    Returns
    -------
    ase.atoms.Atoms:
        The refined structure of atoms

    """
    lattice, scaled_positions, numbers = spg.refine_cell(to_spglib_cell(atoms), symprec)

    return cell_to_Atoms(lattice, scaled_positions, numbers)


def standardize_cell(
    atoms, to_primitive=False, no_idealize=False, symprec=default_symprec
):
    """
    Wrap spglib.standardize_cell

    Parameters
    ----------
    atoms: ase.atoms.Atoms
        The structure to get the dataset of
    to_primitive: bool
        If True go to the primitive cell
    no_idealize: bool
        If True do not idealize the cell
    symprec: float
        The tolerance for determining symmetry and the space group

    Returns
    -------
    ase.atoms.Atoms
        The standardized structure of atoms

    """
    cell = to_spglib_cell(atoms)
    args = spg.standardize_cell(cell, to_primitive, no_idealize, symprec)

    return cell_to_Atoms(*args)
