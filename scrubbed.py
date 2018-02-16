#!usr/bin/python3

import argparse
import sys
import os
import pprint

'''
import all transactions
import all categories and names
sort transactions into categories
get total transaction values for each category

use this to do budget after

'''

# :I this form of transaction is essentially a dictionary, but you
# :I might want to add functionality to it and it allows easy instantiation
# :I of transactional records


class Transaction(object):
    def __init__(self, date, entity, category, balance_sheet, amount):
        self.date = date
        self.entity = entity
        self.category = category
        self.balance_sheet = balance_sheet
        self.amount = amount

    def __repr__(self):
        retstr = ''
        retstr += 'Transaction('
        retstr += 'Date: {} '
        retstr += 'Entity: {} '
        retstr += 'Amount: {} '
        retstr += 'Origin: {} '
        retstr += 'Category: {})'
        retstr = retstr.format(self.date,
                               self.entity,
                               self.amount,
                               self.balance_sheet,
                               self.category)
        return retstr


class AccountReporter(object):
    def __init__(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument("-ingest",
                            default='ingest',
                            help="folder of files to ingest as transaction\
                            logs relative to script")
        parser.add_argument("-categories",
                            default='categories',
                            help="folder of files to ingest as category\
                            names with members relative to script")
        parser.add_argument("-save",
                            default='save',
                            help="save directory for reports")
        args = parser.parse_args(argv)
        self.ingest_dir = args.ingest
        self.categories_dir = args.categories
        self.save_dir = args.save
        self.transactions = []
        self.problem_transactions = []
        self.net_balance = 0
        self.net_expenditures = 0
        self.net_income = 0
        self.categories = {}
        self.ingest_files(self.categories_dir)

    def parse_categories(self, category_file):
        filename, fileext = os.path.splitext(category_file)
        self.categories[filename] = []
        with open(category_file, mode='r') as fo:
            for line in fo:
                '''
                line looks like this
                'mcdonalds\n'
                '''
                self.categories[filename].append(line.rstrip().lower())

    def ingest_files(self, path):
        if path not in os.listdir('.'):
            raise Exception('Ingest dir invalid {}'.format(path))
        os.chdir(path)
        # should this be a try:except?
        if not os.listdir('.'):
            raise Exception('Ingest dir empty {}'.format(path))
        for file in os.listdir('.'):
            if self.ingest_dir == path:
                self.parse_balance_sheet(file)
            if self.categories_dir == path:
                self.parse_categories(file)
        os.chdir('..')
        if self.problem_transactions:
            pprint.pprint(self.problem_transactions)
            # use a better way after debugging to display this?
            raise Exception('Problem records please fix')
        return 0
        # this got changed to a more generic ingest files func
        # :I ingest balance sheets from self.ingest_dir path,
        # :I updates self vars, most importantly self.transactions
        # :I returns 0 if success, some error if failure

    def parse_balance_sheet(self, balance_sheet):
        with open(balance_sheet, mode='r') as fo:
            for line in fo:
                '''
                line looks like this:
                'Feb 02, 2018\tSOBEYS LIQUOR #\t45.13\t\t$8,536.95'
                date,entity,debit,credit,balance
                '''
                fields = line.split('\t')
                if len(fields) >= 4:  # i dont want this magic number
                    date = fields[0]
                    entity = fields[1]
                    debit = fields[2]
                    credit = fields[3]
                else:
                    self.problem_transactions.append(line)
                    # this does not catch all problem cases at all :/
                    continue

                def convert_amount(amount):
                    if amount == '':
                        return 0
                    else:
                        return float(amount.replace(',', ''))

                credit = convert_amount(credit)
                debit = convert_amount(debit)

                date = date.rstrip().lstrip()
                entity = entity.rstrip().lstrip().lower()
                '''
                the format i am providing it in sometimes has white space on
                these vars left and right
                should  i figure out how to make this a date object so i can
                sort my transaction list by date?
                is this the right way of 'sanitizing' these inputs?
                '''
                for k, v in self.categories.items():
                    for name in v:
                        if name in entity:
                            category = k

                self.transactions.append(Transaction(
                    date,
                    entity,
                    category,
                    balance_sheet,
                    debit - credit))
                self.net_expenditures += debit
                self.net_income += credit
        # :I parses balance sheet from specified file path: balance_sheet
        # :I make sure to consider how to handle if the file path doesn't exist
        # :I or is the wrong file type or cannot otherwise be parsed.

    def print_balance_report(self):
        pass
        # :I prints a formatted balance report to console from transactions
        # i dont think i can do this until i have categories for transactions

    def save_balance_report(self):
        pass
        # :I saves a copy of the formatted balance report to a file
        # cant do this until i have balance reports

    def print_category_report(self, category):
        pass


def app(argv):
    # :I functionality when run as a script goes here
    # :I here's a start:
    reporter = AccountReporter(argv)
    # reporter.ingest_files(reporter.ingest_dir)  # want traceback right now
    if reporter.ingest_dir:
        # should take this out of if? this will always
        # have something in it now that i set default dir
        try:
            reporter.ingest_files(reporter.ingest_dir)
        except Exception as e:
            return e
    print('ingest done')  # noob working here too
    pprint.pprint(reporter.transactions)
    ''' not ready yet for this
    if reporter.save_dir:
        try:
            reporter.save_balance_report()
        except Exception as e:
            return e
    '''


if __name__ == '__main__':
    sys.exit(app(sys.argv[1:]))
