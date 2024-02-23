"""This module contains common utilities that don't fit anywhere else for now."""
# Standard library imports
import io
from typing import Iterable, Optional, Hashable, Collection

# Third-party imports
import pandas as pd
import requests

# Local imports
from typings import FileLike


def parse_NCBI_summary(raw_summary: str) -> list[str]:
    return [line.strip("#") for line in raw_summary.split("\n") if len(line) > 1][1:]


def get_summary(url: str, sep: str = "\t") -> Optional[pd.DataFrame]:
    response = requests.get(url)
    if response.ok:
        raw_content = "\n".join(parse_NCBI_summary(response.text))
        return pd.read_csv(io.StringIO(raw_content), sep=sep, index_col=0)
    else:
        return None


def get_summaries(
    species_index: FileLike | Iterable[str], sep: str = ","
) -> dict[str, str]:
    """Returns a dict of taxon names and NCBI assembly summary tables as csv-formatted strings."""
    base_url = "https://ftp.ncbi.nlm.nih.gov/genomes/genbank/fungi/"

    if hasattr(species_index, "__iter__"):
        species = list(species_index) # type: ignore
    else:
        with open(species_index, "r") as file: # type: ignore
            species = [species.strip("\n") for species in file.readlines()]

    csv_formatted_summaries: dict[str, str] = {}
    for s in species:
        summary_table = get_summary(f"{base_url}/{s}/assembly_summary.txt")
        csv_formatted_summaries[s] = summary_table.to_csv(index=False, sep=sep)

    return csv_formatted_summaries


def choose_from(options: Collection[Hashable]) -> int:
    while True:
        for i, option in enumerate(options):
            print(f"{i}. {option}", end="\t")
            if (i + 1) % 5 == 0:
                print()
        print()
        try:
            choice = int(input(f'Choose one of the above [0-{len(options)-1}]: '))
        except ValueError:
            continue
        else:
            if choice in range(len(options)):
                break
            else:
                print("Ivalid value!")
    return choice
