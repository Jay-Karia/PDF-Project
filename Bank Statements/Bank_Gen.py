from PyPDF2 import PdfFileReader
import json
import sys

with open('Bank_Statement_transactions.json') as file:
    data = json.load(file)
    bank_name = data['response']['bank_accounts']['7942445']['bank_name']

keys = ['account_number', 'account_holders', 'holder_address_1', 'holder_address_2', 'holder_city', 'holder_state', 'holder_zip', 'account_type', 'begin_balance', 'end_balance', 'txn_date', 'description', 'amount', 'running_total']

if len(sys.argv) == 2:
    if len(sys.argv[1]) != 8:
        print('The date format should be DDMMYYY')

    reader = PdfFileReader('v2.pdf')
    fields = reader.getFormTextFields()
    num_pages = reader.getNumPages()
    raw_date = sys.argv[1]

    if not raw_date.startswith("01"):
        print("The Parameter date should be the first date of the month")

    # getting the year
    
    year = ''
    for index in range(4,8):
        year += raw_date[index]
    print(year)

    #getting the month


# Parameter = file_name, DDMMYYYY

# Bank statements
# Transactions are submitted through JSON (Transaction date is in US format)
# Transactions could go over multiple pages, so ending balance should be on last page
# We will need a running balance for transactions
# Page x of n footer should be posted based on final page
# Period statement on page header should display beginning to end of parameter month. Please allow for days in month and leap years. So parameter 01022020 would give us “February 01, 2020 through February 28, 2020” ---- doing
# Transactions date month year should be adjusted to be based on parameter date.
# So JSON transaction date 10/15/21 with parameter date 01022020 leads to a PDF transaction output date of 02/15/20
# Deposit amounts in bold, please include minus signs for negative transactions
# Deposits and additions. Sum of positive transactions
# Withdrawals and payments. Sum of negative transactions
