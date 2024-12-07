"""Command-line interface for json2dir."""

import argparse
from pathlib import Path

from .core import json_to_dir, dir_to_json


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Convert between JSON and directory structure"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Convert JSON to directory structure
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert JSON to directory structure"
    )
    convert_parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="Input JSON file"
    )
    convert_parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=True,
        help="Output directory"
    )

    # Convert directory structure to JSON
    export_parser = subparsers.add_parser(
        "export",
        help="Convert directory structure to JSON"
    )
    export_parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="Input directory"
    )
    export_parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=True,
        help="Output JSON file"
    )

    args = parser.parse_args()

    if args.command == "convert":
        json_to_dir(args.input, args.output)
        print(f"Created directory structure in {args.output}")
    elif args.command == "export":
        dir_to_json(args.input, args.output)
        print(f"Created JSON structure in {args.output}")


if __name__ == "__main__":
    main()
