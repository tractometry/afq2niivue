# afq2niivue

A Marimo notebook for visualizing white matter fiber bundles from diffusion MRI tractography using NiiVue.

## Usage

```
VOLUME_PATH=brain.nii.gz TRX_PATH=tracts.trx marimo run viewer.py
```

Where:
- `VOLUME_PATH` is the path to a T1-weighted anatomical image (.nii.gz)
- `TRX_PATH` is the path to a TRX tractography file containing fiber bundles

## Installation

```
pip install marimo
```

All other dependencies are installed automatically by marimo's sandbox.

## About

This notebook reads a TRX tractography file and lets you interactively explore individual fiber bundles overlaid on a T1-weighted anatomical image. Select bundles using checkboxes to visualize one or more brain regions at a time.

Built with [NiiVue](https://github.com/niivue/niivue) by Chris Rorden and [ipyniivue](https://github.com/niivue/ipyniivue). Based on the [NiiVue marimo notebooks](https://github.com/niivue/marimo-notebooks).