import csv


class RangeDict(dict):
    def __getitem__(self, item):
        if type(item) != range:  # or xrange in Python 2
            for key in self:
                if item in key:
                    return self[key]
                raise KeyError(str(key))
        else:
            return super().__getitem__(item)


def fetch_tax_table(csv_file, tax_year, tax_rate, column):
    assert(type(tax_year) is int and type(tax_rate) is int and column)
    with open(csv_file, 'r', newline='') as f:
        csv_reader = csv.DictReader(f, delimiter=';')



