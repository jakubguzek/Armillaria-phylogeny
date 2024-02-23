#!/usr/bin/env python
import argparse
import pathlib
import sys
from typing import Optional

SCRIPT_NAME = pathlib.Path(__file__).name
PROTEOME_FILENAME_PATTERN = "*protein.faa"
REPORT_FILENAME_PATTERN = "*assembly_report.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dirs",
        type=str,
        nargs="*",
        help="list of directories containing proteome files and assebmly report files.",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="where resulting mapping should be written."
    )
    parser.add_argument(
        "--proteome-pattern",
        type=str,
        default=PROTEOME_FILENAME_PATTERN,
        help="pattern used for proteome file glob matching in a direcories",
    )
    parser.add_argument(
        "--report-pattern",
        type=str,
        default=REPORT_FILENAME_PATTERN,
        help="pattern used for report file glob matching in a direcories",
    )
    return parser.parse_args()


def get_accesions(proteome_file: pathlib.Path) -> list[str]:
    accesions = []
    with open(proteome_file, "r") as file:
        for line in file.readlines():
            if line.startswith(">"):
                accesions.append(line.split(" ")[0].strip(">"))
    return accesions


def get_taxid(report_file: pathlib.Path) -> Optional[str]:
    taxid = None
    with open(report_file, "r") as file:
        for line in file.readlines():
            if line.startswith("# Taxid:"):
                taxid = line.split(" ")[-1].strip()
                break
    return taxid


def main() -> int:
    args = parse_args()
    
    directories = [pathlib.Path(dir) for dir in args.dirs]
    directory_doesnt_exist = [not dir.exists() for dir in directories]
    if any(directory_doesnt_exist):
        which = directories[directory_doesnt_exist.index(True)]
        print(f"{SCRIPT_NAME}: error: {which}: No such file or directory!")
        return 1
    is_not_a_directory = [not dir.is_dir() for dir in directories]
    if any(is_not_a_directory):
        which = directories[is_not_a_directory.index(True)]
        print(f"{SCRIPT_NAME}: error: {which}: is not a directory!") 
        return 1

    taxid_accesion_map: dict[str, list[str]] = {}
    for dir in directories:
        proteome_file = list(dir.glob(args.proteome_pattern)).pop()
        report_file = list(dir.glob(args.report_pattern)).pop()
        taxid = get_taxid(report_file)
        accesions = get_accesions(proteome_file)
        if taxid is not None:
            taxid_accesion_map[taxid] = accesions
        else:
            print(f'[warning]: unable to get taxid for file {report_file} in {dir}.')

    if args.output:
        output_file = pathlib.Path(args.output)
        if output_file.is_dir():
            print(f"{SCRIPT_NAME}: error: {output_file} is a directory!")
            return 2

        if output_file.exists():
            print(f"[warning]: {output_file} exists!")
            choice = input("Do you wish to overwrite it? [Y/n]: ")
            if choice.lower() not in ["y", "yes"]:
                return 3
        with open(output_file, "w") as file:
            for taxid, accesions in taxid_accesion_map.items():
                for accesion in accesions:
                    file.write(f"{accesion}\t{taxid}\n")
        return 0

    for taxid, accesions in taxid_accesion_map.items():
        for accesion in accesions:
            print(f"{accesion}\t{taxid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
