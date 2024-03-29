# csvtables
Converts a CSV formatted input to a readable table in text. The table is Markdown compatible.

## Installation
Install package using pip:
```
python -m pip install csvtables
```

## Usage
You can use the package directly in the terminal or by importing it in a python script.

### Command line interface
```
csvtables --help
```

Let's assume we have the following text file which is located in `tests/sample_data.csv` (reference: https://en.wikipedia.org/wiki/List_of_galaxies#Closest_galaxies):
```
Rank,Galaxy,Distance
1,Milky Way Galaxy,0
2,Canis Major Dwarf,0.025 Mly
3,Virgo Stellar Stream,0.030 Mly
4,Sagittarius Dwarf Elliptical Galaxy,0.081 Mly
5,Large Magellanic Cloud,0.163 Mly
6,Small Magellanic Cloud,0.197 Mly
```

The table is generated by running:
```
csvtables closest_galaxies.csv
```
and should produce the following output:
```
| Rank | Galaxy                              | Distance  |
|------|-------------------------------------|-----------|
| 1    | Milky Way Galaxy                    | 0         |
| 2    | Canis Major Dwarf                   | 0.025 Mly |
| 3    | Virgo Stellar Stream                | 0.030 Mly |
| 4    | Sagittarius Dwarf Elliptical Galaxy | 0.081 Mly |
| 5    | Large Magellanic Cloud              | 0.163 Mly |
| 6    | Small Magellanic Cloud              | 0.197 Mly |
```

### Running as a module
```
# example.py

from csvtables import csvtables
csv_file = open("tests/sample_data.csv", "r")
table = csvtables.CSVTable(csv_file)
print(table.generate_table())  # display the table to stdout
```
