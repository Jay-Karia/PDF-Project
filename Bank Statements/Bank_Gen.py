# Importing required modules
import io
import fitz
from fitz.fitz import Widget
import pdfrw
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader # getting the page numbers
import json # getting the data
import datetime # date range
import sys # arguments

param_month = ''
statement_range = ''
param_year = ''

Input_PDF_file = "Template.pdf"
Output_PDF_file = "Final bank statement.pdf"

def FindStatementDateRange (String_Input_date):
    global param_month
    global param_year
    global statement_range
    '''
    This function gets the range of date in words for the bank statement based on the input date in format DDMMYYYY
    '''

    param_year = String_Input_date[4]+String_Input_date[5]+String_Input_date[6]+String_Input_date[7]
    param_month = String_Input_date[2]+String_Input_date[3]
    param_date = String_Input_date[0]+String_Input_date[1]

    DateTime_Input_date = datetime.datetime(int(param_year), int(param_month), int(param_date))

    Another_Date = DateTime_Input_date.replace(day=28) + datetime.timedelta(days=31)

    DateTime_Difference = Another_Date - datetime.timedelta(days=Another_Date.day)

    last_date = str(DateTime_Difference.day)

    start_date_str = datetime.datetime.strptime(String_Input_date,'%d%m%Y')
    starting_date = start_date_str.strftime('%B %d, %Y')

    month = starting_date.split(' ')[0]
    year = starting_date.split(' ')[2]

    ending_date = f"{month} {last_date}, {year}" 

    statement_range = f"{starting_date} through {ending_date}"



# Read the input JSON file
with open('Bank_Statement_transactions.json') as file:
    data = json.load(file)

# Define all the keys required to populate the PDF
keys = ['account_number', 'account_holders', 'holder_address_1', 'holder_address_2', 'holder_city', 'holder_state', 'holder_zip', 'account_type']

# if the arguments are 2 then proceed
if len(sys.argv) == 2:
    if len(sys.argv[1]) != 8:
        print('The date format should be DDMMYYYY')

    pypdf2_reader = PdfFileReader(Input_PDF_file)
    num_pages = pypdf2_reader.getNumPages()
    String_Input_date = sys.argv[1]

    # getting the start_date and end_date
    if String_Input_date.startswith("01"):
        FindStatementDateRange(String_Input_date)
    else:
        print("The Parameter date should be the first date of the month")

    Account_Details = []

    # Read account holder details
    for index in range(0, len(keys)):
        temp_value = data['response']['bank_accounts']['7942445'][keys[index]]
        Account_Details.append(temp_value)

    for periods in data['response']['bank_accounts']['7942445']['periods']:
        begin_balance = periods['begin_balance']
        end_balance = periods['end_balance']
        Account_Details.append(begin_balance)
        Account_Details.append(end_balance)


    Account_Details[8] = format(float(Account_Details[8]), ".2f")
    Account_Details[9] = format(float(Account_Details[9]), ".2f")


    holder_info = f"{Account_Details[1][0]}\n{Account_Details[2]}\n{Account_Details[3]}\n{Account_Details[4]} {Account_Details[5]} {Account_Details[6]}"
    if Account_Details[2] == None:
        holder_info = f"{Account_Details[1][0]}\n{Account_Details[3]}\n{Account_Details[4]} {Account_Details[5]} {Account_Details[6]}"
    elif Account_Details[3] == None:
        holder_info = f"{Account_Details[1][0]}\n{Account_Details[2]}\n{Account_Details[4]} {Account_Details[5]} {Account_Details[6]}"

    #  Calculate running total 
    positive_amounts = []
    sum_positive = 0.0
    sum_negative = 0.0
    negative_amounts = []

    for amount in data['response']['txns']:
        a = amount['amount']
        if '-' not in a:
            a = float(a)
            positive_amounts.append(a)
            sum_positive= round(sum_positive + a, 2)
        elif '-' in a:
            a = float(a)
            negative_amounts.append(a)
            sum_negative= round(sum_negative + a, 2)

    descriptions = []
    amounts = []
    running_total = [] # numeric - doing
    running_sum = 0.0
    adj_txn_dates = []

    for items in data['response']['txns']:
        d = items['description']
        am = float(items['amount'])

        running_sum += am
        descriptions.append(d)
        amounts.append(format(am,".2f"))
        running_total.append(format(running_sum+float(Account_Details[8]), ".2f"))

        td = items['txn_date']
        td_month = td[0]+td[1]
        td_year = td[6]+td[7]+td[8]+td[9]
        td = td.replace(td_month, param_month)
        td = td.replace('/'+td_year, '')
        adj_txn_dates.append(td)

    new_dict = {}
    for index in range(0, len(data['response']['txns'])):
        new_dict[f"date_{index}"] = adj_txn_dates[index]
        new_dict[f"amount_{index}"] = amounts[index]
        new_dict[f"description_{index}"] = descriptions[index]
        new_dict[f"running_total_{index}"] = running_total[index]
        
        # Write txn details to PDF
        # fillpdfs.write_fillable_pdf(Input_PDF_file, Output_PDF_file, new_dict) 


# populating the text fields (holder)
dict_ = {
    'period_input': statement_range,
    'account_number': Account_Details[0],

    'holder_info': holder_info,

    'begin_balance': Account_Details[8],
    'end_balance': Account_Details[9],
    'deposits': sum_positive,
    'withdrawals': sum_negative,
    'account_type': Account_Details[7],
}

# Write holder details to PDF
# fillpdfs.write_fillable_pdf(Output_PDF_file, Output_PDF_file, dict_) #holder details

# X-Y Writing
y = 160

date_x = 35
description_x = 100
running_x = 500
amount_x = 430

# description = "fsd fsd af df sd fsad f asdf sd fsd fs daf asdf s df as df asdf asd fas df sad fasd f adf f "

# def run():
#     canvas_data = get_overlay_canvas()
#     form = merge(canvas_data, template_path=Input_PDF_file)
#     save(form, filename=Output_PDF_file)

# def get_overlay_canvas() -> io.BytesIO:
#     data = io.BytesIO()
#     pdf = canvas.Canvas(data)
#     # date
#     # for i in range(0, len(adj_txn_dates)):
#     pdf.drawString(x=amount_x, y=y, text="amount")
#     pdf.drawString(x=running_x, y=y, text="running")
#     pdf.drawString(x=date_x, y=y, text="date")
#     pdf.drawString(x=description_x, y=y, text="")

#     pdf.save()
#     data.seek(0)
#     return data

# def merge(overlay_canvas: io.BytesIO, template_path: str) -> io.BytesIO:
#     template_pdf = pdfrw.PdfReader(template_path)
#     overlay_pdf = pdfrw.PdfReader(overlay_canvas)
#     for page, data in zip(template_pdf.pages, overlay_pdf.pages):
#         overlay = pdfrw.PageMerge().add(data)[0]
#         pdfrw.PageMerge(page).add(overlay).render()
#     form = io.BytesIO()
#     pdfrw.PdfWriter().write(form, template_pdf)
#     form.seek(0)
#     return form


# def save(form: io.BytesIO, filename: str):
#     with open(filename, 'wb') as f:
#         f.write(form.read())

# run()
