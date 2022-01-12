# Importing required modules
from reportlab.pdfgen.canvas import Canvas
import pdfrw
import json
import io
import os

# global variables
input_pdf_file = "1099INT_Blank.pdf"
output_pdf_file = "Final_1099INT.pdf"

numeric_data_values = []
payer_and_recipient_data_values = []

def ReadJSONData():
    global numeric_data_values
    global payer_and_recipient_data_values

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
                'a_1099_int-Part1-PayerPii:payerAddress:addressLine1',
                'a_1099_int-Part1-PayerPii:payerAddress:addressLine2',
                'a_1099_int-Part1-PayerPii:payerAddress:city',
                'a_1099_int-Part1-PayerPii:payerAddress:state',
                'a_1099_int-Part1-PayerPii:payerAddress:country',
                'a_1099_int-Part2-RecipientPii:recipientAddress:zip',
                'a_1099_int-Part1-PayerPii:payerTelephoneNo.',
                'a_1099_int-Part1-PayerPii:payerTin(FederalIdentificationNumber)',
                'a_1099_int-Part2-RecipientPii:recipientTin(IdentificationNumber)',
                'a_1099_int-Part2-RecipientPii:recipientName',
                'a_1099_int-Part2-RecipientPii:recipientAddress:addressLine1',
                'a_1099_int-Part2-RecipientPii:recipientAddress:addressLine2',
                'a_1099_int-Part2-RecipientPii:recipientAddress:zip',
                'a_1099_int-Part2-RecipientPii:recipientAddress:city',
                'a_1099_int-Part2-RecipientPii:recipientAddress:state',
                'a_1099_int-Part2-RecipientPii:recipientAddress:country',
                'a_1099_int-Part2-RecipientPii:accountNumber','a_1099_int-Part1-PayerPii:payerRtn(Optional)']

                for index in range(0, len(numeric_data_keys)):
                    v = numeric_data_keys[index] = item['raw_fields'][numeric_data_keys[index]]['value'] 
                    numeric_data_values.append(v)

                for index in range(0, len(payer_and_recipient_data_keys)):
                    pv = payer_and_recipient_data_keys[index] = item['raw_fields'][payer_and_recipient_data_keys[index]]['value'] 
                    payer_and_recipient_data_values.append(pv)

def WriteJSONData():
    def run():
        canvas_data = get_overlay_data()
        form = merge(canvas_data, template_path=input_pdf_file)
        save(form, filename=output_pdf_file)

    def get_overlay_data() -> io.BytesIO:
        global payer_and_recipient_data_values
        data = io.BytesIO()
        pdf = Canvas(data)
        pdf.setFontSize(10)

        # drawing payer's information into the blank pdf file
        payer_start_y = 720

        pdf.drawString(x=55, y=payer_start_y, text=payer_and_recipient_data_values[0])
        if payer_and_recipient_data_values[2] == None or payer_and_recipient_data_values[2] == "":
            payer_and_recipient_data_values[2] = ""
            pdf.drawString(x=55, y=payer_start_y-10, text=payer_and_recipient_data_values[1])
            payer_start_y += 10
        elif payer_and_recipient_data_values[1] == None or payer_and_recipient_data_values[1] == "":
            payer_and_recipient_data_values[1] = ""
            pdf.drawString(x=55, y=payer_start_y-10, text=payer_and_recipient_data_values[2])
            payer_start_y += 10
        else:
            pdf.drawString(x=55, y=payer_start_y-10, text=payer_and_recipient_data_values[1])
            pdf.drawString(x=55, y=payer_start_y-20, text=payer_and_recipient_data_values[2])
        pdf.drawString(x=55, y=payer_start_y-30, text=payer_and_recipient_data_values[3])
        pdf.drawString(x=105, y=payer_start_y-30, text=payer_and_recipient_data_values[4])
        pdf.drawString(x=120, y=payer_start_y-30, text=payer_and_recipient_data_values[6])
        pdf.drawString(x=55, y=payer_start_y-40, text=payer_and_recipient_data_values[5])

        pdf.drawString(x=55, y=640, text=payer_and_recipient_data_values[8])
        pdf.drawString(x=175, y=640, text=payer_and_recipient_data_values[9])
        pdf.drawString(x=55, y=590, text=payer_and_recipient_data_values[10])
        
        if payer_and_recipient_data_values[11] == "":
            pdf.drawString(x=55, y=560, text=payer_and_recipient_data_values[12])
        elif payer_and_recipient_data_values[12] == "":
            pdf.drawString(x=55, y=560, text=payer_and_recipient_data_values[11])
        else:
            pdf.drawString(x=55, y=560, text=payer_and_recipient_data_values[11])
            pdf.drawString(x=55, y=550, text=payer_and_recipient_data_values[12])

        pdf.drawString(x=55, y=530, text=payer_and_recipient_data_values[14])
        pdf.drawString(x=105, y=530, text=payer_and_recipient_data_values[15])
        pdf.drawString(x=120, y=530, text=payer_and_recipient_data_values[13])

        pdf.drawString(x=55, y=450, text=payer_and_recipient_data_values[17])

        # Drawing Right Side Values on PDF
        pdf.drawString(x=300, y=730, text=payer_and_recipient_data_values[18])

        pdf.drawString(x=305, y=687, text=numeric_data_values[0])
        pdf.drawString(x=305, y=650, text=numeric_data_values[1])
        pdf.drawString(x=305, y=615, text=numeric_data_values[2])
        pdf.drawString(x=305, y=590, text=numeric_data_values[3])
        pdf.drawString(x=405, y=590, text=numeric_data_values[4])
        pdf.drawString(x=305, y=568, text=numeric_data_values[5])
        pdf.drawString(x=405, y=568, text=numeric_data_values[6])
        pdf.drawString(x=305, y=530, text=numeric_data_values[7])
        pdf.drawString(x=405, y=530, text=numeric_data_values[8])

        pdf.save()
        data.seek(0)
        return data

    def merge(overlay_canvas: io.BytesIO, template_path: str) -> io.BytesIO:
        template_pdf = pdfrw.PdfReader(template_path)
        overlay_pdf = pdfrw.PdfReader(overlay_canvas)
        for page, data in zip(template_pdf.pages, overlay_pdf.pages):
            overlay = pdfrw.PageMerge().add(data)[0]
            pdfrw.PageMerge(page).add(overlay).render()
        form = io.BytesIO()
        pdfrw.PdfWriter().write(form, template_pdf)
        form.seek(0)
        return form

    def save(form: io.BytesIO, filename: str):
        with open(filename, 'wb') as f:
            f.write(form.read())

    run()
    # os.system(output_pdf_file)

ReadJSONData()
WriteJSONData()
