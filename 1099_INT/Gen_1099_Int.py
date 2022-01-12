# Importing required modules
import json

def ReadJSONData():
    with open('A_1099_INT.json') as json_file:
        data = json.load(json_file)
        form_type = ''
        for item in data['response']['forms']:
            form_type = item['form_type']
            if form_type == 'A_1099_INT':
                keys = ['a_1099_int-Part3-Boxes(1-8):1-InterestIncome', 'a_1099_int-Part3-Boxes(1-8):2-EarlyWithdrawalPenalty',
                'a_1099_int-Part3-Boxes(1-8):3-InterestOnU.S.SavingsBondsAndTreasuryObligations',
                'a_1099_int-Part3-Boxes(1-8):4-FederalIncomeTaxWithheld',
                'a_1099_int-Part3-Boxes(1-8):5-InvestmentExpenses',
                'a_1099_int-Part3-Boxes(1-8):6-ForeignTaxPaid',
                'a_1099_int-Part3-Boxes(1-8):7-ForeignCountryOrU.S.Possession',
                'a_1099_int-Part3-Boxes(1-8):8-Tax-ExemptInterest',
                'a_1099_int-Part4-Boxes(9-17):9-SpecifiedPrivateActivityBondInterest',
                'a_1099_int-Part4-Boxes(9-17):10-MarketDiscount',
                'a_1099_int-Part4-Boxes(9-17):11-BondPremium',
                'a_1099_int-Part4-Boxes(9-17):12-BondPremiumOnTreasuryObligations',
                'a_1099_int-Part4-Boxes(9-17):13-BondPremiumOnTax-ExemptBond',
                'a_1099_int-Part4-Boxes(9-17):15-State',
                'a_1099_int-Part4-Boxes(9-17):16-StateIdentificationNo.',
                'a_1099_int-Part4-Boxes(9-17):17-StateTaxWithheld']

                values = []

                for index in range(0, len(keys)):
                    v = keys[index] = item['raw_fields'][keys[index]]['value'] 
                    values.append(v)

                print(values)


ReadJSONData()