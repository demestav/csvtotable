from csvtables import __version__
from csvtables import csvtables


def test_version():
    assert __version__ == "0.2.0"


def test_find_max_width():
    headers = ["a", "b", "c"]
    body = [{"a": "1", "b": "123", "c": "12345"}]
    col_max_width = csvtables.find_max_width(headers, body)
    assert col_max_width["a"] == 1
    assert col_max_width["b"] == 3
    assert col_max_width["c"] == 5
