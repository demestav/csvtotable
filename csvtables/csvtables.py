# -*- coding: utf-8 -*-
"""csvtotext 0.1.0."""
import argparse
import csv
import pathlib


class CSVTable:
    """Manage CSV data."""

    def __init__(
        self, text_stream, compact=False, delimiter=",",
    ):
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
        # for row in zip(*enabled_columns):
        #     for col in row:

    def find_max_width(self, headers, body):
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
            md_entry = f" {entry}{' '*(width-len(entry))} |"
        else:
            md_entry = f" {entry} |"

        if prepend:
            md_entry = f"|{md_entry}"
        return md_entry


class CSVColumn:
    """Manage a CSV column."""

    def __init__(self, header):
        self.header = header
        self._truncate = None
        self._data = []
        self.width = len(self.header)
        self.enabled = True
        self.padding = 1

    @property
    def truncate(self):
        return self._truncate

    @truncate.setter
    def truncate(self, width=None):
        if width:
            width = max(len(self.header) + 2, width)
        self._truncate = width

    def setup_width(self):
        for d in self._data:
            if len(d) > self.width:
                self.width = len(d)


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
    parser.add_argument("-d", nargs=1)

    args = parser.parse_args()
    csv_fn = pathlib.Path(args.csv_file)
    csv_file = open(csv_fn, "r")

    csv_table = CSVTable(csv_file, args.d[0])
    text_table = csv_table.generate_table()
    csv_file.close()
    print(text_table)  # noqa: T001


if __name__ == "__main__":
    cli()
