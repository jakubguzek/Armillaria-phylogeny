# Standard library
import enum
import ftplib
import os
import pathlib
from typing import Hashable, Optional, Protocol

# Third-party libraries
import pandas as pd
import requests

# Local imports
import utils


class DataSource(enum.Enum):
    GenBank = "genbank"
    RefSeq = "refseq"


class OrganismGroup(enum.Enum):
    All = "all"
    Archaea = "archaea"
    Bacteria = "bacteria"
    Fungi = "fungi"
    Invertebrate = "invertebrate"
    Plant = "plant"
    Protozoa = "protozoa"
    VertebrateMammalian = "vertebrate_mammalian"
    VertebrateOther = "vertebrate_other"
    Viral = "viral"


class Proteome:
    _NCBI_FTP_ADDRESS = "ftp.ncbi.nlm.nih.gov"
    _BASE_URL = f"https://{_NCBI_FTP_ADDRESS}/genomes"

    def __init__(
        self,
        species: str,
        organism_group: OrganismGroup,
        source: DataSource = DataSource.GenBank,
    ) -> None:
        self._root_url = f"{self._BASE_URL}/{source.value}"
        self.species_binom = species.strip().replace(" ", "_").capitalize()
        self._organism_group = organism_group
        if organism_group == OrganismGroup.All:
            self._summary = utils.get_summary(
                f"{self._root_url}/assembly_summary_{source.value}.txt"
            )
        else:
            self._summary = utils.get_summary(
                f"{self._root_url}/{self._organism_group.value}/{self.species_binom}/assembly_summary.txt"
            )
        if self._summary is not None:
            self._assemblies = self._summary[
                self._summary.organism_name == species.replace("_", " ")
            ]
        else:
            raise ValueError("Unable to fetch summary!")

    def get_assemblies(self, assembly_id: Optional[str] = None) -> list[tuple[Hashable, pd.Series]]:
        columns = [
            "refseq_category",
            "species_taxid",
            "version_status",
            "release_type",
            "genome_rep",
            "asm_name",
            "asm_submitter",
            "ftp_path",
            "assembly_type",
            "assembly_level",
            "genome_size",
            "annotation_name",
            "annotation_date",
            "total_gene_count",
            "protein_coding_gene_count",
        ]
        if assembly_id is not None:
            return [(assembly_id, self._summary.loc[assembly_id][columns])]
        return [assembly for assembly in self._summary[columns].iterrows()]

    def pprint_assemblies(self, assembly_id: Optional[str] = None) -> None:
        print(f"\033[1mAssemblies for {self.species_binom.replace('_', ' ')}:\033[0m") #]]
        terminal_width, _ = os.get_terminal_size()
        max_col_width = int(terminal_width * 0.9)
        pd.set_option("display.max_colwidth", max_col_width - 28)
        for asm_id, details in self.get_assemblies(assembly_id=assembly_id):
            print("-" * max_col_width)
            print(f"{asm_id}:")
            print("-" * max_col_width)
            print(details)
        print("-" * max_col_width, end="\n\n")

    def download_assembly(
        self,
        assembly_id: str,
        root_dir: pathlib.Path,
        full: bool = False,
        verbose: bool = False,
    ):
        ftp_path = self._summary.loc[assembly_id, "ftp_path"].replace(
            "https://ftp.ncbi.nlm.nih.gov", ""
        )
        paths = []

        def recursive_ftp_crawl(ftp: ftplib.FTP, path: str):
            ftp.cwd(path)
            for name, facts in ftp.mlsd():
                if name.startswith("."):
                    continue
                if facts["type"] == "file":
                    paths.append(f"{path}/{name}")
                elif facts["type"] == "dir":
                    recursive_ftp_crawl(ftp, f"{path}/{name}/")

        with ftplib.FTP(self._NCBI_FTP_ADDRESS) as ftp:
            ftp.login()
            ftp.cwd(ftp_path)
            recursive_ftp_crawl(ftp, ftp_path)

        if not root_dir.exists():
            root_dir.mkdir()

        if not root_dir.is_dir():
            raise FileExistsError(f"{root_dir.name} is not a directory")

        for i, path in enumerate(paths):
            p = pathlib.Path(path)
            complete = i * 100 // len(paths)
            url = f"https://{self._NCBI_FTP_ADDRESS}{path}"
            if verbose:
                print(
                    f"\033[2KDownloading file {p.name}\nfrom: {url}\nWritting to {root_dir/p.name}",
                    flush=True,
                )  # ]
                print(
                    f"\033[2K\033[32m {'━' * complete}\033[31m{'━' * (100 - complete)}  \033[0m{i+1}/{len(paths)}",
                    end=" ",
                    flush=True,
                )  # ]]]]
                print("Downloading...", end="", flush=True)
            response = requests.get(url)
            if not response.ok:
                print(
                    f"\r\033[2K[\033[31m\033[1merror\033[0m] \033[1mFetching of file: {p.name} failed! (status code: {response.status_code})\033[0m"
                )  # ]]]]]]
                continue
            if verbose:
                print("\033[14D\033[0KWriting...", end="\r", flush=True)  # ]]
            with open(root_dir / p.name, "wb") as output_file:
                output_file.write(response.content)
        if verbose:
            print(
                f"\033[2K\033[32m {'━' * 100} \033[0m{len(paths)}/{len(paths)} Done!",
                end="\n",
            )  # ]]


def main() -> int:
    with open("./species.txt") as file:
        species = [name.strip() for name in file.readlines()]
    proteomes = [Proteome(name, OrganismGroup.Fungi) for name in species]
    for p in proteomes:
        assemblies = [asm_id for asm_id, _ in p.get_assemblies()]
        for i, asm_id in enumerate(assemblies):
            print(asm_id, end='\t')
            if i % 5 == 0:
                print()
        # p.download_assembly("GCA_030435635.1", pathlib.Path("./data/GCA_030435635.1"), verbose=True)
    return 0


if __name__ == "__main__":
    main()
