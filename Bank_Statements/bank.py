import json
from datetime import date

with open('Bank_Statements/bank.json') as json_file:
    data = json.load(json_file)

period = date.today()
account_number = data['response']['bank_accounts']['7942445']['account_number']
account_holders = data['response']['bank_accounts']['7942445']['account_holders']
holder_address_1 = data['response']['bank_accounts']['7942445']['holder_address_1']
holder_address_2 = data['response']['bank_accounts']['7942445']['holder_address_2']
holder_city = data['response']['bank_accounts']['7942445']['holder_city']
holder_state = data['response']['bank_accounts']['7942445']['holder_state']
holder_zip = data['response']['bank_accounts']['7942445']['holder_zip']
account_type = data['response']['bank_accounts']['7942445']['account_type']
begin_balance = data['response']['bank_accounts']['7942445']['periods'][0]['begin_balance']
