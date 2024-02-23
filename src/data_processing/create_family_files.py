#!/usr/bin/env python
import argparse
import pathlib
import sys
from numpy import repeat

import pandas as pd
from Bio import SeqIO

SCRIPT_NAME = pathlib.Path(__file__).name


def parse_args() -> argparse.Namespace:
    raise NotImplementedError


def get_cluster_sequence_map(clusters: pd.DataFrame, sequences_file: pathlib.Path):
    records = []
    with open(sequences_file, "r") as file:
        for record in SeqIO.parse(file, "fasta"):
            records.append((record.id, str(record.seq)))
    df = pd.DataFrame(records, columns=["seqid", "sequence"])
    return df


def main() -> int:
    representative = pd.read_csv(
        "./data/clusters_with_paralogs.tsv", sep="\t", header=None, names=["cluster"]
    )
    clusters = pd.read_csv(
        "./data/clusterdb_cluster.tsv",
        sep="\t",
        header=None,
        names=["cluster", "seqid"],
    )
    tax_mapping = pd.read_csv(
        "./data/tax_mapping.tsv", sep="\t", header=None, names=["seqid", "taxid"]
    )
    species_taxid = pd.read_csv("./species_taxid_map.tsv", sep="\t")

    representative = pd.merge(representative, clusters, on="cluster")
    sequences_file = pathlib.Path("./data/database.fasta")
    sequences = get_cluster_sequence_map(representative, sequences_file)
    representative = pd.merge(representative, sequences, on="seqid")
    representative = pd.merge(representative, tax_mapping, on='seqid')
    representative = pd.merge(representative, species_taxid, on='taxid')
    representative["name"] = representative["name"].str.replace(" ", "_")
    for name, cluster in representative.groupby("cluster"):
        s = ""
        for _, row in cluster.iterrows():
            s += f">{row['name']}-{row['seqid']}\n{row['sequence']}\n"
        with open(f"./data/protein_families_with_paralogs/{name}.fasta", "w") as file:
            file.write(s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
