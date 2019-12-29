# csvtables
Converts a CSV formatted input to a readable table in text. The table is Markdown compatible.

## Usage
Import `convert_table` to your project and call it with a CSV formatted iterable. This can be a file or a `StringIO` object. Passing `compact=True` argument will remove all the unnecessary whitespace from the output, producing a smaller size but less readable table.

### Example:
A sample data CSV file `tests/sample_data.csv` contains a list of fictional people.

#### Running from command line
`csvtables tests/sample_data.csv` will produce a table of the data

#### Running as a module
```
# example.py
from csvtables import csvtables
csv_file = open("tests/sample_data.csv", "r")
table_string = csvtables.convert_table(csv_file)
print(table_string) # display the table to stdout
```