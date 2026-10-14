# CLAUDE.md

Coursework repo for **Automating GIS Processes** (University of Helsinki): https://autogis-site.readthedocs.io/en/latest/
Remote: `git@github.com:maggioniduffy/auto-gis.git`. The local folder was `CURSO-GIS` and is being renamed to `autogis`.

## Layout

- `lesson-N/` holds that lesson's notebooks, `data/` and `figs/`. Exercises sit in `lesson-N/Exercise-N` (or `exercise-N`).
- Lessons done so far: 1–4. Lessons 5–7 and the final assignment are still to do.
- `enviroment.yml` is the conda env definition (the filename is misspelled, and the README refers to `environment.yml`). Env name: `autogis`, conda-forge only.

## Conventions

- Work is in Jupyter notebooks. Edit them with NotebookEdit (or JSON-aware edits), never by plain string replacement over raw `.ipynb` JSON.
- Use relative paths in notebooks (e.g. `data/...`). Absolute paths break when the folder is moved or renamed. The saved outputs in `lesson-2/Geopandas: an introduction.ipynb` still show the old `CURSO-GIS` absolute path, which is cosmetic.
- Commit style is short and descriptive, e.g. "Add lesson 4 notebook, data and figs".
- Don't commit `__pycache__/` (already in `.gitignore`).

## Gotchas

- Dependencies come from conda-forge. Don't mix in pip installs for geospatial packages (geopandas, pyrosm, r5py, osmnx) unless needed.
- `lesson-2/data` is about 22 MB. Check size before adding more large files to `data/`.
