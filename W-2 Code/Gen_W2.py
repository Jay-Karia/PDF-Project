from fillpdf import fillpdfs
import pdfrw
import io
from reportlab.pdfgen import canvas
import json
import sys
import os

if (len(sys.argv) == 4):
    def printing_info():

        '''
        This function will populate the data from the json file: form_field_mapping_v2.json
        into the output PDF file. 
        '''

        if '.json' in sys.argv[1]:

            with open(f'{sys.argv[1]}') as json_file:
                data = json.load(json_file)
        else:
            with open(f'{sys.argv[1]}.json') as json_file:
                data = json.load(json_file)

        for formtype in data['forms']:
            if formtype['form_type'] == 'W2':
                employerName = formtype['raw_fields']['employerName']['value']
                employerAddressLine1 = formtype['raw_fields']['employerAddressLine1']['value']
                employerAddressLine2 = formtype['raw_fields']['employerAddressLine2']['value']
                employerAddressCity = formtype['raw_fields']['employerAddressCity']['value']
                employerAddressState = formtype['raw_fields']['employerAddressState']['value']
                employerAddressZip = formtype['raw_fields']['employerAddressZip']['value']
                employerInfo = f'{employerName}\r\n{employerAddressLine1}\r\n{employerAddressLine2}\r\n{employerAddressCity} {employerAddressState} {employerAddressZip}'
                # ------
                # Employee Information
                employeeLastName = formtype['raw_fields']['employeeName']['value'].split(' ')[2]
                employeeName = formtype['raw_fields']['employeeName']['value'].split(' ')[0]+' '+ formtype['raw_fields']['employeeName']['value'].split(' ')[1]
                employeeAddressLine1 = formtype['raw_fields']['employeeAddressLine1']['value']
                employeeAddressLine2 = formtype['raw_fields']['employeeAddressLine2']['value']
                employeeAddressCity = formtype['raw_fields']['employeeAddressCity']['value']
                employeeAddressState = formtype['raw_fields']['employeeAddressState']['value']
                employeeAddressZip = formtype['raw_fields']['employeeAddressZip']['value']
                employeeInfo = f'\n{employeeAddressLine1}\r\n{employeeAddressLine2}\r\n{employeeAddressCity} {employeeAddressState} {employeeAddressZip}'
                year = formtype['raw_fields']['year']['value']

                keys = ['employeeSocialSecurityNumber','employerIdNo','wagesTipsOtherComp','federalIncomeTaxWithheld','socialSecurityWages','socialSecurityTaxWithheld','medicareWagesAndTips','medicareTaxWithheld','socialSecurityTips','allocatedTips','box9','box12aAmount','box12bAmount','box12cAmount','box12dAmount','box14Other','dependentCareBenefits','year','statePrimary','stateSecondary','employerStateIdNumberPrimary','employerStateIdNumberSecondary','stateWagesTipsPrimary','stateWagesTipsSecondary','stateIncomeTaxPrimary','stateIncomeTaxSecondary','localWagesTipsPrimary','localWagesTipsSecondary','localIncomeTaxPrimary','localIncomeTaxSecondary','localityNamePrimary','localityNameSecondary','box12aCode','box12bCode','box12cCode','box12dcode','employeeAddressLine1','employeeAddressLine2','employeeAddressCity','employeeAddressState','employeeAddressZip']

                values = []

                for index in range(0, len(keys)):
                    v = keys[index] = formtype['raw_fields'][keys[index]]['value'] 
                    values.append(v)
                    # print(values[index], index)

                for index in range(0, len(keys)):
                    if keys[index] is keys[17]:
                        pass
                    else:
                        try:
                            keys[index] = format(float(keys[index]), ',')+'0' 
                        except ValueError:
                            pass

                # fillpdfs.get_form_fields('v2.pdf')

                dict_ = {
                    'topmostSubform[0].CopyA[0].f1_1[0]': keys[0],

                    'topmostSubform[0].CopyA[0].LeftCol[0].f1_3[0]': keys[1],
                    'topmostSubform[0].CopyA[0].LeftCol[0].f1_4[0]': employerInfo,

                    'topmostSubform[0].CopyA[0].RightCol[0].c1_2[0]': 1,

                    'topmostSubform[0].CopyA[0].LeftCol[0].f1_6[0]': employeeName,
                    'topmostSubform[0].CopyA[0].LeftCol[0].f1_7[0]': employeeLastName,
                    'topmostSubform[0].CopyA[0].LeftCol[0].f1_9[0]': employeeInfo,

                    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_20[0]': keys[32],
                    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_21[0]': keys[11],
                    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_22[0]': keys[33],
                    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_23[0]': keys[12],
                    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_24[0]': keys[34],
                    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_25[0]': keys[13],
                    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_26[0]': keys[35],
                    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_27[0]': keys[14],

                    'topmostSubform[0].CopyA[0].RightCol[0].f1_10[0]': keys[2],
                    'topmostSubform[0].CopyA[0].RightCol[0].f1_11[0]': keys[3],
                    'topmostSubform[0].CopyA[0].RightCol[0].f1_12[0]': keys[4],
                    'topmostSubform[0].CopyA[0].RightCol[0].f1_14[0]': keys[6],
                    'topmostSubform[0].CopyA[0].RightCol[0].f1_13[0]': keys[5],
                    'topmostSubform[0].CopyA[0].RightCol[0].f1_15[0]': keys[7],
                    'topmostSubform[0].CopyA[0].RightCol[0].f1_16[0]': keys[8],
                    'topmostSubform[0].CopyA[0].RightCol[0].f1_17[0]': keys[9],
                    'topmostSubform[0].CopyA[0].RightCol[0].f1_18[0]': keys[16],
                    'topmostSubform[0].CopyA[0].RightCol[0].shade[1]': keys[10],
                    'topmostSubform[0].CopyA[0].RightCol[0].f1_28[0]': keys[15],

                    'topmostSubform[0].CopyA[0].f1_29[0]': keys[18],
                    'topmostSubform[0].CopyA[0].f1_30[0]': keys[20],
                    'topmostSubform[0].CopyA[0].f1_36[0]': keys[21],
                    'topmostSubform[0].CopyA[0].f1_31[0]': keys[22],
                    'topmostSubform[0].CopyA[0].f1_32[0]': keys[24],
                    'topmostSubform[0].CopyA[0].f1_37[0]': keys[23],
                    'topmostSubform[0].CopyA[0].f1_38[0]': keys[25],
                    'topmostSubform[0].CopyA[0].f1_33[0]': keys[26],
                    'topmostSubform[0].CopyA[0].f1_39[0]': keys[27],
                    'topmostSubform[0].CopyA[0].f1_34[0]': keys[28],
                    'topmostSubform[0].CopyA[0].f1_41[0]': keys[29],
                    'topmostSubform[0].CopyA[0].f1_35[0]': keys[30],
                }

                # fillpdfs.print_form_fields('v2.pdf')
                if '.pdf' not in sys.argv[3]:
                    fillpdfs.write_fillable_pdf(sys.argv[3]+'.pdf', 'new.pdf', dict_)
                elif '.pdf' in sys.argv[3]:
                    fillpdfs.write_fillable_pdf(sys.argv[3], 'new.pdf', dict_)
                fillpdfs.flatten_pdf('new.pdf', 'edited.pdf')
                os.remove('new.pdf')

    def year_printing():

        '''
        This function will populate the "year" taken from the input parameter while running the script
        '''

        def run():
            canvas_data = get_overlay_canvas()
            form = merge(canvas_data, template_path='./edited.pdf')
            save(form, filename='final.pdf')

        def get_overlay_canvas() -> io.BytesIO:
            data = io.BytesIO()
            pdf = canvas.Canvas(data)
            pdf.setFontSize(size=24)
            if len(sys.argv[2]) == 8:
                arg = sys.argv[2]
                year = ''
                for i in range(4,8):
                    year += arg[i]
                available_fonts = pdf.getAvailableFonts()
                pdf.setFont(psfontname='Helvetica-Bold', size=24)
                pdf.drawString(x=300, y=436, text=year)
            else: 
                print("The date format should be: DDMMYYYY")

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

    try:
        printing_info()
        year_printing()
        os.remove('edited.pdf')
        print('PDF generated successfully!')
    except IndexError:
        print('Could not generate PDF!')

else:
    print(f"Required arguments missing, arguments given -> {len(sys.argv)}\r\n")
    print("Required Arguments: 1) Python Script 2) Inputs JSON file 3) DDMMYYYY 4) PDF file name to be generated")
