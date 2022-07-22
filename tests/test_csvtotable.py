from io import StringIO

import pytest

from csvtables import csvtables


def test_find_max_width():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    assert csv_table.columns[0].width == 1
    assert csv_table.columns[1].width == 3
    assert csv_table.columns[2].width == 5


def test_column_truncate_table():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    csv_table.columns[1].truncate = 2
    csv_table.columns[2].truncate = 3

    assert (
        csv_table.generate_table()
        == """| a | b  | c   |
|---|----|-----|
| 1 | 12 | 123 |"""
    )


def test_table_output():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csvtable = csvtables.CSVTable(csv_string)
    assert (
        csvtable.generate_table()
        == """| a | b   | c     |
|---|-----|-------|
| 1 | 123 | 12345 |"""
    )


# | - | --- | ----- |
# | 1 | 123 | 12345 |
# """
#     )


def test_column_headers():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    assert len(csv_table.columns) == 3


def test_column_header_names():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    assert csv_table.columns[0].header == "a"
    assert csv_table.columns[1].header == "b"
    assert csv_table.columns[2].header == "c"


def test_class_header_names():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    headers = csv_table.headers
    assert headers[0] == "a"
    assert headers[1] == "b"
    assert headers[2] == "c"


def test_class_set_header_names_wrong_number():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    with pytest.raises(ValueError):
        csv_table.headers = ["only one"]


def test_class_set_header_names():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    csv_table.headers = ["d", "e", "f"]
    headers = csv_table.headers
    assert headers[0] == "d"
    assert headers[1] == "e"
    assert headers[2] == "f"


def test_column_truncate_alt():
    csv_string = StringIO("abcde,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    for col in csv_table.columns:
        assert col.truncate is None
    csv_table.columns[0].truncate = 20
    assert csv_table.columns[0].truncate == 20
    csv_table.columns[0].truncate = 2
    assert csv_table.columns[0].truncate == 5


def test_column_data():
    csv_string = StringIO("a,b,c\n1,123,12345\n678,901,234\n")
    csv_table = csvtables.CSVTable(csv_string)
    assert csv_table.columns[0]._data == ["1", "678"]
