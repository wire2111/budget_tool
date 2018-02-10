import argparse

#--= main todo
'''
import all transactions
import all categories and names
sort transactions into categories
get total transaction values for each category

use this to do budget after

'''

#=--


testing = 123
debug = 1
current_bank_total = 8536.95
print('')
print('current bank: %s' % current_bank_total)

#--= global functions # MUCH NEEDED GLOBAL FUNCTIONS



def dprint(text):
	if debug == 1:
		pprint.pprint(text, width=200)

#=--


#--= create records dict
'''
TODO import from txt files the transaction records from all accounts
lets put these into a dict with a key of the file/account name and value being
a list of dicts, each dict inside the file/account name list will be a seperate
transaction

records = {
	'cheque': [
				{
					'date': 'Nov 30, 2016',
					'name': 'ACCT BAL REBATE',
					'debit': 0,
					'credit': 14.95,
					'balance': '$7,541.60',
				},
				{
					'date': 'Nov 30, 2016',
					'name': 'MONTHLY ACCOUNT FEE',
					'debit': 14.95,
					'credit': 0,
					'balance': '$7,526.65',
				}
			],
	'dmc':	[
				{
					'date': 'Nov 30, 2016',
					'name': 'MONTHLY ACCOUNT FEE',
					'debit': 14.95,
					'credit': 0,
					'balance': '$7,526.65',
				}
			]
}
'''
import os
import pprint
import sys

records = {}
expected_records_import = 0
actual_records_imported = 0

def import_records(record_file):
	global expected_records_import
	global actual_records_imported
	account,ext = os.path.splitext(record_file)
	dprint('working with record file: %s' % record_file)
	records.setdefault(account, [])
	records_fo = open(record_file)
	for line in records_fo:
		expected_records_import += 1
		line_list = line.rstrip().lower().split(sep='\t')
		if record_file == 'dvisa.txt':
			del line_list[1]
			while len(line_list) < 5:
				line_list.append('0')
		dict_record = create_transaction_dict(line_list)
		records[account].append(dict_record)
		#actual_records_imported += 1
	records_fo.close()
	return

def create_transaction_dict(record_line):
	try:
		date,name,debit,credit,balance = record_line
	except:
		raise Exception('invalid record: ' + str(record_line))
	try:
		debit = float(debit.replace(',',''))
	except:
		if debit != '':
			print('problem float() on: %s' % debit)
		debit = 0
	try:
		credit = float(credit.replace(',',''))
	except:
		if credit != '':
			print('problem float() on: %s' % credit)
		credit = 0
	ret = {
	'date': date,
	'name': name,
	'debit': debit,
	'credit': credit,
	'balance': balance
	}
	return ret


os.chdir('records')
for record_file in os.listdir('.'):
	import_records(record_file)

for account in records:
	actual_records_imported += len(records[account])
	records[account].reverse()

dprint('records dict start')
dprint(records)
dprint('records dict end')


#print('records found to import: %s' % expected_records_import)
#print('records actually imported: %s' % actual_records_imported)

assert expected_records_import == actual_records_imported, 'records import \
size mismatch'


#=--

#--= create records_totals dicts

'''
TODO get totals of records structure and put them in a records_totals structure
records_totals = {
	'cheque':	{
					'transactions': 2,
					'debit': 14.95,
					'credit': 14.95,
				},
	'dmc':		{
					'transactions': 1,
					'debit': 14.95,
					'credit': 0,
				}
}

'''

records_totals = {}

def round_totals(dest_dict):
	dest_dict['totals']['credit'] = round(dest_dict['totals']['credit'], 2)
	dest_dict['totals']['debit'] = round(dest_dict['totals']['debit'], 2)

def create_totals_dict(dest_dict, account_name):
	dest_dict[account_name] = {
	'transactions': 0,
	'debit': 0,
	'credit': 0
	}

def add_record_records_totals(record):
	records_totals[account]['transactions'] += 1
	records_totals[account]['debit'] += record['debit']
	records_totals[account]['credit'] += record['credit']

for account in records:
	create_totals_dict(records_totals, account)
	for record in records[account]:
		add_record_records_totals(record)

create_totals_dict(records_totals, 'totals')



for account in records_totals:
	if account == 'totals':
		continue
	for key,value in records_totals[account].items():
		records_totals['totals'][key] += value

round_totals(records_totals)

dprint('records_totals dict start:')
dprint(records_totals)
dprint('records_totals dict end')

#=--

#--= create categories dict

'''
TODO import from txt files the categories and names that make them up
this will be a string on each line that could be upper or lower case and can
have whitespace
lets put these into a dict with a key of the category name and a value being a
list of strings that can be names of transactions that belong to this category
categories = {
	'gas': [
			'SHELL',
			'ESSO',
			'co-op gas'
			],
	'booze': [
			'SOBEYS SWCB',
			'OLYMPIA LIQUOR',
			'BOOZEFUCKA'
			]
}

'''
categories = {}
expected_names_import = 0
actual_names_imported = 0

def import_names(category_file):
	global expected_names_import
	global actual_names_imported
	category,ext = os.path.splitext(category_file)
	categories[category] = []
	category_fo = open(category_file)
	for line in category_fo:
		expected_names_import += 1
		categories[category].append(line.rstrip().lower())
	category_fo.close()


os.chdir('../categories')

for category_file in os.listdir('.'):
	import_names(category_file)

for category in categories:
	actual_names_imported += len(categories[category])

#print('names found to import: %s' % expected_names_import)
#print('names actually imported: %s' % actual_names_imported)

assert expected_names_import == actual_names_imported, 'names import \
size mismatch'

dprint('categories dict start:')
dprint(categories)
dprint('categories dict end')

#=--

#--= create sorted dicts

'''
TODO sort records from records structure into the sorted structure which has
the same layout as records but category names instead of account names
sorted = {
	'fixed': 		[
						{
							'date': 'Nov 30, 2016',
							'name': 'ACCT BAL REBATE',
							'debit': 0,
							'credit': 14.95,
							'balance': '$7,541.60',
						},
						{
							'date': 'Nov 30, 2016',
							'name': 'MONTHLY ACCOUNT FEE',
							'debit': 14.95,
							'credit': 0,
							'balance': '$7,526.65',
						}
					],
	'restaurant':	[
						{
							'date': 'Nov 30, 2016',
							'name': 'Mcdonalds',
							'debit': 14.95,
							'credit': 0,
							'balance': '$7,526.65',
						}
					]
}
'''

sorted = {}

for category in categories:
	sorted[category] = []

def sort_record(record, account):
	for category in categories:
		for name in categories[category]:
			if name in record['name']:
				sorted[category].append(record)
				return 1
	print('problem record:')
	print(record)
	return 0

errors = 0

for account in records:
	for record in records[account]:
		if not sort_record(record, account):
			errors = 1

if errors == 1:
	sys.exit()


dprint('sorted dict start:')
dprint(sorted)
dprint('sorted dict end')

#=--

#--= create sorted_totals dict

'''
TODO get totals of sorted structure and put them in a sorted_totals structure
sorted_totals = {
	'fixed':	{
					'transactions': 2,
					'debit': 14.95,
					'credit': 14.95,
				},
	'restaurant':		{
					'transactions': 1,
					'debit': 14.95,
					'credit': 0,
				}
}

'''

sorted_totals = {}

for category in sorted:
	sorted_totals[category] = {
	'transactions': 0,
	'debit': 0,
	'credit': 0
	}
	for record in sorted[category]:
		sorted_totals[category]['transactions'] += 1
		sorted_totals[category]['debit'] += record['debit']
		#if category != 'payment':
			#sorted_totals[category]['credit'] += record['credit']
		sorted_totals[category]['credit'] += record['credit']

sorted_totals['totals'] = {
'transactions': 0,
'debit': 0,
'credit': 0
}

for category in sorted_totals:
	if category == 'totals':
		continue
	for key,value in sorted_totals[category].items():
		sorted_totals['totals'][key] += value

round_totals(sorted_totals)

#print("record_totals %s" % records_totals['totals'])
#print("sorted_totals %s" % sorted_totals['totals'])

assert sorted_totals['totals'] == records_totals['totals'], 'omgfuckup'



dprint('sorted totals start:')
dprint(sorted_totals)
dprint('sorted totals end')

#=--

#--= handle printing certain records from 1st argument
try:
	if sys.argv[1] in sorted:
		print('')
		for r in sorted[sys.argv[1]]:
			ret = 'Date: %s Name: %s Credit: %s Debit: %s' % ( \
			r['date'], \
			r['name'], \
			r['credit'], \
			r['debit']
			)
			print(ret)
		print('')
		sys.exit()
except SystemExit:
	sys.exit()
except:
	pass

#=--

#--= budget_values and income_values dict

budget_values = {
	'groceries': 0, # put real values in here
	'restaurant': 0,
	'booze': 0,
	'gas': 0,
	'pet': 0,
	'fixed': 0, # will be total of fixed_value dict
	'oneoff': 0,
	'interest': 0,
	'payment': 0,
	'pay': 0,
	'total': 0
}

fixed_values = {
	'mortgage': 0, # put real values here
	'utilities': 0,
	'telus': 0,
	'car_ins': 0,
	'house_ins': 0,
	'life_ins': 0,
	'newsgroups': 0,
	'weed': 0,
	'property_taxes': 0,
	'koodoo': 0,
	'toyota': 0
}

income_values = {
	'person1': 0, # put real values here
	'person2': 0,
	'total': 0
}



for k,v in fixed_values.items():
	budget_values['fixed'] += v

for category in budget_values:
	if category == 'total':
		continue
	budget_values['total'] += budget_values[category]

for name in income_values:
	if name == 'total':
		continue
	income_values['total'] += income_values[name]



net_budget = income_values['total'] - budget_values['total']

print('')
print('total monthly expected income: %s' % income_values['total'])
print('total monthly budget(sos amount): %s' % budget_values['total'])
print('projected budget excess: %s' % round(net_budget,2))

dprint('budget values start:')
dprint(budget_values)
dprint('budget values end')
dprint('income values start:')
dprint(income_values)
dprint('income values end')

#=--

#--= create budget_net_totals dict

budget_net_totals = {
	'groceries': 0,
	'restaurant': 0,
	'booze': 0,
	'gas': 0,
	'pet': 0,
	'fixed': 0,
	'oneoff': 0,
	'interest': 0,
	'payment': 0,
	'pay': 0,
	'still needed this month': 0,
	'overage this month': 0
}

for category in sorted_totals:
	#if category not in budget_values:
		#continue
	if category == 'payment':
		sorted_net = sorted_totals[category]['debit']
		budget_net = budget_values[category] - sorted_net
		budget_net_totals[category] = round(budget_net,2)
	elif category == 'totals':
		continue
	elif category == 'interest':
		sorted_net = sorted_totals[category]['debit'] - sorted_totals[category]['credit']
		budget_net = budget_values[category] + sorted_net
		budget_net_totals[category] = round(budget_net,2)
	else:
		sorted_net = sorted_totals[category]['debit'] - sorted_totals[category]['credit']
		budget_net = budget_values[category] - sorted_net
		budget_net_totals[category] = round(budget_net,2)

dprint('budget net totals start:2222')
dprint(budget_net_totals)
dprint('budget net totals end')


for k,v in budget_net_totals.items():
	if k not in ('pay', 'payment', 'still needed this month', 'overage this month', 'interest'):
		if v > 0 and k != 'oneoff':
			budget_net_totals['still needed this month'] += v
		elif v < 0:
			budget_net_totals['overage this month'] += v

budget_net_totals['still needed this month'] = round(budget_net_totals['still needed this month'], 2)
budget_net_totals['overage this month'] = round(budget_net_totals['overage this month'], 2)





dprint('budget net totals start:')
dprint(budget_net_totals)
dprint('budget net totals end')

#=--

print('')
print('current monthly status:')
print('')
for k,v in budget_net_totals.items():
	print('   %s: %s' % (k, v))
print('')


sos_money = budget_values['total']
usable_money = current_bank_total - sos_money
current_remaining_monthly_budget = budget_net_totals['still needed this month'] # remaining projected budget needing to spend still
current_overage_monthly_budget = budget_net_totals['overage this month'] # projected budget overages for this month
usable_money = usable_money - current_remaining_monthly_budget
debt_repayment = round(usable_money,2)
payments_already_done = budget_net_totals['payment'] * -1
interest = budget_net_totals['interest']
net_debt = round(debt_repayment + payments_already_done - interest + current_overage_monthly_budget,2)


if debt_repayment > 0:
	print('debt repayment available now: %s' % debt_repayment)
else:
	print('no debt repayment possible!')
if payments_already_done > 0:
	print('payments already done: %s' % payments_already_done)
if net_debt > 0:
	print('net debt: %s' % net_debt)
else:
	print('net debt in negative!')
	print('net debt: %s' % net_debt)


'''
sanity check transfer amount
assert current_bank_total - debt_repayment from last month + income_values['total'] - sorted_tables['pay']['total'] >= current_remaining_monthly_budget + sos_money



'''
