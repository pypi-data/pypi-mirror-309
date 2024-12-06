# Tutorial

!!! warning "Warnings"

	- All tutorials assume you have a background in (_ab initio_) calculations and in the fundamental theory of vibrations in solids. The background theory is written down to establish a common notation;
	    and introduction to these topics can be found various textbooks, some of which you find in the [references](references.md).
	- The settings used throughout the tutorials are chosen in order to allow for smooth calculations. They are _not_ sufficient for producing publication-ready scientific results.
	- We assume you have [installed](../Installation.md) and [configured](../Installation.md#configuration) `FHI-vibes` successfully.
	- We assume you have some working experience with `python`, `numpy`, and `jupyter-notebook`.

In this tutorial, we introduce the functionality of `FHI-vibes` with hands-on examples.

### Outline

The following tutorials are available:

- [Single point calculations](0_singlepoint.md)
- [Geometry optimization](1_geometry_optimization.md)
- [Phonon calculations](2_phonopy_intro.md)
- [Molecular dynamics](3_md_intro.md)
- [Harmonic sampling](4_statistical_sampling.md)
- [Anharmonicity quantification](5_anharmonicity_quantification.md)
- [Lattice Expansion](6_lattice_expansion.md)
- [Green Kubo](7_green_kubo.md)
- [High-Throughput workflows](../High_Throughput/Tutorial/0_configuring_fw_for_vibes.md)

### LDA-Silicon

All tutorials discuss fcc-Silicon, which is treated at the _ab initio_ level using FHI-aims and the LDA exchange-correlation functional.
Although only very moderate computational resources are needed (mostly few minutes of runtime on a modern multi-core node), the tutorials
are intended to be run on a computing cluster, since they aim at showcasing typical
FHI-vibes usage.

!!! info
	We assume that you are familiar with running *FHI-aims* for performing _ab initio_ calculations.



Typically, FHI-vibes requires two files: One describes the geometry of the system
following  syntax used for `geometry.in` files in FHI-aims. For fcc-Silicon in the
primitive unit cell, it thus reads

??? info "Geometry input file `geometry.in`"
    ```
    lattice_vector 0.0000000000000000 2.7149999999999999 2.7149999999999999
    lattice_vector 2.7149999999999999 0.0000000000000000 2.7149999999999999
    lattice_vector 2.7149999999999999 2.7149999999999999 0.0000000000000000
    atom_frac 0.0000000000000000 0.0000000000000000 0.0000000000000000 Si
    atom_frac 0.2500000000000000 0.2500000000000000 0.2500000000000000 Si
    ```

The second files describes the computational tasks and the numerical parameters used
in the calculation. Accordingly, it also contains a `calculator` section that specifies
that FHI-aims shall be used at the LDA level of theory and which numerical settings shall
be used for the Silicon example in the tutorial. This section thus reads:

??? info "`calculator` section for task in put file"
    ```
	[files]
	geometry:                      geometry.in

    [calculator]
    name:                          aims
    socketio:                      true

    [calculator.parameters]
    xc:                            pw-lda
    compute_forces:                true

    [calculator.kpoints]
    density:                       2

    [calculator.basissets]
    Si:                            light
    ```

Let's walk through the settings once:

- `[files]`
	- `geometry: geometry.in`: read the input geometry from `geometry.in`.
- `[calculator]`
	- `name: aims` means that `FHI-aims` will be used as explained [here](../Documentation/calculator_setup.md#calculator).
	- `socketio: true` means that the socketIO communication will be used. This will speed up the computation of related structures.
- `[calculator.parameters]`: these are settings that go directly to `control.in`
	- `xc: pw-lda` means that the pw-LDA exchange-correlation functional will be used.
	- `compute_forces: true` means that forces will be computed.
- `[calculator.kpoints]`: this is an optional way of setting k-point grids based on a target density (specifying `k_grid: X Y Z` in `[calculator.parameters]` is also possible!)
	- `density: 2` use a k-point density of at least 2 per $\require{mediawiki-texvc} \AA^{-3}$.
- `[calculator.basissets]`: Details on which basissets to use
	- `Si: light`: use _light default_ basis sets for silicon.

More details for each keyword can be found in the documentation.


!!! info
    For experimenting, testing, and rapid code-developing, it is often useful to use a force-field instead of an
    _ab initio_ calculator. For instance, one can use the Lennard-Jones (LJ) potential available within ASE to run all
    tutorials for LJ-Argon. Such calculations take only seconds, even on older laptops. The required geometry description
    and calculator settings are given below.

### LJ-Argon

??? info "Geometry in put file `geometry.in`"
    ```
    lattice_vector 0.0000000000000000 2.6299999999999999 2.6299999999999999
    lattice_vector 2.6299999999999999 0.0000000000000000 2.6299999999999999
    lattice_vector 2.6299999999999999 2.6299999999999999 0.0000000000000000
    atom 0.0000000000000000 0.0000000000000000 0.0000000000000000 Ar
    ```
??? info "`calculator` section for task input file"
    ```
    	[files]
		geometry:                      geometry.in

        [calculator]
        name:                          lj

        [calculator.parameters]
        # parameters for LJ Argon
        sigma:    3.405
        epsilon:  0.010325
        rc:       8.0
    ```
