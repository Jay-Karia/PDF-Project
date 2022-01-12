# Importing required modules
import json

def ReadJSONData():
    with open('A_1099_INT.json') as json_file:
        data = json.load(json_file)
        form_type = ''
        for item in data['response']['forms']:
            form_type = item['form_type']
            if form_type == 'A_1099_INT':
                numeric_data_keys = ['a_1099_int-Part3-Boxes(1-8):1-InterestIncome', 'a_1099_int-Part3-Boxes(1-8):2-EarlyWithdrawalPenalty',
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

                payer_and_recipient_data_keys = ['a_1099_int-Part1-PayerPii:payerName', 
                'a_1099_int-Part2-RecipientPii:recipientAddress:addressLine1',
                'a_1099_int-Part2-RecipientPii:recipientAddress:addressLine2',
                'a_1099_int-Part1-PayerPii:payerAddress:city',
                'a_1099_int-Part1-PayerPii:payerAddress:state',
                'a_1099_int-Part1-PayerPii:payerAddress:country',
                'a_1099_int-Part2-RecipientPii:recipientAddress:zip',
                'a_1099_int-Part1-PayerPii:payerTelephoneNo.',
                'a_1099_int-Part1-PayerPii:payerTin(FederalIdentificationNumber)',
                "a_1099_int-Part2-RecipientPii:recipientTin(IdentificationNumber)",
                'a_1099_int-Part2-RecipientPii:recipientTin(IdentificationNumber)',
                'a_1099_int-Part2-RecipientPii:recipientName',
                'a_1099_int-Part2-RecipientPii:recipientAddress:addressLine1',
                'a_1099_int-Part2-RecipientPii:recipientAddress:addressLine2',
                'a_1099_int-Part2-RecipientPii:recipientAddress:zip',
                'a_1099_int-Part2-RecipientPii:recipientAddress:city',
                'a_1099_int-Part2-RecipientPii:recipientAddress:state',
                'a_1099_int-Part2-RecipientPii:recipientAddress:country',
                'a_1099_int-Part2-RecipientPii:accountNumber','a_1099_int-Part1-PayerPii:payerRtn(Optional)']

                numeric_data_values = []

                payer_and_recipient_data_values = []

                for index in range(0, len(numeric_data_keys)):
                    v = numeric_data_keys[index] = item['raw_fields'][numeric_data_keys[index]]['value'] 
                    numeric_data_values.append(v)

                for index in range(0, len(payer_and_recipient_data_keys)):
                    pv = payer_and_recipient_data_keys[index] = item['raw_fields'][payer_and_recipient_data_keys[index]]['value'] 
                    payer_and_recipient_data_values.append(pv)

                print(payer_and_recipient_data_values)


ReadJSONData()
