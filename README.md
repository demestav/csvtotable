# csvtotable
Converts a CSV formatted input to a readable table in text. The table is Markdown compatible.

## Usage
Import `convert_table` to your project and call it with a CSV formatted iterable. This can be a file or a `StringIO` object. Passing `compact=True` argument will remove all the unnecessary whitespace from the output, producing a smaller size but less readable table.

### Example:
`names.csv`:
```
name,surname
Jane,Doe
John,Doe
```

```
# example.py
import io
from csvtotable.csvtotable import convert_table
with open("example.csv", "r") as f:
    data = f.read()
markdown_table_string = convert_table(io.StringIO(data))
```