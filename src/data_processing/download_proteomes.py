#!/usr/bin/env python
"""Script for downloading assembly and annotation data from NCBI."""
# Standard library imports
import argparse
import pathlib
import sys

from pandas.core.interchange.dataframe_protocol import enum

# Local imports
import utils
from proteome import Proteome, OrganismGroup

SCRIPT_NAME = pathlib.Path(__name__).name


def parse_arge() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--species", type=str, nargs="*", help="list of species binomial names"
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default=".",
        help="path to a directory where files shoul be saved.",
    )
    parser.add_argument(
        "--species-index",
        type=str,
        help="path to a file with list of species names (one per line.)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_arge()

    species = []
    if args.species_index:
        species_index_path = pathlib.Path(args.species_index)
        if not species_index_path.exists():
            print(
                f"{SCRIPT_NAME}: error: {species_index_path}: No such file or directory!"
            )
            return 1
        if species_index_path.is_dir():
            print(f"{SCRIPT_NAME}: error: {species_index_path} is a directory!")
            return 2
        with open(species_index_path) as file:
            species.extend([name.strip() for name in file.readlines()])

    if args.species:
        species.extend(args.species)

    outdir = pathlib.Path(args.outdir)

    proteomes = [Proteome(name, OrganismGroup.Fungi) for name in species]
    while True:
        chosen_assemblies = []
        for proteome in proteomes:
            assemblies = [asm_id for asm_id, _ in proteome.get_assemblies()]
            proteome.pprint_assemblies()
            c = utils.choose_from(assemblies)
            chosen_assemblies.append(assemblies[c])
        print(f"Chosen proteomes: {', '.join(chosen_assemblies)}")
        choice = input("Do you accept it? [Y/n]: ")
        if choice.lower() in ["y", "yes"]:
            break
    for i, proteome in enumerate(proteomes):
        proteome.download_assembly(
            chosen_assemblies[i], pathlib.Path(outdir / f"{proteome.species_binom}"), verbose=True
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
