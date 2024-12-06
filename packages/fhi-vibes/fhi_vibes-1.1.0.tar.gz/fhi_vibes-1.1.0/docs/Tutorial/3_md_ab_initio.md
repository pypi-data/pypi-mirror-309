# _ab initio_ Molecular Dynamics

!!! info
	We will now introduce _ab initio_ Molecular Dynamics simulations where the atomic forces come from a first-principles code. We will use `FHI-aims` as this calculator in the following. We assume:

	- You are familiar with running MD simulations in a different context and are here to learn how to run MD with `FHI-vibes`.
	- You are familiar with running `FHI-aims` calculations.
	- Optionally: You are familiar with running `FHI-aims` calculations on a workstation or computing cluster.

_Ab initio_ molecular dynamics simulations are MD simulations where the forces are computed from first principles, e.g., using density functional theory (DFT) with LDA or GGA xc-functional in the Born-Oppenheimer approximation. Thus,

$$
\begin{align}
\mathcal V ({\bf R}) = E_{\rm tot}^{\rm DFT} ({\bf R})~,
\label{eq:PES}
\end{align}
$$

where the potential energy $\mathcal V({\bf R})$ of a given atomic configuration $\bf R$ is given by the total energy  $E_{\rm tot}^{\rm DFT} ({\bf R})$ of the electronic and nuclear system computed for this structure[^footnote1].
Given that a single DFT calculations is required for each step of the trajectory, MD calculations are computationally more expensive than the calculations performed in the other tutorials.

## Setting up ab initio MD

We will use an 8 atoms supercell of silicon with LDA xc-functional as previously in the tutorial on geometry optimization and phonon calculations. You can reuse the structure from [the tutorial on geometry optimization](1_geometry_optimization.md), as well as the calculator setup.

```
cp ../path/to/relaxation/geometry.in.next_step geometry.in.primitive
```

Create a supercell with 8 atoms:

```
vibes utils make-supercell geometry.in.primitive -n 8
mv geometry.in.primitive.supercell_8 geometry.in.supercell
```

To speed up the thermalization, we pre-thermalize the supercell by giving the kinetic energy corresponding to a temperature of $300\,{\rm K}$ with the following command:
```
vibes utils create-samples geometry.in.supercell -T 300
mv geometry.in.supercell.0300K geometry.in
```

### Prepare `md.in`

Before we can run the MD, we need to create an input file. To this end, copy the calculator section [for LDA-Si](0_intro.md#lda-silicon) to a file called `md.in`. Next, we use the CLI command `template` to add settings for performing a NVT simulation:

```
vibes template md --nvt >> md.in
```

??? info "The generated `md.in`"

    ```
    [calculator]
    name:                          aims

    [calculator.parameters]
    xc:                            pw-lda

    [calculator.kpoints]
    density:                       2

    [calculator.basissets]
    default:                       light

    [calculator.socketio]
    port:                          12345

    [md]
    driver:                        Langevin
    timestep:                      1
    maxsteps:                      1000
    compute_stresses:              False
    workdir:                       md

    [md.kwargs]
    temperature:                   300
    friction:                      0.02
    logfile:                       md.log
    ```

We suggest to add and/or adjust the following  keywords:

```
[md]
timestep:                      4
maxsteps:                      2500
compute_stresses:              10

[files]
geometry:                      geometry.in
primitive:                     geometry.in.primitive
supercell:                     geometry.in.supercell
```

The `timestep` can be increased to $4\,{\rm fs}$ for Silicon at $300\,{\rm K}$. With `maxsteps: 2500` we will run a total of 2500 MD steps, i.e., $10\,{\rm ps}$ simulation time. **The total simulation time depends on the system and the quantity of interest!**`temperature` should be set to $300\,{\rm K}$, our target temperature.
The flag `compute_stresses` in the section `[md]` will make FHI-aims compute the _ab initio_ stress every 10 steps during the MD simulation. This will provide access to pressure.[^footnote2]
by inspecting the Adding `primitive: geometry.in.primitive` and `supercell: geometry.in.supercell` in the `[files]` section is not necessary to run the calculation. However, `vibes` will automatically attach this information to the trajectory so that it cannot get lost. This also makes life easier when post processing. For example, the displacements $\Delta {\bf R}_I(t)$ can only be properly calculated, when the reference supercell is known.

The final `md.in` should look like this:

```
[calculator]
name:                          aims

[calculator.parameters]
xc:                            pw-lda

[calculator.kpoints]
density:                       2

[calculator.basissets]
default:                       light

[calculator.socketio]
port:                          12345

[md]
driver =           Langevin
timestep =         4
temperature =      300
friction =         0.02
maxsteps =         2500
compute_stresses = 10

[files]
geometry:                      geometry.in
primitive:                     geometry.in.primitive
supercell:                     geometry.in.supercell
```

We are now ready to  run the simulation!

## Run a calculation

This step is similar to [before](2_phonopy.md#run-the-calculation), i.e., you run

```
vibes run md >> log.md &
```

??? info "`log.md"

    ```
    [vibes.run]    run MD workflow with settings from md.in

    [md]           driver: Langevin
    [md]           settings:
    [md]             type: molecular-dynamics
    [md]             md-type: Langevin
    [md]             timestep: 0.39290779153856253
    [md]             temperature: 0.02585199101165164
    [md]             friction: 0.02
    [md]             fix-cm: True
    [md]           ** /scratch/usr/becflokn/vibes/tutorial/3_md/ab_initio/si_8/md/trajectory.son does not exist, nothing to prepare
    [calculator]   Update aims k_grid with kpt density of 2 to [4, 4, 4]
    [calculator]   .. add `sc_accuracy_rho: 1e-06` to parameters (default)
    [calculator]   .. add `relativistic: atomic_zora scalar` to parameters (default)
    [calculator]   .. add `compensate_multipole_errors: False` to parameters (default)
    [calculator]   .. add `output_level: MD_light` to parameters (default)
    [calculator]   Add basisset `light` for atom `Si` to basissets folder.
    [calculator]   Calculator: aims
    [calculator]   settings:
    [calculator]     xc: pw-lda
    [calculator]     k_grid: [4, 4, 4]
    [calculator]     sc_accuracy_rho: 1e-06
    [calculator]     relativistic: atomic_zora scalar
    [calculator]     compensate_multipole_errors: False
    [calculator]     output_level: MD_light
    [calculator]     compute_forces: True
    [calculator]     compute_heat_flux: True
    [calculator]     use_pimd_wrapper: ('localhost', 12345)
    [calculator]     aims_command: run_aims
    [calculator]     species_dir: /scratch/usr/becflokn/vibes/tutorial/3_md/ab_initio/si_8/md/basissets
    [socketio]     Use SocketIO with host localhost and port 12345
    [backup]       /scratch/usr/becflokn/vibes/tutorial/3_md/ab_initio/si_8/md/calculations does not exists, nothing to back up.
    Module for Intel Parallel Studio XE Composer Edition (version 2019 Update 5) loaded.
    Module for Intel-MPI (version 2018.5) loaded.
    [md]           Step 1 finished, log.
    [md]           switch stresses computation off
    [md]           Step 2 finished, log.
    [md]           switch stresses computation off
    [md]           Step 3 finished, log.
    [md]           switch stresses computation off
    [md]           Step 4 finished, log.
    [md]           switch stresses computation off
    [md]           Step 5 finished, log.
    ...
    ```

For running on a cluster, see [additional remarks](0_singlepoint.md#submit-calculation-on-a-cluster).

## Postprocess

### Process the calculation

The data obtained at each time step will be written to the trajectory file `md/trajectory.son`. The CLI provides a tool to process the trajectory and create an `xarray.Dataset` from it. To this end, run

 ```
vibes output md md/trajectory.son
 ```

This command will create `trajectory.nc`, a dataset representation of the data contained in the MD trajectory saved as an `xarray.Dataset` to a NetCDF file. The included data can be viewed with

```
vibes info netcdf trajectory.nc
```

??? info "Output of `vibes info netcdf trajectory.nc`"

    ```
    <xarray.Dataset>
    Dimensions:              (I: 8, a: 3, b: 3, time: 2501)
    Coordinates:
      * time                 (time) float64 0.0 4.0 8.0 ... 9.996e+03 1e+04
    Dimensions without coordinates: I, a, b
    Data variables:
        positions            (time, I, a) float64 ...
        displacements        (time, I, a) float64 ...
        velocities           (time, I, a) float64 ...
        momenta              (time, I, a) float64 ...
        forces               (time, I, a) float64 ...
        energy_kinetic       (time) float64 ...
        energy_potential     (time) float64 ...
        stress               (time, a, b) float64 ...
        stress_kinetic       (time, a, b) float64 ...
        stress_potential     (time, a, b) float64 ...
        temperature          (time) float64 ...
        cell                 (time, a, b) float64 ...
        positions_reference  (I, a) float64 ...
        lattice_reference    (a, b) float64 ...
        pressure             (time) float64 ...
        pressure_kinetic     (time) float64 ...
        pressure_potential   (time) float64 ...
    Attributes:
        name:             trajectory
        system_name:      Si
        natoms:           8
        time_unit:        fs
        timestep:         4.000000000000006
        nsteps:           2500
        symbols:          ['Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si', 'Si']
        masses:           [28.085 28.085 28.085 28.085 28.085 28.085 28.085 28.085]
        atoms_reference:  {"pbc": [true, true, true],\n"cell": \n[[ 5.42906529316...
        atoms_primitive:  {"pbc": [true, true, true],\n"cell": \n[[-0.00000000000...
        atoms_supercell:  {"pbc": [true, true, true],\n"cell": \n[[ 5.42906529316...
        volume:           160.02034201861315
        raw_metadata:     {"MD": {\n  "type": "molecular-dynamics",\n  "md-type":...
        hash:             ff1410ec05dc89c85cf148670ecb05947a0066c8
    ```

### Inspect results

You can perform postprocessing of the pressure by [inspecting the trajectory dataset in `trajectory.nc`](../Documentation/output_files.md#trajectorync). Be aware that the simulation time is shorter when discarding the thermalization period.

??? info "reference pressure"
	For 8 atoms LDA-Silicon, you should get a potential pressure of $-0.61 \pm 0.06 {}$

[A more detailed introduction to postprocessing including example scripts is given in the next chapter.](3_md_postprocess.md)

## References
Running the calculation will take some time depending on the computer your working with. You find references [in our reference repository](https://gitlab.com/vibes-developers/vibes-tutorial-files/-/tree/master/3_molecular_dynamics/ab_initio). There you also find reference calculations for 64 and 216 atoms.

[^footnote1]: Note that a correct _ab initio_ MD requires also to choose the different numerical settings in the DFT calculation with care. For instance, the inherent incompleteness of the SCF cycle in Kohn-Sham DFT schemes can introduce a systematic error that introduces energy drifts and other unphysical effects. Choosing the correct convergence settings is an important aspect of performing _ab initio_ MD simulations and is highly materials specific. Devising a strategy on how to choose these settings goes beyond the scope of this tutorial.

[^footnote2]: We compute the stress only every 10th step because computing the stress is numerically more expensive in _ab initio_ than computing the atomic forces only. Since we know that consecutive samples generated during MD are highly correlated, we don't loose valuable information by computing this quantity not in every single step.
