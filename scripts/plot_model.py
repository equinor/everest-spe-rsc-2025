#!/usr/bin/env python
# coding: utf-8
"""Plot 3D model

Example:
    python plot_model.py -d EGG_MODEL_OPM.DATA -n 60 60 7 -s 8 8 8 -o model.pdf --show-wells --show-colorbar

Arguments:
    -d, --data: Path to the data file
    -n, --shape: Grid shape
    -s, --spacing: Grid spacing
    -o, --output: Output file
    --show-wells: Show wells
    --show-colorbar: Show colorbar

This script was originally developed by Mathias Nielsen, who kindly
shared it with us.

2024-12-20 - Modified by: Rodolfo Oliveira
2024-12-18 - Created by: Mathias Nielsen
"""


import argparse
import numpy  as np
import matplotlib.pyplot as plt
from res2df import ResdataFiles, grid, compdat


def create_parser():
    parser = argparse.ArgumentParser(description='Plot 3D model')
    parser.add_argument('-d', '--data', help='Path to the data file', required=True)
    parser.add_argument('-n', '--shape', help='Grid shape', nargs=3, type=int, required=True)
    parser.add_argument('-s', '--spacing', help='Grid spacing', nargs=3, type=float, required=True)
    parser.add_argument('-o', '--output', help='Output file', default='model.pdf')

    parser.add_argument('--show-wells', help='Show wells', action='store_true')
    parser.add_argument('--show-colorbar', help='Show colorbar', action='store_true')

    return parser


def read_well_df(resdata_files):
    """Read well data from resdata files and return a DataFrame with the
    COMPDAT data for each well.

    Parameters
    ----------
    resdata_files : ResdataFiles
        Resdata files.

    Returns
    -------
    well_df : pd.DataFrame
        DataFrame with the COMPDAT data for each well.
    """

    well_df = compdat.df(resdata_files)
    
    well_df = well_df.groupby(
        ["WELL", "I", "J"]).agg(
        K_MIN=("K1", "min"),
        K_MAX=("K1", "max")
    ).reset_index()

    return well_df


def read_grid_df(resdata_files):
    """Read grid data from resdata files and return a DataFrame with the
    GRID data.

    Parameters
    ----------
    resdata_files : ResdataFiles
        Resdata files.

    Returns
    -------
    grid_df : pd.DataFrame
        DataFrame with the GRID data.
    """

    grid_df = grid.df(resdata_files)

    return grid_df


def plot_grid_voxel(ax, grid_df, grid_shape, grid_spacing, show_colorbar=False):
    """Plot the grid as voxels.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Matplotlib axes.
    grid_df : pd.DataFrame
        DataFrame with the GRID data.
    grid_shape : tuple
        Grid shape.
    grid_spacing : tuple
        Grid spacing.

    Returns
    -------
    res : matplotlib.collections.Poly3DCollection
        Matplotlib Poly3DCollection.
    """

    grid_coords = np.indices(np.array(grid_shape) + 1, dtype=float)
    grid_coords[0] *= grid_spacing[0]
    grid_coords[1] *= grid_spacing[1]
    grid_coords[2] *= grid_spacing[2]

    grid_active = np.zeros(grid_shape, dtype=bool)
    grid_active[grid_df['I'] - 1, grid_df['J'] - 1, grid_df['K'] - 1] = True

    cmap = plt.get_cmap('viridis_r')
    norm = plt.Normalize(grid_df['PERMX'].min(), grid_df['PERMX'].max())
    rgba_colors = cmap(norm(grid_df['PERMX'].values))
    
    grid_colors = np.zeros(grid_shape + (4,))
    grid_colors[grid_df['I'] - 1, grid_df['J'] - 1, grid_df['K'] - 1] = rgba_colors

    res = ax.voxels(
        grid_coords[0], 
        grid_coords[1], 
        grid_coords[2],
        grid_active,
        facecolors=grid_colors,
        linewidth=0.5,
        zorder=10,
    )

    if show_colorbar:
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array(grid_df['PERMX'])
        plt.colorbar(
            sm,
            ax=ax,
            label='Permeability / mD',
            orientation='horizontal'
        )
    
    ax.set_aspect('equal')
    ax.view_init(
        elev=30, 
        azim=-90, 
        roll=0,
    )

    ax.axis('off')

    return res


def plot_wells(ax, well_df, grid_spacing):
    """Plot the wells.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Matplotlib axes.
    well_df : pd.DataFrame
        DataFrame with the COMPDAT data for each well.
    grid_spacing : tuple
        Grid spacing.
    """

    for i, well in well_df.iterrows():
        well_x = (well['I'] - 1 - 0.5) * grid_spacing[0]
        well_y = (well['J'] - 1 - 0.5) * grid_spacing[1]
        well_z1 = well['K_MIN'] * grid_spacing[2]
        well_z2 = well['K_MAX'] * grid_spacing[2]
        dz = well_z2 - well_z1
        well_z1 += dz
        well_z2 += dz

        ax.plot(
            [well_x, well_x], 
            [well_y, well_y],
            [well_z2, well_z1],
            linewidth=2,
            color='tab:blue' if well["WELL"].startswith("INJ") else 'tab:red',
            marker='v' if well["WELL"].startswith("INJ") else '^',
            markevery=[0],
            zorder=100_000,
        )
    
        ax.text(
            well_x,
            well_y,
            well_z2 + grid_spacing[2],
            f"{well['WELL']}", 
            zorder=100_000,
            color='black', 
            verticalalignment='bottom', 
            horizontalalignment='center', 
            alpha=1, 
            fontsize=6,
        )


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    
    data_file = args.data
    grid_shape = tuple(args.shape)
    grid_spacing = args.spacing

    resdata_files = ResdataFiles(data_file)

    fig, ax = plt.subplots(
        figsize=(10, 10), 
        subplot_kw={"projection":'3d'}
    )

    grid_df = read_grid_df(resdata_files)
    plot_grid_voxel(ax, grid_df, grid_shape, grid_spacing, args.show_colorbar)

    if args.show_wells:
        well_df = read_well_df(resdata_files)
        plot_wells(ax, well_df, grid_spacing)
    
    plt.axis('off')
    fig.savefig(args.output, pad_inches=0)
    # plt.show()
