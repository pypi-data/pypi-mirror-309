"""A lightweight wrapper for Phono3py"""

import numpy as np
from phono3py import Phono3py, load
from phono3py.api_phono3py import Phono3pyYaml

from vibes import konstanten as const
from vibes.helpers.numerics import get_3x3_matrix
from vibes.phonopy import enumerate_displacements, get_supercells_with_displacements
from vibes.structure.convert import to_phonopy_atoms

from . import _defaults as defaults


def prepare_phono3py(
    atoms,
    supercell_matrix,
    fc2=None,
    fc3=None,
    cutoff_pair_distance=defaults.kwargs.cutoff_pair_distance,
    displacement_dataset=None,
    is_diagonal=defaults.kwargs.is_diagonal,
    displacement=defaults.kwargs.displacement,
    symprec=defaults.kwargs.symprec,
    log_level=defaults.kwargs.log_level,
    **kwargs,
):
    """
    Prepare a Phono3py object

    Args:
    ----
        atoms: ase.atoms.Atoms
        supercell_matrix: np.ndarray
        fc2: np.ndarray
        fc3: np.ndarray
        cutoff_pair_distance: float
        displacement_dataset: dict
        is_diagonal: bool
        mesh: np.ndarray
        displacement: float
        symprec: float
        log_level: int

    Returns:
    -------
        phono3py.Phono3py

    """
    ph_atoms = to_phonopy_atoms(atoms, wrap=True)

    supercell_matrix = get_3x3_matrix(supercell_matrix)

    phonon3 = Phono3py(
        ph_atoms,
        supercell_matrix=np.transpose(supercell_matrix),
        symprec=symprec,
        is_symmetry=True,
        frequency_factor_to_THz=const.omega_to_THz,
        log_level=log_level,
    )

    if displacement_dataset is not None:
        phonon3.dataset = displacement_dataset

    phonon3.generate_displacements(
        distance=displacement,
        cutoff_pair_distance=cutoff_pair_distance,
        is_diagonal=is_diagonal,
    )

    if fc2 is not None:
        phonon3.set_fc2(fc2)
    if fc3 is not None:
        phonon3.set_fc3(fc3)

    return phonon3


def preprocess(
    atoms,
    supercell_matrix,
    cutoff_pair_distance=defaults.kwargs.cutoff_pair_distance,
    is_diagonal=defaults.kwargs.is_diagonal,
    displacement=defaults.kwargs.displacement,
    symprec=defaults.kwargs.symprec,
    log_level=defaults.kwargs.log_level,
    **kwargs,
):
    """
    Set up a Phono3py object and generate all the supercells necessary for the 3rd order

    Args:
    ----
        atoms: ase.atoms.Atoms
        supercell_matrix: np.ndarray
        cutoff_pair_distance: float
        is_diagonal: bool
        displacement: float
        symprec: float
        log_level: int

    Returns:
    -------
        phonon3: phono3py.Phono3py
        supercell: ase.atoms.Atoms
        supercells_with_disps: list of ase.atoms.Atoms

    """
    phonon3 = prepare_phono3py(
        atoms,
        supercell_matrix=supercell_matrix,
        cutoff_pair_distance=cutoff_pair_distance,
        is_diagonal=is_diagonal,
        displacement=displacement,
        symprec=symprec,
        log_level=log_level,
    )

    phonon3, scell, supercells_with_disps = get_supercells_with_displacements(phonon3)

    # exclude the none cells due to cutoff_pair_distance
    scs = [atoms for atoms in supercells_with_disps if atoms is not None]
    enumerate_displacements(scs)

    return phonon3, scell, scs


def phono3py_save(phonon: Phono3py, file=defaults.phono3py_params_yaml_file):
    """Adapted form Phono3py.save"""
    ph3py_yaml = Phono3pyYaml()
    ph3py_yaml.set_phonon_info(phonon)
    with open(file, "w") as w:
        w.write(str(ph3py_yaml))


def phono3py_load(
    file=defaults.phono3py_params_yaml_file,
    log_level=defaults.kwargs.log_level,
    **kwargs,
):
    """
    Load phono3py object from file

    Args:
    ----
      mesh: the q mesh
      log_level: log level
      kwargs: kwargs for `Phono3py.load`

    Returns:
    -------
      Phono3py

    """
    return load(file, **kwargs)
