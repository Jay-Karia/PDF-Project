# importing required modules
from datetime import datetime
from time import daylight
from reportlab.pdfgen.canvas import Canvas
from sys import argv as arg
import pdfrw
import json
import io

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

employer_info = []
employee_info = []

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
    global employee_info
    global employer_info

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

        employer_info = [employer_name, employer_address_1, employer_address_2, employer_city, employer_state, employer_postal_code]

        # employee
        employee_name = data['employee']['name']
        employee_address_1 = data['employee']['address']['line1']
        employee_address_2 = data['employee']['address']['line2']
        employee_city = data['employee']['address']['city']
        employee_state = data['employee']['address']['state_code']
        employee_postal_code = data['employee']['address']['postal_code']
        employee_marital_status = data['employee']['marital_status']

        employee_info = [employee_name, employee_address_1, employee_address_2, employee_city, employee_state, employee_postal_code, employee_marital_status]

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

def PrintingFixedData(): 

    input_pdf_file = 'Template.pdf'
    output_pdf_file = "Final Paystubs.pdf"

    try:
        period_beginning = arg[1]
        pg_year = period_beginning[4]+period_beginning[5]+period_beginning[6]+period_beginning[7]
        pg_month = period_beginning[2]+period_beginning[3]
        pg_day = period_beginning[0]+period_beginning[1]
        period_beginning = f"{pg_month}/{pg_day}/{pg_year}"

        period_ending = arg[2]
        pe_year = period_ending[4]+period_ending[5]+period_ending[6]+period_ending[7]
        pe_month = period_ending[2]+period_ending[3]
        pe_day = period_ending[0]+period_ending[1]
        period_ending = f"{pe_month}/{pe_day}/{pe_year}"

        pay_date = arg[3]
        pd_year = pay_date[4]+pay_date[5]+pay_date[6]+pay_date[7]
        pd_month = pay_date[2]+pay_date[3]
        pd_day = pay_date[0]+pay_date[1]
        pay_date = f"{pd_month}/{pd_day}/{pd_year}"
    except:
        print("Date format should be DDMMYYYY")

    def run():
        canvas_data = get_overlay_data()
        form = merge(canvas_data, template_path=input_pdf_file)
        save(form, filename=output_pdf_file)

    def get_overlay_data() -> io.BytesIO:
        data = io.BytesIO()
        pdf = Canvas(data)

        pdf.setFontSize(10)
        pdf.drawString(100, 730, employer_info[0])

        if employer_info[1] == None:
            employer_info[1] = ""
            pdf.drawString(100, 715, employer_info[2])
            pdf.drawString(100, 700, employer_info[3]+",")
            pdf.drawString(165, 700, employer_info[4])
            pdf.drawString(185, 700, employer_info[5])

        elif employer_info[2] == None:
            employer_info[2] = ""
            pdf.drawString(100, 715, employer_info[1])
            pdf.drawString(100, 700, employer_info[3]+",")
            pdf.drawString(165, 700, employer_info[4])
            pdf.drawString(185, 700, employer_info[5])

        else:
            pdf.drawString(100, 715, employer_info[1])
            pdf.drawString(100, 700, employer_info[2])
            pdf.drawString(100, 685, employer_info[3]+",")
            pdf.drawString(165, 685, employer_info[4])
            pdf.drawString(185, 685, employer_info[5])

        pdf.drawString(185, 670, employee_info[6])

        pdf.drawString(350, 680, employee_info[0])
        if employee_info[1] == None:
            employee_info[1] = ""
            pdf.drawString(350, 665, employee_info[2])
            pdf.drawString(350, 650, employee_info[3]+",")
            pdf.drawString(420, 650, employee_info[4])
            pdf.drawString(440, 650, employee_info[5])

        elif employee_info[2] == None:
            employee_info[2] = ""
            pdf.drawString(350, 665, employee_info[1])
            pdf.drawString(350, 650, employee_info[3]+",")
            pdf.drawString(420, 650, employee_info[4])
            pdf.drawString(440, 650, employee_info[5])

        else:
            pdf.drawString(350, 665, employee_info[1])
            pdf.drawString(350, 650, employee_info[2])
            pdf.drawString(350, 635, employee_info[3]+",")
            pdf.drawString(420, 635, employee_info[4])
            pdf.drawString(440, 635, employee_info[5])

        pdf.drawString(430, 735, period_beginning)
        pdf.drawString(430, 723, period_ending)
        pdf.drawString(430, 711, pay_date)



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

ReadingJSONData()
PrintingFixedData()
