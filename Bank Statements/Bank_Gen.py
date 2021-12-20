# Importing required modules
from fillpdf import fillpdfs
from PyPDF2 import PdfFileReader
import json
import sys

# reading the json file
with open('Bank_Statement_transactions.json') as file:
    data = json.load(file)
    bank_name = data['response']['bank_accounts']['7942445']['bank_name']

# all the keys requires to populate the pdf
keys = ['account_number', 'account_holders', 'holder_address_1', 'holder_address_2', 'holder_city', 'holder_state', 'holder_zip', 'account_type']

# if the arguments are 2 then proceed
if len(sys.argv) == 2:
    if len(sys.argv[1]) != 8:
        print('The date format should be DDMMYYY')

    reader = PdfFileReader('v2.pdf')
    fields = reader.getFormTextFields()
    num_pages = reader.getNumPages()
    raw_date = sys.argv[1]
    # calculating the date from the parameter
    param_year = ''
    for index in range(4,8):
        param_year += raw_date[index]

    # getting the start_date and end_date
    if raw_date.startswith("01"):
        # getting the date
        date = raw_date[0]+raw_date[1]
        #getting the month
        param_month = raw_date[2]+raw_date[3]
        new_month = ''
        end_date = ''
        if (param_month == "01"):
            new_month = "January"
            end_date = "31"+' '+new_month+', '+param_year
        elif (param_month == "02"):
            new_month = "February"
            end_date = "28"+' '+new_month+', '+param_year
        elif (param_month == "03"):
            new_month = "March"
            end_date = "31"+' '+new_month+', '+param_year
        elif (param_month == "04"):
            new_month = "April"
            end_date = "30"+' '+new_month+', '+param_year
        elif (param_month == "05"):
            new_month = "May"
            end_date = "31"+' '+new_month+', '+param_year
        elif (param_month == "06"):
            new_month = "June"
            end_date = "30"+' '+new_month+', '+param_year
        elif (param_month == "07"):
            new_month = "July"
            end_date = "31"+' '+new_month+', '+param_year
        elif (param_month == "08"):
            new_month = "August"
            end_date = "31"+' '+new_month+', '+param_year
        elif (param_month == "09"):
            new_month = "September"
            end_date = "30"+' '+new_month+', '+param_year
        elif (param_month == "10"):
            new_month = "October"
            end_date = "31"+' '+new_month+', '+param_year
        elif (param_month == "11"):
            new_month = "November"
            end_date = "30"+' '+new_month+', '+param_year
        elif (param_month == "12"):
            new_month = "December"
            end_date = "31"+' '+new_month+', '+param_year
        start_date = date+' '+new_month+', '+param_year
        final_date = f'{start_date} through {end_date}'

    else:
        print("The Parameter date should be the first date of the month")

values = []

for index in range(0, len(keys)):
    b_balance = account_number = data['response']['bank_accounts']['7942445'][keys[index]]
    values.append(b_balance)

for periods in data['response']['bank_accounts']['7942445']['periods']:
    b_balance = periods['begin_balance']
    e_balance = periods['end_balance']
    values.append(b_balance)
    values.append(e_balance)

values[8] = float(values[8])
values[9] = float(values[9])

holder_info = f"{values[1][0]}\n{values[2]}\n{values[3]}\n{values[4]} {values[5]} {values[6]}"
if values[2] == None:
    holder_info = f"{values[1][0]}\n{values[3]}\n{values[4]} {values[5]} {values[6]}"
elif values[3] == None:
    holder_info = f"{values[1][0]}\n{values[2]}\n{values[4]} {values[5]} {values[6]}"

positive_amounts = []
sum_positive = 0.0
sum_negative = 0.0
negative_amounts = []

for amount in data['response']['txns']:
    a = amount['amount']
    if '-' not in a:
        positive_amounts.append(a)
        a = float(a)
        sum_positive+= a
    else:
        negative_amounts.append(a)
        a = float(a)
        sum_negative+=a

descriptions = []
amounts = []
running_total = []
running_sum = 0.0
adj_txn_dates = []

for items in data['response']['txns']:
    d = items['description']
    am = float(items['amount'])
    running_sum += am
    descriptions.append(d)
    amounts.append(am)
    running_total.append(running_sum+values[8])

    td = items['txn_date']
    td_month = td[0]+td[1]
    td_year = td[6]+td[7]+td[8]+td[9]
    td = td.replace(td_month, param_month)
    td = td.replace('/'+td_year, '')
    
    adj_txn_dates.append(td)

# Iterating through pages


def add_new_transactions_page():
    '''Adds a new page for transactions details'''
    print("More than 7 transactions")

total_txns = len(data['response']['txns'])
if total_txns > 7:
    add_new_transactions_page()

# populating the fields
dict_ = {
    'period_input': final_date,
    'account_number': values[0],

    'holder_info': holder_info,

    'begin_balance': values[8],
    'end_balance': values[9],
    'deposits': sum_positive,
    'withdrawals': sum_negative,
    'account_type': values[7],

    'txn_date': adj_txn_dates[0],
    'description': descriptions[0],
    'amount': amounts[0],
    'running_total': running_total[0]
}


# fillpdfs.print_form_fields('v2.pdf')
fillpdfs.write_fillable_pdf('v2.pdf', 'edited.pdf', dict_)
# fillpdfs.print_form_fields('v2.pdf')

# Parameter = file_name, DDMMYYYY

# Transactions could go over multiple pages, so ending balance should be on last page
# We will need a running balance for transactions
# Page x of n footer should be posted based on final page
# So JSON transaction date 10/15/21 with parameter date 01022020 leads to a PDF transaction output date of 02/15/20
