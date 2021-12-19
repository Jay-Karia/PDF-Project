# Importing required modules
from fillpdf import fillpdfs
from PyPDF2 import PdfFileReader
from reportlab.pdfgen import canvas
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
    year = ''
    for index in range(4,8):
        year += raw_date[index]

    # getting the start_date and end_date
    if raw_date.startswith("01"):
        # getting the date
        date = raw_date[0]+raw_date[1]
        #getting the month
        month = raw_date[2]+raw_date[3]
        new_month = ''
        end_date = ''
        if (month == "01"):
            new_month = "January"
            end_date = "31"+' '+new_month+', '+year
        elif (month == "02"):
            new_month = "February"
            end_date = "28"+' '+new_month+', '+year
        elif (month == "03"):
            new_month = "March"
            end_date = "31"+' '+new_month+', '+year
        elif (month == "04"):
            new_month = "April"
            end_date = "30"+' '+new_month+', '+year
        elif (month == "05"):
            new_month = "May"
            end_date = "31"+' '+new_month+', '+year
        elif (month == "06"):
            new_month = "June"
            end_date = "30"+' '+new_month+', '+year
        elif (month == "07"):
            new_month = "July"
            end_date = "31"+' '+new_month+', '+year
        elif (month == "08"):
            new_month = "August"
            end_date = "31"+' '+new_month+', '+year
        elif (month == "09"):
            new_month = "September"
            end_date = "30"+' '+new_month+', '+year
        elif (month == "10"):
            new_month = "October"
            end_date = "31"+' '+new_month+', '+year
        elif (month == "11"):
            new_month = "November"
            end_date = "30"+' '+new_month+', '+year
        elif (month == "12"):
            new_month = "December"
            end_date = "31"+' '+new_month+', '+year
        start_date = date+' '+new_month+', '+year
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

for items in data['response']['txns']:
    d = items['description']
    am = float(items['amount'])
    running_sum += am
    descriptions.append(d)
    amounts.append(am)
    running_total.append(running_sum+values[8])

# populating the fields
dict_ = {
    'period_input': final_date,
    'account_number': values[0],
    'account_holders': values[1],
    'holder_address_1': values[2],
    'holder_address_2': values[3],
    'holder_city': values[4],
    'holder_state': values[5],
    'holder_zip': values[6],
    'begin_balance': values[8],
    'end_balance': values[9],
    'deposits': sum_positive,
    'withdrawals': sum_negative,
    'account_type': values[7],
}


# fillpdfs.print_form_fields('v2.pdf')
fillpdfs.write_fillable_pdf('v2.pdf', 'edited.pdf', dict_)
# fillpdfs.print_form_fields('v2.pdf')

# Parameter = file_name, DDMMYYYY

# Transactions could go over multiple pages, so ending balance should be on last page
# We will need a running balance for transactions
# Page x of n footer should be posted based on final page
# So JSON transaction date 10/15/21 with parameter date 01022020 leads to a PDF transaction output date of 02/15/20
