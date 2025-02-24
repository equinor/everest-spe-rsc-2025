#!/usr/bin/env python
# coding: utf-8
"""Plot ensemble of 3D models

Example:
    python plot_ensemble.py -d EGG_MODEL_OPM.DATA -r 10 -n 60 60 7 -s 8 8 8 -o ensemble.pdf

Arguments:
    -d, --root-dir: Base directory with the models
    -r, --real: Number of realizations
    -n, --shape: Grid shape
    -s, --spacing: Grid spacing
    -o, --output: Output file

2024-12-20 - Created by: Rodolfo Oliveira
"""


import argparse
import matplotlib.pyplot as plt
from plot_model import read_grid_df, plot_grid_voxel
from res2df import ResdataFiles
import pathlib
import glob


def create_parser():
    parser = argparse.ArgumentParser(description='Plot ensemble of 3D models')
    parser.add_argument('-d', '--root-dir', help='Base directory with the models', required=True)
    parser.add_argument('-b', '--batch', help='Batch number', type=int, default=0)
    parser.add_argument('-r', '--real', help='Number of realizations', type=int, required=True)
    parser.add_argument('-n', '--shape', help='Grid shape', nargs=3, type=int, required=True)
    parser.add_argument('-s', '--spacing', help='Grid spacing', nargs=3, type=float, required=True)
    parser.add_argument('-o', '--output', help='Output file', default='ensemble.pdf')

    return parser


def get_base_cases(root_dir, nreal, nbatch=0, extension=".DATA"):
    """Get the base cases for the ensemble of models.

    Parameters
    ----------
    root_dir : str
        Root directory with the models.
    nreal : int
        Number of realizations.
    nbatch : int, optional
        Batch number, by default 0.
    extension : str, optional
        Extension of the files, by default ".DATA". 

    Returns
    -------
    files : list
        List with the paths of the base cases
    """
    files = []
    for ireal in range(nreal):
        runpath = pathlib.Path(root_dir) \
            / f"batch_{nbatch}" \
            / f"geo_realization_{ireal}" \
            / f"simulation_{ireal}"
        
        files.append(glob.glob(str(runpath) + f"/**/*{extension}", recursive=True)[0])

    return files


def main():
    parser = create_parser()
    args = parser.parse_args()

    root_dir = args.root_dir
    nreal = args.real
    nbatch = args.batch
    grid_shape = tuple(args.shape)
    grid_spacing = args.spacing

    files_list = get_base_cases(root_dir, nreal, nbatch)

    fig, ax = plt.subplots(
        1, 10,
        figsize=(10, 1), 
        subplot_kw={"projection":'3d'}
    )
    
    ax = ax.flatten()

    for i, ifile in enumerate(files_list):
        resdata_files = ResdataFiles(ifile)
        grid_df = read_grid_df(resdata_files)
        
        plot_grid_voxel(ax[i], grid_df, grid_shape, grid_spacing)

    fig.savefig(args.output, pad_inches=0, dpi=600)


if __name__ == '__main__':
    main()