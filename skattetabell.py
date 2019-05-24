import csv


class RangeDict(dict):
    def __getitem__(self, item):
        if type(item) != range:  # or xrange in Python 2
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError('Key not found in dict')
        else:
            return super().__getitem__(item)


def fetch_tax_table(csv_file, tax_year, tax_rate, column):
    assert(type(tax_year) is int and type(tax_rate) is int and type(column) is int)

    if tax_year > 2019 or tax_year < 2016:
        raise Exception('Tax year is not in table')
    if tax_rate < 29 or tax_rate > 40:
        raise Exception('Invalid tax rate (must be between 29 and 40 inclusive)')
    if column < 1 or column > 6:
        raise Exception('Invalid column (min 1, max 6)')

    tax_table = RangeDict()

    with open(csv_file, 'r', newline='') as f:
        csv_reader = csv.DictReader(f, delimiter=';')
        line = next(csv_reader)
        while line and int(line['Ar']) >= tax_year and int(line['Tabellnr']) <= tax_rate:
            if int(line['Ar']) == tax_year and int(line['Tabellnr']) == tax_rate:
                lower = int(line['Inkomst fr.o.m.'])
                upper = int(line['Inkomst t.o.m.'])
                tax_table[range(lower, upper + 1)] = int(line['Kolumn %d' % column])
            line = next(csv_reader)

    return tax_table


def main():

    table_file = 'tabeller.csv'

    tax_year = int(input('Input tax year: '))
    tax_rate = int(input('Input tax table (your tax rate rounded to nearest whole number): '))
    column = int(input('Which tax column do you belong to? '))

    print('\nFetching your tax table...')
    tax_table = fetch_tax_table(table_file, tax_year, tax_rate, column)
    print('Done!\n')

    new_income = True
    new_table = False
    while new_income:
        if new_table:
            tax_year = int(input('Input tax year: '))
            tax_rate = int(input('Input tax table (your tax rate rounded to nearest whole number): '))
            column = int(input('Which tax column do you belong to? '))

            print('\nFetching your tax table...')
            tax_table = fetch_tax_table(table_file, tax_year, tax_rate, column)
            print('Done!\n')

        income = int(input('Input desired income: '))

        print('Looking up tax for %d income...' % income)
        tax = tax_table[income]
        print('Done')

        print('Your income after tax is %d kr\n' % (income - tax))

        n_i = input("Input another income? (y/n) ").lower()

        while n_i != 'y' and n_i != 'n':
            n_i = input("Incorrect reply! Input another income? (y/n) ").lower()

        if n_i == 'y':
            new_income = True
            n_t = input("Want a new tax table? (y/n) ").lower()
            while n_t != 'y' and n_t != 'n':
                n_t = input("Incorrect reply! Want a new tax table? (y/n) ").lower()
            if n_t == 'y':
                new_table = True
            else:
                new_table = False
        else:
            new_income = False


if __name__ == "__main__":
    main()
