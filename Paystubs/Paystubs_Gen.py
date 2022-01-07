# importing required modules
import json

# global variables
subtotal_descriptions = []
subtotal_rates = []
subtotal_hours = []
subtotal_ytd_pay = []
subtotal_current_pay = []

net_pay_account_number = []
net_pay_current_pay = []

gross_pay = 0.0
ytd_addition = 0.0

def ReadingJSONData():

    global subtotal_descriptions
    global subtotal_rates
    global subtotal_hours
    global subtotal_ytd_pay
    global subtotal_current_pay
    global net_pay_account_number
    global net_pay_current_pay
    global gross_pay
    global ytd_addition

    with open('./Resources/Paystub_fields.json') as json_file:
        items = json.load(json_file)
    for data in items['response']:
        # employer
        employer_name = data['employer']['name']
        employer_address_1 = data['employer']['address']['line1']
        employer_address_2 = data['employer']['address']['line2']
        employer_city = data['employer']['address']['city']
        employer_state = data['employer']['address']['state_code']
        employer_postal_code = data['employer']['address']['postal_code']

        # employee
        employee_name = data['employee']['name']
        employee_address_1 = data['employee']['address']['line1']
        employee_address_2 = data['employee']['address']['line2']
        employee_city = data['employee']['address']['city']
        employee_state = data['employee']['address']['state_code']
        employee_postal_code = data['employee']['address']['postal_code']
        employee_marital_status = data['employee']['marital_status']

        # earning subtotals
        for subtotals in data['earnings']['subtotals']:

            temp_description = subtotals['description']
            temp_rates = subtotals['current_rate']
            temp_hours = subtotals['current_hours']
            temp_ytd_pay = subtotals['ytd_pay']['amount']
            temp_current_pay = subtotals['current_pay']['amount']

            temp_ytd_pay = float(temp_ytd_pay)
            ytd_addition += temp_ytd_pay

            subtotal_descriptions.append(temp_description)
            subtotal_rates.append(temp_rates)
            subtotal_hours.append(temp_hours)
            subtotal_ytd_pay.append(temp_ytd_pay)
            subtotal_current_pay.append(temp_current_pay)


        for totals in data['earnings']['totals']:
            temp_gross_pay = totals['current_pay']['amount']
            if temp_gross_pay == None:
                temp_gross_pay = 0.0
            temp_gross_pay = float(temp_gross_pay)
            gross_pay += temp_gross_pay

        gross_pay = str(gross_pay)
        gross_pay = "$"+"{:,.2f}".format(float(gross_pay))

        for net_pay_data in data['net_pay']['distribution_details']:
            temp_net_pay_account_number = net_pay_data['account_number']

            net_pay_account_number.append(temp_net_pay_account_number)

        temp_total_pays_current_pay = data['net_pay']['totals']['current_pay']['amount']
        net_pay_current_pay.append(temp_total_pays_current_pay)

        ytd_addition = "{:,.2f}".format(float(ytd_addition))

ReadingJSONData()
