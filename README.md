# Automating GIS Processes II

Coursework, exercises, and notes for the **Automating GIS Processes** course (University of Helsinki), following the official course site: https://autogis-site.readthedocs.io/en/latest/

## Requirements

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda
- Python 3.10

## Setup

### 1. Install Miniconda/Conda

Follow the instructions for your OS in the [course guide](https://autogis-site.readthedocs.io/en/latest/course-info/installing-python.html):

- **Windows**: download the installer from the [Miniconda download page](https://docs.conda.io/en/latest/miniconda.html#windows-installers), run it, then verify with `conda --version` in an Anaconda Prompt.
- **macOS**: download the `.pkg` installer for your architecture from the [Miniconda download page](https://docs.conda.io/en/latest/miniconda.html#macos-installers), run it, then verify with `conda --version` in Terminal.
- **Linux (Debian/Ubuntu)**: no `.deb` package is available, so download and run the install script manually:

  ```bash
  curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  sha256sum Miniconda3-latest-Linux-x86_64.sh   # verify the hash against the download page
  sh Miniconda3-latest-Linux-x86_64.sh
  ```

  On RedHat-based distros, use `dnf`/`yum` to install `conda`; on Arch-based distros, use `pacman` to install `python-conda`.

### 2. Create the course environment

This repo includes an `environment.yml` (matching the [official one](https://github.com/Automating-GIS-processes/site/blob/main/environment.yml)) with all packages used in the course:

```yaml
name: autogis

channels:
  - conda-forge

dependencies:
  - python=3.10

  # JupyterLab
  - jupyterlab
  - jupyterlab-git

  # lessons
  - bokeh
  - folium
  - geojson
  - geopandas
  - geopy
  - matplotlib
  - osmnx
  - pyrosm
  - r5py
```

Create and activate it:

```bash
conda env create --file=environment.yml
conda activate autogis
```

> If you'd rather build the environment manually, create it from scratch and install packages one by one — always from the `conda-forge` channel to avoid dependency conflicts:
>
> ```bash
> conda create --name autogis
> conda activate autogis
> conda install -c conda-forge jupyterlab jupyterlab-git geopandas matplotlib geojson folium
> ```

### 3. Launch JupyterLab

From the repo's root folder:

```bash
jupyter lab
```

## Repository structure

```
.
├── environment.yml        # Conda environment definition
├── lesson-1/               # Shapely & geometry objects
├── lesson-2/               # Vector data I/O, GeoPandas, map projections
├── lesson-3/               # Geocoding, point-in-polygon, spatial join
├── lesson-4/               # Overlay analysis, aggregating & simplifying data
├── lesson-5/               # Static & interactive maps
├── lesson-6/               # OpenStreetMap data, network analysis
├── lesson-7/               # Raster data exploration & processing
├── final-assignment/       # Final project
└── README.md
```

Adjust the folder names above to match your actual notebook/exercise structure.

## Course resources

- [Course site](https://autogis-site.readthedocs.io/en/latest/)
- [Course GitHub repository](https://github.com/Automating-GIS-processes/site)
- [Grading criteria](https://autogis-site.readthedocs.io/en/latest/course-info/grading.html)

## License

See the course's [License and Terms of Use](https://autogis-site.readthedocs.io/en/latest/course-info/license.html).
