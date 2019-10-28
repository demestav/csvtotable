# csvtomd
Converts a CSV formatted input to markdown table. It supports human friendly output as well!

## Usage
Import `convert_table` to your project and call it with a CSV formatted iterable. This can be a file or a `StringIO` object. It takes an optional argument `human_readable` (default=`False`) which will return a nicer formatted table.

### Example:
```
# example.py
import io
from csvtomd.csvtomd import convert_table
with open("example.csv", "r") as f:
    data = f.read()
markdown_table_string = convert_table(io.StringIO(data))
```