# Armillaria phylogeny analysis

This repository contains scripts used for analysis as well as results and full report of the analysis. Full repository is available [here](https://github.com/jakubguzek/Armillaria-phylogeny).

## Report

Analysis report is available as report.pdf file within parent directory/ It contains theoretical introduction, methods and results with discussion.

## Scripts 

### Python 

Python scripts are contained within src/data_processing/ directory. 

#### download_proteomes.py

This script is useful for seni-automatic download of annotated genomic assemblies from NCBI ftp. 

```
usage: download_proteomes.py [-h] [-s [SPECIES ...]] [--outdir OUTDIR] [--species-index SPECIES_INDEX]

options:
  -h, --help            show this help message and exit
  -s [SPECIES ...], --species [SPECIES ...]
                        list of species binomial names
  --outdir OUTDIR       path to a directory where files shoul be saved.
  --species-index SPECIES_INDEX
                        path to a file with list of species names (one per line.)

```

#### taxmap.py

This python script is useful for getting a mapping from sequences ids to taxon ids. Output in tsv format.

```
usage: taxmap.py [-h] [-o OUTPUT] [--proteome-pattern PROTEOME_PATTERN] [--report-pattern REPORT_PATTERN] [dirs ...]

positional arguments:
  dirs                  list of directories containing proteome files and assebmly report files.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        where resulting mapping should be written.
  --proteome-pattern PROTEOME_PATTERN
                        pattern used for proteome file glob matching in a direcories
  --report-pattern REPORT_PATTERN
                        pattern used for report file glob matching in a direcories
```

#### filter_trees.py

Useful for filtering out files, that contain trees with low support.

```
usage: filter_trees.py [-h] [-t THRESHOLD] [-n] [input_trees ...]

positional arguments:
  input_trees           tree files in newick format

options:
  -h, --help            show this help message and exit
  -t THRESHOLD, --threshold THRESHOLD
                        minimal allowed support
  -n                    only print how many files passed filtering and exit.
```

Example usage:
```
./filter_trees.py ./dir_with_newick_files/*.nw -t 0.69

```

### Bash

Bash scripts are contained within scripts directory
 - `./get_seqids.sh` - get ids of sequences from fasta file that has ids are record names
 - `./compute_msa.sh` - compute msa
 - `./compute_trees.sh` - compute ML trees
 - `./create_blast_db.sh` - concatenate fasta files and change record names
 - `./unzip_proteomes.sh` - unzip many files in paralell
 - `./compute_consensus.sh` - compute consensus trees
 - `./compute_supertree.sh` - compute supertree


