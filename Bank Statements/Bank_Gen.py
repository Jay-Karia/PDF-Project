from fillpdf import fillpdfs
import json

with open('Bank_Statement_transactions.json') as file:
    data = json.load(file)
    bank_name = data['response']['bank_accounts']['7942445']['bank_name']

keys = ['account_number', 'account_holders', 'holder_address_1', 'holder_address_2', 'holder_city', 'holder_state', 'holder_zip', 'account_type', 'begin_balance', 'end_balance', 'txn_date', 'description', 'amount', 'running_total']

fillpdfs.print_form_fields('Bank_Statement_blank.pdf') # {} no form fields