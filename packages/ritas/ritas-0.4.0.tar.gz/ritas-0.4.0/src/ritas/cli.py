"""
Command line interface for RITAS.

This tool is used to convert an input file with yield monitor data to an output
grid file.

"""

import logging
from pathlib import Path

import click

from ritas import LOG, ColNames
from ritas.workflows import simple_workflow


@click.command(help=__doc__)
@click.option(
    "--input",
    "-i",
    "infile",
    type=click.Path(exists=True, path_type=Path),
    required=True,
)
@click.option(
    "--swath-width",
    "-w",
    "swath_width",
    type=float,
    default=None,
    help="Width (m) of the swath, over-riding what is in the input file.",
)
@click.option(
    "--output",
    "-o",
    "outfile",
    type=click.Path(exists=False, path_type=Path),
    required=True,
)
@click.option(
    "--mass-field",
    "-m",
    "mass_field",
    type=str,
    default=ColNames.MASS,
)
@click.option(
    "--swath-field",
    "-s",
    "swath_field",
    type=str,
    default=ColNames.SWATH,
)
@click.option(
    "--distance-field",
    "-d",
    "distance_field",
    type=str,
    default=ColNames.DISTANCE,
)
def main(**kwargs: dict) -> None:
    """Run the command line interface for ritas."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    infile = kwargs.pop("infile")
    outfile = kwargs.pop("outfile")
    LOG.info("I am about to process %s -> %s", infile, outfile)
    simple_workflow(infile, outfile, **kwargs)
