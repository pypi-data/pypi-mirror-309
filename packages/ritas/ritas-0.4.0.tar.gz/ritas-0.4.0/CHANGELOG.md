<!-- markdownlint-configure-file {"MD024": { "siblings_only": true } } -->
# RITAS Changelog

## ritas 0.4.0 Release (19 Nov 2024)

### API Changes

### New Features

- Require `rasterio>=1.4.0` due to `rasterize` API usage with GeoTIFF output.

### Bug Fixes

- Rectify input to EPSG:26915 (UTM Zone 15N) (#29).

## ritas 0.3.0 Release (28 May 2024)

### API Changes

- Depend on `rasterio` for IO support.
- Standardize log generation via `ritas.LOG`.

### New Features

- Added `--swath-width` or `-w` CLI switch to specify a width (#19).
- Support GeoTIFF output (#14).
- Support Shapefile for RITAS input.

### Bug Fixes

- Corrected the module version detection string.

## ritas 0.2.0 Release (23 Feb 2024)

An initial release with some viable functionality.  This library continues to
be in active development.

## ritas 0.1.1 Release (20 Feb 2024)

Hopefully a clean release ready for pypi and conda-forge.  Infrastructure
improvements with this release.

## ritas 0.1.0 Release (19 Feb 2024)

Initial project release, with a soon followup to release to PyPI and eventually
conda-forge.

### API Changes

None.

### New Features

None.

### Bug Fixes

None.
