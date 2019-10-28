import csv
import io


def convert_table(csv_dict, human_readable=False):

    csv_reader = csv.DictReader(csv_dict)
    headers = csv_reader.fieldnames

    if human_readable:
        all_data = list()
        col_max = {k: len(k) for k in headers}
        for row in csv_reader:
            for k, v in row.items():
                if len(v) > col_max[k]:
                    col_max[k] = len(v)
            all_data.append(row)
    else:
        col_max = {k: None for k in headers}
        all_data = [x for x in csv_reader]

    # Header
    md_header = ""
    md_header = decorate_entry(headers[0], width=col_max[headers[0]], first=True)
    sep_length = col_max[headers[0]] if human_readable else len(headers[0])
    md_separator = decorate_entry("-" * sep_length, first=True)
    for h in headers[1:]:
        md_header += decorate_entry(h, width=col_max[h])
        sep_length = col_max[h] if human_readable else len(h)
        md_separator += decorate_entry("-" * sep_length, width=None)

    # Data
    md_data = ""
    for d in all_data:
        first = True
        for h, value in d.items():
            md_data += decorate_entry(value, width=col_max[h], first=first)
            first = False
        md_data += "\n"

    md_content = md_header + "\n" + md_separator + "\n" + md_data
    return md_content


def decorate_entry(entry, width=None, first=False):
    if width:
        md_entry = f" {entry}{' '*(width-len(entry))} |"
    else:
        md_entry = f" {entry} |"

    if first:
        md_entry = f"|{md_entry}"
    return md_entry
