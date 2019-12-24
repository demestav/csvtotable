# -*- coding: utf-8 -*-
"""csvtotext 0.1.0."""
import argparse
import csv
import pathlib


def convert_table(csv_dict, compact=False):
    """Convert csv data to easy to read table (md compatible).

    Args:
        csv_dict: file-like object that contains CSV data
        compact: remove all whitespace

    Returns:
        CSV table text

    """
    csv_reader = csv.DictReader(csv_dict)
    headers = csv_reader.fieldnames
    csv_data = list(csv_reader)

    if not compact:
        col_max = find_max_width(headers, csv_data)
    else:
        col_max = {k: None for k in headers}

    # Header
    md_header = ""
    md_header = decorate_entry(headers[0], width=col_max[headers[0]], prepend=True)
    sep_length = col_max[headers[0]] if not compact else len(headers[0])
    md_separator = decorate_entry("-" * sep_length, prepend=True)
    for h in headers[1:]:
        md_header += decorate_entry(h, width=col_max[h])
        sep_length = col_max[h] if not compact else len(h)
        md_separator += decorate_entry("-" * sep_length, width=None)

    # Data
    md_data = ""
    for d in csv_data:
        first = True
        for h, value in d.items():
            md_data += decorate_entry(value, width=col_max[h], prepend=first)
            first = False
        md_data += "\n"

    md_content = md_header + "\n" + md_separator + "\n" + md_data
    return md_content


def find_max_width(headers, body):
    """Find the maximum length of each column, taking into account both the header and the table data.

    Args:
        headers: List of the column headers
        body: List of the table data

    Returns:
        A map between header and maximum width
    """
    col_max = {k: len(k) for k in headers}
    for row in body:
        for header, value in row.items():
            if len(value) > col_max[header]:
                col_max[header] = len(value)
    return col_max


def decorate_entry(entry, width=None, prepend=False):
    """Convert a value into a table cell.

    Args:
        entry: The value to decorate
        width: Final size of the table cell in characters
        prepend: Prepend table border character

    Returns:
        Decorated table cell
    """
    if width:
        md_entry = f" {entry}{' '*(width-len(entry))} |"
    else:
        md_entry = f" {entry} |"

    if prepend:
        md_entry = f"|{md_entry}"
    return md_entry


def cli():
    """Handle arguments from command line."""
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=str, help="CSV file to convert.")
    parser.add_argument(
        "-c",
        "--compact-format",
        action="store_true",
        help="Remove unnecessary whitespace (more compact output but less readable)",
    )

    args = parser.parse_args()

    csv_fn = pathlib.Path(args.csv_file)
    csv_file = open(csv_fn, "r")

    csv_table = convert_table(csv_file, args.compact_format)
    print(csv_table)  # noqa: T001


if __name__ == "__main__":
    cli()
