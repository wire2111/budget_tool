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
    def __init__(self, date, entity, category, balance_sheet, amount, notes):
        self.date = date
        self.entity = entity
        self.category = category
        self.balance_sheet = balance_sheet
        self.amount = amount
        self.notes = notes

    def __str__(self):
        return 'Date: {} Entity: {} Amount: {}'.format(
            self.date,
            self.entity,
            self.amount)

    def __repr__(self):
        return 'Transaction(Date: {} Entity: {} Amount: {} Origin: {})'.format(
            self.date,
            self.entity,
            self.amount,
            self.balance_sheet)


class AccountReporter(object):
    def __init__(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument("-ingest",
                            default=None,
                            help="folder of files to ingest as transaction\
                            logs relative to script")
        parser.add_argument("-save",
                            default=None,
                            help="save directory for reports")
        args = parser.parse_args(argv)
        self.ingest_dir, self.save_dir = args.ingest, args.save
        self.transactions = []  # list of transaction objects
        self.net_balance = 0
        self.net_expenditures = 0
        self.net_income = 0
        self.problem_transactions = []

    def ingest_balance_sheets(self):
        if self.ingest_dir not in os.listdir('.'):
            raise Exception('Ingest dir invalid')
        os.chdir(self.ingest_dir)
        if not os.listdir('.'):
            raise Exception('Ingest dir empty')
        for balance_sheet in os.listdir('.'):
            self.parse_balance_sheet(balance_sheet)
        if self.problem_transactions:
            pprint.pprint(self.problem_transactions)
            # use a better way after debugging to display this?
            raise Exception('Problem records please fix')
        pprint.pprint(self.transactions)  # <-- noob working here
        return 0  # why specifically 0?
        # ingest balance sheets from self.ingest_dir path,
        # updates self vars, most importantly self.transactions
        # returns 0 if success, some error if failure

    def parse_balance_sheet(self, balance_sheet):
        with open(balance_sheet, mode='r') as fo:
            for line in fo:
                fields = line.split('\t')
                length = len(fields)
                if length == 5:  # i dont want this magic number
                    date, entity, debit, credit, balance = fields
                elif length == 4:  # i dont want this magic number either!
                    date, entity, debit, credit = fields
                else:
                    self.problem_transactions.append(line)
                    # this does not catch all problem cases at all :/
                    continue

                def str_to_float(amount):
                    if amount == '':
                        return 0
                    else:
                        return float(amount.replace(',', ''))

                date = date.rstrip().lstrip()
                '''
                the format i am providing it in sometimes has white space on
                this var
                should figure out how to make this a date object so i can sort
                my transaction list by date
                '''
                credit = str_to_float(credit)
                debit = str_to_float(debit)

                # is this the right way of 'sanitizing' these inputs?

                self.transactions.append(Transaction(
                    date,
                    entity,
                    'to do still',  # todo category sorting
                    balance_sheet,
                    debit - credit,
                    'not sure'))  # notes
                self.net_expenditures += debit
                self.net_income += credit
        # parses balance sheet from specified file path: balance_sheet
        # make sure to consider how to handle if the file path doesn't exist
        # or is the wrong file type or cannot otherwise be parsed.

    def print_balance_report(self):
        pass
        # prints a formatted balance report to console from transactions
        # i dont think i can do this until i have categories for transactions

    def save_balance_report(self):
        pass
        # saves a copy of the formatted balance report to a file
        # cant do this until i have balance reports

    def print_category_report(self, category):
        pass


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
    print('ingest done')  # noob working here too
    if reporter.save_dir:
        try:
            reporter.save_balance_report()
        except Exception as e:
            return e


if __name__ == '__main__':
    sys.exit(app(sys.argv[1:]))
