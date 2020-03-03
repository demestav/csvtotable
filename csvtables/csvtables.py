# -*- coding: utf-8 -*-
"""csvtotext 0.1.0."""
import argparse
import csv
import pathlib


class CSVTable:
    """Manage CSV data."""

    def __init__(self, text_stream, compact=False, delimiter=",", truncate=[]):
        self.text_stream = text_stream
        self._csv_reader = csv.reader(text_stream, delimiter=delimiter)
        # Create the columns
        header_line = next(self._csv_reader)
        self.columns = [CSVColumn(h) for h in header_line]
        self.compact = compact

        # Load data to columns
        for row in self._csv_reader:
            for col_obj, row_col_val in zip(self.columns, row):
                col_obj._data.append(row_col_val)

        # Setup column width
        for col in self.columns:
            col.setup_width()

        # Setup column truncate
        for col_truncate in truncate:
            self.columns[col_truncate[0]].truncate = col_truncate[1]

    @property
    def headers(self):
        return [c.header for c in self.columns]

    @headers.setter
    def headers(self, headers):
        # Check correct headers number
        if len(headers) != len(self.columns):
            raise ValueError(
                "Number of headers should be the same as number of columns"
            )
        for index, header in enumerate(headers):
            self.columns[index].header = header

    def generate_table(self):
        enabled_columns = list(filter(lambda c: c.enabled, self.columns))
        # Header
        table_text = ""
        first = True
        for col in enabled_columns:
            table_text += self.decorate_entry(
                col.header, width=col.width, prepend=first
            )
            first = False

        # Seperator
        table_text += "\n"
        first = True
        for col in enabled_columns:
            table_text += self.decorate_entry(
                "-" * col.width, width=None, prepend=first
            )
            first = False

        # Data
        enabled_cols_data = [c._data for c in enabled_columns]
        first = True
        for cols in zip(*enabled_cols_data):
            first = True
            table_text += "\n"
            for index, col in enumerate(cols):
                table_text += self.decorate_entry(
                    col, width=enabled_columns[index].width, prepend=first
                )
                first = False
        return table_text

    def decorate_entry(self, entry, width=None, prepend=False):
        """Convert a value into a table cell.

        Args:
            entry: The value to decorate
            width: Final size of the table cell in characters
            prepend: Prepend table border character

        Returns:
            Decorated table cell
        """
        if width:
            md_entry = f" {entry[:width]}{' '*(width-len(entry))} |"
        else:
            md_entry = f" {entry} |"

        if prepend:
            md_entry = f"|{md_entry}"
        return md_entry

    def calculate_size(self):
        """Calculate the size of the resulting table in characters.

        For each column add the width + 2 for padding + 1 for the horizontal seperator.
        The total width is the columns width + 1 for the newline +1 for the final seperator.
        The total height is the number of data rows + 1 for seperator + 1 for header.
        The size in characters is the product of width and height.

        Returns:
            size in characters
        """
        enabled_columns = list(filter(lambda c: c.enabled, self.columns))
        enabled_columns_width_list = [c.width + 3 for c in enabled_columns]
        total_width = sum(enabled_columns_width_list) + 2  # Include new line
        table_height = len(enabled_columns[0]._data) + 2  # Include header and separator
        size_in_characters = total_width * table_height
        return size_in_characters


class CSVColumn:
    """Manage a CSV column."""

    def __init__(self, header):
        self.header = header
        self._truncate = None
        self._data = []
        self._max_width = 0
        self.enabled = True
        self.padding = 1

    @property
    def truncate(self):
        return self._truncate

    @property
    def width(self):
        return self._max_width if not self._truncate else self._truncate

    @truncate.setter
    def truncate(self, width=None):
        if width:
            width = max(len(self.header) + 2, width)
        self._truncate = width

    def setup_width(self):
        header_max_width = len(self.header)
        data_max_width = len(max(self._data, key=len))
        self._max_width = max(header_max_width, data_max_width)


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
    parser.add_argument("-d", "--delimiter", nargs=1, help="Define the delimiter")
    parser.add_argument(
        "-t",
        "--truncate",
        nargs=2,
        type=int,
        metavar=("column", "max_length"),
        action="append",
    )

    args = parser.parse_args()
    csv_fn = pathlib.Path(args.csv_file)
    csv_file = open(csv_fn, "r")

    if args.delimiter:
        delimiter = args.delimiter[0]
    else:
        delimiter = ","

    if args.truncate:
        truncate = args.truncate
    else:
        truncate = []

    csv_table = CSVTable(csv_file, delimiter=delimiter, truncate=truncate)
    text_table = csv_table.generate_table()
    csv_file.close()
    print(text_table)  # noqa: T001


if __name__ == "__main__":
    cli()
