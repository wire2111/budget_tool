#!usr/bin/python3

import argparse
import sys


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


class Transaction:
    def __init__(self, date, entity, category, description, amount, notes):
        self.date = date
        self.entity = entity
        self.category = category
        self.description = description
        self.amount = amount
        self.notes = notes

# might want to change def __str__ and/or def __repr__ for easy formatting


class AccountReporter:
    def __init__(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument("-balance_sheets",
                            nargs='+',
                            default=None,
                            help="files to ingest as transaction logs")
        parser.add_argument("-save",
                            default=None,
                            help="Save directory for reports")
        args = parser.parse_args(argv)
        self.balance_sheets, self.save = args.balance_sheets, args.save
        self.transactions = set()   # set because we do not want to allow duplicate
                                    # transactions, and we can easily overwrite them
        self.net_balance = 0
        self.net_expenditures = 0
        self.net_income = 0

    def parse_balance_sheets(self):
        pass
        # parses balance sheets from self.files,
        # updates self vars, most importantly self.transactions
        # returns 0 if success, some error if failure

    def parse_balance_sheet(self, balance_sheet):
        pass
        # parses balance sheet from specified filepath: balance_sheet
        # make sure to consider how to handle if the filepath doesn't exist
        # or is the wrong filetype or cannot otherwise be parsed.

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
    if reporter.balance_sheets:
        try:
            reporter.parse_balance_sheets()
        except Exception as e:
            return e
    if reporter.save:
        try:
            reporter.save_balance_report()
        except Exception as e:
            return e


if __name__ == '__main__':
    sys.exit(app(sys.argv[1:]))
