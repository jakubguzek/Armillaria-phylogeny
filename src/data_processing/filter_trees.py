#!/usr/bin/env python
import argparse
import pathlib
import sys

import ete3

SCRIPT_NAME = pathlib.Path(__file__).name
THRESHOLD = 0.7


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_trees", type=str, nargs="*", help="tree files in newick format"
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=THRESHOLD,
        help="minimal allowed support",
    )
    parser.add_argument(
        "-n",
        action="store_true",
        help="only print how many files passed filtering and exit.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    tree_files = [pathlib.Path(file) for file in args.input_trees]
    file_doesnt_exist = [not dir.exists() for dir in tree_files]
    if any(file_doesnt_exist):
        which = tree_files[file_doesnt_exist.index(True)]
        print(f"{SCRIPT_NAME}: error: {which}: No such file or directory!")
        return 1
    is_a_directory = [dir.is_dir() for dir in tree_files]
    if any(is_a_directory):
        which = tree_files[is_a_directory.index(True)]
        print(f"{SCRIPT_NAME}: error: {which}: is not a directory!")
        return 1

    passed: list[pathlib.Path] = []
    for file in tree_files:
        tree = ete3.Tree(str(file))
        nodes = tree.traverse()
        if nodes is not None:
            above_threshold = [
                node.support / 100 > args.threshold
                for node in nodes
                if node.support != 1.0
            ]
            if all(above_threshold):
                passed.append(file)

    print(f"threshold: {args.threshold}")
    if args.n:
        print(f"{len(passed)} ({len(tree_files)})")
        return 0

    for file in passed:
        print(f"{file.parent / file.stem}.bestTree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
