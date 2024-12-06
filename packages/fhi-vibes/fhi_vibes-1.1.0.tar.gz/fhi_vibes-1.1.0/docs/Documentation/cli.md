# Command Line Interface (CLI)

FHI-vibes comes with a command line interface (CLI) for

- creating input files (`vibes  template`),
- informing about input and output files (`vibes info`),
- running calculations (`vibes run` and `vibes submit`),
- processing calculations (`vibes output`), and
- performing several other tasks like converting output files (`vibes utils`).

Practical examples for working with the CLI are found in the [tutorials](../Tutorial/0_intro.md). Each of the the sub-commands has its own `--help` for additional information.


## `vibes template`

Create template files

```
$ vibes template --help

Usage: vibes template [OPTIONS] COMMAND [ARGS]...

  provide template input files for tasks and workflows

Options:
  -h, --help         Show this message and exit.

Commands:
  calculator     Calculator templates: aims, lj
  configuration  Configuration templates: .vibesrc, .fireworksrc
  md             provide template input for MD simulation (default: NVE)
  phonopy        provide template input for phonopy workflow.
  relaxation     provide template input for relaxation workflow.
  slurm          provide template slurm settings
```

The templates are printed to screen and can be piped to a file with `| tee`, `>` or `>>`.

## `vibes info`

```
$ vibes info --help

Usage: vibes info [OPTIONS] COMMAND [ARGS]...

  inform about content of a file

Options:
  -h, --help  Show this message and exit.

Commands:
  anharmonicity   Compute sigmaA for trajectory dataset in FILE
  csv             show contents of csv FILE
  geometry        inform about a structure in a geometry input file
  greenkubo (gk)  Visualize heat flux and thermal conductivity
  md              inform about MD simulation in FILE
  netcdf          show contents of netCDF FILE
  phonopy         inform about a phonopy calculation based on the input FILE
  relaxation      summarize geometry optimization in FILE
  settings        write the settings in FILE *including* the configuration
  trajectory      print metadata from trajectory in FILE

```

## `vibes run`

```
vibes run --help

Usage: vibes run [OPTIONS] COMMAND [ARGS]...

  run a vibes workflow

Options:
  -h, --help  Show this message and exit.

Commands:
  md           run an MD simulation from FILE (default: md.in)
  phono3py     Run a phono3py calculation from FILE (default: phono3py.in)
  phonopy      run a phonopy calculation from FILE (default: phonopy.in)
  relaxation   run an relaxation from FILE (default: relaxation.in)
  singlepoint  run singlepoint calculations from FILE (default: aims.in)
```



## `vibes submit`

```
$ vibes submit --help

Usage: vibes submit [OPTIONS] COMMAND [ARGS]...

  submit a vibes workflow to slurm

Options:
  --dry
  -h, --help  Show this message and exit.

Commands:
  md           submit MD simulation from FILE (default: md.in)
  phono3py     Submit a phono3py calculation for FILE (default: phono3py.in)
  phonopy      submit a phonopy calculation from FILE (default: phonopy.in)
  relaxation   submit relaxation from FILE (default: relaxation.in)
  singlepoint  submit singlepoint calculations from FILE (default: aims.in)
```

## `vibes output`

```
$ vibes output --help

Usage: vibes output [OPTIONS] COMMAND [ARGS]...

  produce output of vibes workflow

Options:
  -h, --help  Show this message and exit.

Commands:
  greenkubo (gk)   Perform greenkubo analysis for dataset in FILE
  phono3py         Perform phono3py postprocess for trajectory in FILE
  phonopy          perform phonopy postprocess for trajectory in FILE
  trajectory (md)  write trajectory data in FILE to xarray.Dataset
```

## `vibes utils`

```
$ vibes utils --help

Usage: vibes utils [OPTIONS] COMMAND [ARGS]...

  tools and utilities

Options:
  -h, --help  Show this message and exit.

Commands:
  backup                backup FOLDER to TARGET
  create-samples        create samples from geometry in FILENAME
  force-constants (fc)  utils for working with force constants
  geometry              utils for manipulating structures (wrap, refine, etc.)
  hash                  create sha hash for FILE
  make-supercell        create a supercell of desired shape or size
  trajectory            trajectory utils
```
