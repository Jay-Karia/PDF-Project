# importing required modules
import json

# global variables
subtotal_descriptions = []
subtotal_rates = []
subtotal_hours = []

def ReadingJSONData():

    global subtotal_descriptions
    global subtotal_rates
    global subtotal_hours

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

            subtotal_descriptions.append(temp_description)
            subtotal_rates.append(temp_rates)
            subtotal_hours.append(temp_hours)

ReadingJSONData()
