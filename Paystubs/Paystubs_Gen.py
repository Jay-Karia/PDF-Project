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

included_descriptions = ['Salary', 'Regular Pay', 'Overtime', 'Sick', 'Commission', 'Double Time', 'Holiday', 'Meals', 'Vacation']

period_begin = ''
period_end = ''
pay_date_json = ''

net_pay_account_number = []
net_pay_current_pay = []

gross_pay = 0.0
ytd_addition = 0.0

employer_info = []
employee_info = []

input_pdf_file = 'Template.pdf'
output_pdf_file = "Final Paystubs.pdf"

def ReadJSONData():

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
    global period_begin
    global period_end
    global pay_date_json

    with open('Paystub_fields.json') as json_file:
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
            if temp_rates == None:
                temp_rates = ""
            temp_hours = subtotals['current_hours']
            if temp_hours is None:
                temp_hours = ""
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

        temp_period_begin = data['paystub_details']['pay_period_start_date']
        temp_period_begin = temp_period_begin.replace('-', '')
        begin_year = temp_period_begin[0]+temp_period_begin[1]+temp_period_begin[2]+temp_period_begin[3]
        begin_month = temp_period_begin[4]+temp_period_begin[5]
        begin_date = temp_period_begin[6]+temp_period_begin[7]
        period_begin = f"{begin_date}{begin_month}{begin_year}"

        temp_period_end = data['paystub_details']['pay_period_end_date']
        temp_period_end = temp_period_end.replace('-', '')
        end_year = temp_period_end[0]+temp_period_end[1]+temp_period_end[2]+temp_period_end[3]
        end_month = temp_period_end[4]+temp_period_end[5]
        end_date = temp_period_end[6]+temp_period_end[7]
        period_end = f"{end_date}{end_month}{end_year}"

        temp_pay_date = data['paystub_details']['pay_date']
        temp_pay_date = temp_pay_date.replace('-', '')
        pay_year = temp_pay_date[0]+temp_pay_date[1]+temp_pay_date[2]+temp_pay_date[3]
        pay_month = temp_pay_date[4]+temp_pay_date[5]
        temp_pay_date = temp_pay_date[6]+temp_pay_date[7]
        pay_date_json = f"{temp_pay_date}{pay_month}{pay_year}"

def PrintFixedPosData(): 


    try:
        try:
            period_beginning = arg[1]
        except:
            period_beginning = period_begin
        pg_year = period_beginning[4]+period_beginning[5]+period_beginning[6]+period_beginning[7]
        pg_month = period_beginning[2]+period_beginning[3]
        pg_day = period_beginning[0]+period_beginning[1]
        period_beginning = f"{pg_month}/{pg_day}/{pg_year}"

        try:
            period_ending = arg[2]
        except:
            period_ending = period_end
        pe_year = period_ending[4]+period_ending[5]+period_ending[6]+period_ending[7]
        pe_month = period_ending[2]+period_ending[3]
        pe_day = period_ending[0]+period_ending[1]
        period_ending = f"{pe_month}/{pe_day}/{pe_year}"

        try:
            pay_date = arg[3]
        except:
            pay_date = pay_date_json
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

            pdf.drawString(100, 200, employee_info[2])
            pdf.drawString(100, 185, employee_info[3]+",")
            pdf.drawString(170, 185, employee_info[4])
            pdf.drawString(190, 185, employee_info[5])

        elif employee_info[2] == None:
            employee_info[2] = ""
            pdf.drawString(350, 665, employee_info[1])
            pdf.drawString(350, 650, employee_info[3]+",")
            pdf.drawString(420, 650, employee_info[4])
            pdf.drawString(440, 650, employee_info[5])
            
            pdf.drawString(100, 200, employee_info[1])
            pdf.drawString(100, 185, employee_info[3]+",")
            pdf.drawString(170, 185, employee_info[4])
            pdf.drawString(190, 185, employee_info[5])

        else:
            pdf.drawString(350, 665, employee_info[1])
            pdf.drawString(350, 650, employee_info[2])
            pdf.drawString(350, 635, employee_info[3]+",")
            pdf.drawString(420, 635, employee_info[4])
            pdf.drawString(440, 635, employee_info[5])

            pdf.drawString(100, 215, employee_info[1])
            pdf.drawString(100, 200, employee_info[2])
            pdf.drawString(100, 185, employee_info[3]+",")
            pdf.drawString(170, 185, employee_info[4])
            pdf.drawString(190, 185, employee_info[5])

        pdf.drawString(430, 735, period_beginning)
        pdf.drawString(430, 723, period_ending)

        pdf.drawString(430, 711, pay_date)
        pdf.drawString(470, 190, pay_date)

        pdf.drawString(100, 125, employee_info[0])
        pdf.drawString(353, 125, net_pay_account_number[0])
        pdf.drawString(553, 125, net_pay_current_pay[0])

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

def PrintDynamicPosData():
    def run():
        canvas_data = get_overlay_data()
        form = merge(canvas_data, template_path=output_pdf_file)
        save(form, filename=output_pdf_file)

    def get_overlay_data() -> io.BytesIO:
        global subtotal_descriptions
        data = io.BytesIO()
        pdf = Canvas(data)
        j = 0
        pdf.setFontSize(10)
        for i in range(len(subtotal_descriptions)):
            subtotal_descriptions[i] = subtotal_descriptions[i].title()
            if included_descriptions[i] in subtotal_descriptions:
                j+=15
                pdf.drawString(20, 595-j, included_descriptions[i])
        j=0
        for i in range(len(subtotal_rates)):
            if subtotal_rates[i] == "":
                pass
            else:
                subtotal_rates[i] = "{:,.2f}".format(float(subtotal_rates[i]))
                j+=15
                pdf.drawRightString(145, 595-j, subtotal_rates[i])

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
    pass

ReadJSONData()
PrintFixedPosData()
PrintDynamicPosData()
