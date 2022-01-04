# Importing required modules
import io
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj
import textwrap
from PyPDF2.pdf import PdfFileWriter
import pdfrw
from PyPDF2 import PdfFileReader # getting the page numbers
import json # getting the data
import datetime # date range
import sys # arguments

param_month = ''
statement_range = ''
param_year = ''
try:
    Input_PDF_file = sys.argv[3]
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
    if '.json' in sys.argv[1]:
        with open(f'{sys.argv[1]}') as json_file:
            data = json.load(json_file)
    else:
        with open(f'{sys.argv[1]}.json') as json_file:
            data = json.load(json_file)

    # Define all the keys required to populate the PDF
    keys = ['account_number', 'account_holders', 'holder_address_1', 'holder_address_2', 'holder_city', 'holder_state', 'holder_zip', 'account_type']

    # if the arguments are 2 then proceed
    if len(sys.argv) == 4:
        if len(sys.argv[2]) != 8:
            print('The date format should be DDMMYYYY')

        pypdf2_reader = PdfFileReader(Input_PDF_file)
        num_pages = pypdf2_reader.getNumPages()
        String_Input_date = sys.argv[2]

        # getting the start_date and end_date
        if String_Input_date.startswith("01"):
            FindStatementDateRange(String_Input_date)
        else:
            print("The Parameter date should be the first date of the month")

        Account_Details = []

        # Read account holder details
        pk = ''
        for index in data['bank_accounts']:
            pk = index

        for index in range(0, len(keys)):
            temp_value = data['bank_accounts'][pk][keys[index]]
            Account_Details.append(temp_value)

        for periods in data['bank_accounts'][pk]['periods']:
            begin_balance = periods['begin_balance']
            end_balance = periods['end_balance']
            Account_Details.append(begin_balance)
            Account_Details.append(end_balance)


        Account_Details[8] = format(float(Account_Details[8]), ".2f")
        Account_Details[9] = format(float(Account_Details[9]), ".2f")

        positive_amounts = []
        sum_positive = 0.0
        sum_negative = 0.0
        negative_amounts = []

        for amount in data['txns']:
            a = amount['amount']
            a = float(a)
            if a > 0:
                positive_amounts.append(a)
                sum_positive = sum_positive + a
            elif a<=0:
                negative_amounts.append(a)
                sum_negative= round(sum_negative + a, 2)

        descriptions = []
        amounts = []
        running_total = [] # numeric - doing
        running_sum = 0.0
        adj_txn_dates = []

        for index in data['txns']:
            d = index['description']
            am = float(index['amount'])

            running_sum += am
            descriptions.append(d)
            amounts.append(format(am,".2f"))
            running_total.append(format(running_sum+float(Account_Details[8]), ".2f"))

            td = index['txn_date']
            td_month = td[0]+td[1]
            td_year = td[6]+td[7]+td[8]+td[9]
            td = td.replace(td_month, param_month)
            td = td.replace('/'+td_year, '')
            adj_txn_dates.append(td)

        adj_txn_dates = sorted(adj_txn_dates)

        total_txns = len(data['txns'])
        counter = 0

        # X-Y Writing
        date_x = 35

        y = 160
        new_page_date_y = 665

        txn_per_pages = 30
        end_balance_y = 0

        def print_txn_details():
            page_number = 1
            # Print first page
            canvas_data = populate_txn_details(0, 6, date_x, y, False, page_number)
            form = merge(canvas_data, template_path=Output_PDF_file)
            save(form, filename=Output_PDF_file)
            # Print txn detail pages
            start_txn_no = 7
            if total_txns>7:
                for i in range(start_txn_no, total_txns, txn_per_pages):
                    page_number+=1
                    canvas_data = populate_txn_details(i, i+txn_per_pages-1, date_x, new_page_date_y, True, page_number)
                    form = merge(canvas_data, template_path=Output_PDF_file)
                    save(form, filename=Output_PDF_file)

        def populate_txn_details(txn_index_start, txn_index_end, start_x:int, start_y:int, new_page:bool, page_number:int) -> io.BytesIO:
            global description
            global end_balance_y
            global counter

            data = io.BytesIO()
            pdf = Canvas(data)
            if new_page is True:
                counter = 0
                for i in range(1,page_number):
                    pdf.showPage()

            j = 0
            for i in range(txn_index_start, txn_index_end + 1):
                try:
                    max_char_width = 70
                    pdf.setFontSize(8)
                    if len(descriptions[i])>max_char_width:
                        descriptions[i] =  textwrap.shorten(descriptions[i], width=max_char_width)

                    pdf.drawString(x=date_x, y=start_y-j, text=adj_txn_dates[i])
                    pdf.drawString(x=start_x+65, y=start_y-j, text=descriptions[i])
                    pdf.drawRightString(x=start_x+435, y=start_y-j, text="{:,.2f}".format(float(amounts[i])))
                    pdf.drawRightString(x=start_x+505, y=start_y-j, text="{:,.2f}".format(float(running_total[i])))
                    j+= 20
                    counter+=1
                except:
                    pass

            g = 0
            for i in range(0, counter+1):
                g+= 20
                pdf.drawString(x=0, y=start_y+35-g,text="____________________________________________________________________________________________________________________________________________")

            if total_txns<= 7:
                pdf.setFontSize(10)
                end_balance_x = date_x
                end_balance_y = y-(counter*20)
                pdf.drawString(x=end_balance_x, y=end_balance_y, text="End Balance:")

                end_balance_value_x = date_x+505
                end_balance_value_y = end_balance_y
                pdf.drawRightString(x=end_balance_value_x, y=end_balance_value_y, text="$"+"{:,}".format(float(Account_Details[9])))


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

        def insertPages():
            writer = PdfFileWriter()
            reader = PdfFileReader(open(Input_PDF_file, 'rb'))
            writer.insertPage(reader.getPage(0), 0)

            i = 0
            for i in range(7, total_txns, txn_per_pages):
                writer.insertPage(reader.getPage(1), i)

            output = open(Output_PDF_file,'wb')
            writer.write(output) 
            output.close()

        def insertPageNumbersAndAccountNumberAndHolderDetails():
            global Account_Details
            global end_balance_y
            input_file = Output_PDF_file
            output_file = Output_PDF_file

            reader = PdfReader(input_file)
            pages = [pagexobj(p) for p in reader.pages]

            canvas = Canvas(output_file)
            canvas.setFontSize(10)
            # statement date range
            canvas.drawString(x=370, y=740, text=statement_range)
            # holder info
            canvas.drawString(x=50, y=600, text=Account_Details[1][0])
            if f"{Account_Details[2]}" == "None":
                Account_Details[2] = ""
                canvas.drawString(x=50, y=585, text=Account_Details[3])
                canvas.drawString(x=50, y=570, text=Account_Details[4])
                canvas.drawString(x=105, y=570, text=Account_Details[5])
                canvas.drawString(x=125, y=570, text=Account_Details[6])
            elif f"{Account_Details[3]}" == "None":
                Account_Details[3] = ""
                canvas.drawString(x=50, y=585, text=Account_Details[2])
                canvas.drawString(x=50, y=570, text=Account_Details[4])
                canvas.drawString(x=105, y=570, text=Account_Details[5])
                canvas.drawString(x=125, y=570, text=Account_Details[6])
            else:
                canvas.drawString(x=50, y=585, text=Account_Details[2])
                canvas.drawString(x=50, y=570, text=Account_Details[3])
                canvas.drawString(x=50, y=555, text=Account_Details[4])
                canvas.drawString(x=105, y=555, text=Account_Details[5])
                canvas.drawString(x=125, y=555, text=Account_Details[6])

            Account_Details[8] = float(Account_Details[8])
            Account_Details[9] = float(Account_Details[9])
            canvas.drawRightString(x=375, y=470, text="{:,.2f}".format(Account_Details[8]))
            canvas.drawRightString(x=375, y=410, text="{:,.2f}".format(Account_Details[9]))
            canvas.drawRightString(x=375, y=450, text="{:,.2f}".format(sum_positive))
            canvas.drawRightString(x=375, y=430, text="{:,.2f}".format(sum_negative))

            canvas.drawRightString(x = 535, y = 190, text="{:,.2f}".format(float(Account_Details[8])))

            pg_counter = 1


            for page_num, page in enumerate(pages, start=1):
                pg_counter += 1
                canvas.doForm(makerl(canvas, page))

                footer_text = f"Page {page_num} of {len(pages)}"
                if counter>16 or counter<=7:
                    footer_text = f"Page {page_num} of {len(pages)+1}"

                canvas.saveState()
                canvas.setStrokeColorRGB(0, 0, 0)
                canvas.setFont('Times-Roman', 10)
                canvas.drawString(445, 10, footer_text)
                canvas.drawString(425, 725, Account_Details[0])
                canvas.restoreState()
                canvas.showPage()
            
                if pg_counter == len(pages):
                    end_balance_y = new_page_date_y-(20*counter)
                    end_balance_x = 35
                    canvas.drawString(x=end_balance_x, y=end_balance_y, text="End Balance:")

                    end_balance_value_x = date_x+505
                    end_balance_value_y = end_balance_y
                    canvas.drawRightString(x=end_balance_value_x, y=end_balance_value_y, text="$"+"{:,}".format(float(Account_Details[9])))

                    if counter<=16:
                            canvas.drawImage('Footer_image.jpg', x=0, y=25 ,width=595, height=300)

            if counter>16 or counter<=7:
                canvas.drawImage('Footer_image.jpg', x=0, y=25 ,width=595, height=300)
                canvas.setPageSize((595, 300))
                canvas.setFont('Times-Roman', 10)
                canvas.drawString(445, 10, f"Page {len(pages)+1} of {len(pages)+1}")
                canvas.showPage()

            canvas.save()

        insertPages()
        print_txn_details()
        insertPageNumbersAndAccountNumberAndHolderDetails()
        print("PDF Generated Successfully")

except:
    print("\nCould Not Generate PDF\n")
    print(f"Required arguments missing, arguments given -> {len(sys.argv)}")
    print("Required Arguments: 1) Python Script 2) Inputs JSON file 3) DDMMYYYY 4) PDF file name to be generated\n")
