#!usr/bin/python3

import argparse
import sys
import os
import pprint
from personal_budget import budget

'''
budget = {
    'booze': 0,
    'fixed': 0,
    'gas': 0,
    'groceries': 0,
    'interest': 0,
    'oneoff': 0,
    'pay': -0,
    'payment': 0,
    'pet': 0,
    'restaurant': 0,
}
'''


class Transaction():
    def __init__(self, date, entity, category, balance_sheet, credit, debit, reporter):
        self.date = date.rstrip().lstrip()
        self.entity = entity.rstrip().lstrip().lower()
        self.category = self.sort_to_category(self.entity, reporter.categories)
        self.balance_sheet = balance_sheet
        self.debit = self.convert_amount(debit)
        self.credit = self.convert_amount(credit)
        self.amount = self.credit - self.debit

    def __repr__(self):
        retstr = 'Transaction('
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

    def convert_amount(self, amount):
        if amount == '':
            return 0
        else:
            return float(amount.replace(',', ''))

    def sort_to_category(self, entity, categories_dict):
        for category, v in categories_dict.items():
            for name in v:
                if name in entity:
                    return category
        return ''


class AccountReporter():
    def __init__(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument("-ingest",
                            default='ingest',
                            help="folder of files to ingest as transaction\
                            logs defaults to 'ingest'")
        parser.add_argument("-categories",
                            default='categories',
                            help="folder of files to ingest as category\
                            names with members names defaults to 'catgories'")
        parser.add_argument("-save",
                            default='save',
                            help="save directory for reports defaults to \
                            save")
        parser.add_argument("-balance",
                            type=int,
                            default=0,
                            help="current bank balance")
        args = parser.parse_args(argv)
        self.ingest_dir = args.ingest
        self.categories_dir = args.categories
        self.save_dir = args.save
        self.bank_balance = args.balance
        self.transactions = []
        self.problem_transactions = []
        self.unknown_name_transactions = []
        self.net_balance = 0
        self.net_expenditures = 0
        self.net_income = 0
        self.categories = {}
        self.category_totals = {}
        self.balance_totals = {}
        self.validate_dir(self.categories_dir)
        self.validate_dir(self.ingest_dir)
        self.ingest_files()
        self.build_balance_totals()

    def validate_dir(self, path_dir_name):
        current_dir_contents = os.listdir('.')
        if path_dir_name not in current_dir_contents:
            raise Exception('Ingest dir invalid {}'.format(path_dir_name))
        path_dir_contents = os.listdir(path_dir_name)
        if path_dir_contents == []:
            raise Exception('Ingest dir empty {}'.format(path_dir_name))

    def ingest_files(self):
        categories_dir_files = os.listdir(self.categories_dir)
        for file in categories_dir_files:
            self.parse_categories(file)
        ingest_dir_files = os.listdir(self.ingest_dir)
        for file in ingest_dir_files:
            self.parse_balance_sheet(file)
        if not self.problem_transactions == []:
            pprint.pprint(self.problem_transactions)
            # use a better way after debugging to display this?
            raise Exception('Problem records please fix')
        if not self.unknown_name_transactions == []:
            pprint.pprint(self.unknown_name_transactions)
            raise Exception("Add names to correct categories")
        return 0

    def parse_categories(self, category_file):
        filename, fileext = os.path.splitext(category_file)
        self.categories[filename] = []
        file_path = self.categories_dir + os.sep + category_file
        with open(file_path, mode='r') as fo:
            for line in fo:
                '''
                line looks like this
                'mcdonalds\n'
                '''
                self.categories[filename].append(line.rstrip().lower())
        for category in self.categories:
            self.category_totals[category] = 0

    def parse_balance_sheet(self, balance_sheet):
        balance_sheet_path = self.ingest_dir + os.sep + balance_sheet
        with open(balance_sheet_path, mode='r') as fo:
            for line in fo:
                '''
                line looks like this:
                'Feb 02, 2018\tSOBEYS LIQUOR #\t45.13\t\t$8,536.95'
                date,          entity,         debit,credit,balance
                '''
                fields = line.split('\t')
                if len(fields) in [4, 5]:
                    date = fields[0]
                    entity = fields[1]
                    debit = fields[2]
                    credit = fields[3]
                else:
                    self.problem_transactions.append(line)
                    continue
                trans = Transaction(date,
                                    entity,
                                    '',
                                    balance_sheet,
                                    debit,
                                    credit,
                                    self)
                if not trans.category == '':
                    self.transactions.append(trans)
                    self.category_totals[trans.category] += trans.credit-trans.debit
                else:
                    self.unknown_name_transactions.append(trans)
                self.net_expenditures += trans.debit
                self.net_income += trans.credit

    def build_balance_totals(self):
        for category in budget:
            self.balance_totals[category] = (budget[category] +
                                             self.category_totals[category])

    def print_balance_report(self):
        retstr = ''
        for category in budget:
            retstr += (category + ': {:.2f}\n'
                       .format(self.balance_totals[category]))
        print('\nbalance report:\n')
        print(retstr)
        return

    def print_category_report(self, category):
        if category == 'all':
            print('\nall transactions ingested:\n')
            for transaction in self.transactions:
                print(transaction)
            return
        if category == 'totals':
            print('\ntransaction expenditure totals:\n')
            for k, v in self.category_totals.items():
                print('{}: {:.2f}'.format(k, v))
        elif category in self.categories:
            print('\nall transactions from category: {}\n'.format(category))
            for transaction in self.transactions:
                if transaction.category == category:
                    print(transaction)
            return
        return

    def print_available_balance(self):
        remaining_budgeted = 0
        full_budget = 0
        for category in budget:
            if category not in ['interest', 'oneoff', 'pay', 'payment']:
                full_budget += budget[category]
                if self.category_totals[category] > 0:
                    remaining_budgeted += self.category_totals[category]
        available = self.bank_balance - remaining_budgeted - full_budget
        if available > 0:
            print('available for transfer:\n{:.2f}'.format(available))
        else:
            print('nothing available')


def app(argv):
    reporter = AccountReporter(argv)
    reporter.print_category_report('all')
    reporter.print_category_report('totals')
    reporter.print_balance_report()
    reporter.print_available_balance()


if __name__ == '__main__':
    sys.exit(app(sys.argv[1:]))
