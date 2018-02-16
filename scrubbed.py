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

# this form of transaction is essentially a dictionary, but you
# might want to add functionality to it and it allows easy instantiation
# of transactional records


class Transaction(object):
    def __init__(self, date, entity, category, description, amount, notes):
        self.date = date
        self.entity = entity
        self.category = category
        self.description = description
        self.amount = amount
        self.notes = notes

    def __str__(self):
        return 'Date: {} Entity: {} Amount: {}'.format(self.date, self.entity, self.amount)

    def __repr__(self):
        return 'Transaction(Date: {} Entity: {} Amount: {})'.format(self.date, self.entity, self.amount)


class AccountReporter(object):
    def __init__(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument("-ingest",
                            default=None,
                            help="folder of files to ingest as transaction logs relative to script")
        parser.add_argument("-save",
                            default=None,
                            help="save directory for reports")
        args = parser.parse_args(argv)
        self.ingest_dir, self.save_dir = args.ingest, args.save
        self.transactions = []  # list of transaction objects
        self.net_balance = 0
        self.net_expenditures = 0
        self.net_income = 0

    def ingest_balance_sheets(self):
        os.chdir(self.ingest_dir)
        for balance_sheet in os.listdir('.'):
            self.parse_balance_sheet(balance_sheet)
        pprint.pprint(self.transactions)  # <-- noob working here
        # parses balance sheets from self.ingest_dir path,
        # updates self vars, most importantly self.transactions
        # returns 0 if success, some error if failure

    def parse_balance_sheet(self, balance_sheet):
        fo = open(balance_sheet, mode='r')
        for line in fo:
            fields = line.split('\t')
            length = len(fields)
            if length == 5:  # i dont want this magic number
                date, entity, debit, credit, balance = fields
            elif length == 4:  # i dont want this magic number either!
                date, entity, debit, credit = fields
            else:
                continue  # todo deal with this problem record

            def str_to_float(amount):
                if amount == '':
                    return 0
                else:
                    return float(amount.replace(',', ''))

            date = date.rstrip().lstrip()
            credit = str_to_float(credit)
            debit = str_to_float(debit)
            self.transactions.append(Transaction(date,
                                                 entity,
                                                 'to do still',
                                                 balance_sheet,
                                                 debit - credit,
                                                 'not sure'))
            self.net_expenditures += debit
            self.net_income += credit
        # parses balance sheet from specified file path: balance_sheet
        # make sure to consider how to handle if the file path doesn't exist
        # or is the wrong file type or cannot otherwise be parsed.

    def print_balance_report(self):
        pass
        # prints a formatted balance report to console from transactions

    def save_balance_report(self):
        pass
        # saves a copy of the formatted balance report to a file

    def print_category_report(self, category):
        pass
        # this should be self-explanatory at this point

# etc


def app(argv):
    # functionality when run as a script goes here
    # here's a start:
    reporter = AccountReporter(argv)
    # reporter.parse_balance_sheets()  # want traceback right now
    if reporter.ingest_dir:
        try:
            reporter.ingest_balance_sheets()
        except Exception as e:
            return e
    if reporter.save_dir:
        try:
            reporter.save_balance_report()
        except Exception as e:
            return e


if __name__ == '__main__':
    sys.exit(app(sys.argv[1:]))
