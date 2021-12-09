import json
from pdfrw import PdfReader, PdfWriter
import io

with open('form_field_mapping.json') as json_file:
    data = json.load(json_file)

# Other
employeeSocialSecurity = data['response']['forms'][2]['raw_fields']['employeeSocialSecurityNumber']['value']
employerIdNo = data['response']['forms'][2]['raw_fields']['employerIdNo']['value']
wagesTipsOtherComp = data['response']['forms'][2]['raw_fields']['wagesTipsOtherComp']['value']
federalIncomeTaxWithheld = data['response']['forms'][2]['raw_fields']['federalIncomeTaxWithheld']['value']
# Employer Information
employerName = data['response']['forms'][2]['raw_fields']['employerName']['value']
employerAddressLine1 = data['response']['forms'][2]['raw_fields']['employerAddressLine1']['value']
employerAddressLine2 = data['response']['forms'][2]['raw_fields']['employerAddressLine2']['value']
employerAddressCity = data['response']['forms'][2]['raw_fields']['employerAddressCity']['value']
employerAddressState = data['response']['forms'][2]['raw_fields']['employerAddressState']['value']
employerAddressZip = data['response']['forms'][2]['raw_fields']['employerAddressZip']['value']
employerInfo = f'{employerName}\r\n{employerAddressLine1}\r\n{employerAddressLine2}\r\n{employerAddressCity}\r\n{employerAddressState}\n{employerAddressZip}'
# ------
socialSecurityWages = data['response']['forms'][2]['raw_fields']['socialSecurityWages']['value']
socialSecurityTaxWithheld = data['response']['forms'][2]['raw_fields']['socialSecurityTaxWithheld']['value']
medicareWagesAndTips = data['response']['forms'][2]['raw_fields']['medicareWagesAndTips']['value']
medicareTaxWithheld = data['response']['forms'][2]['raw_fields']['medicareTaxWithheld']['value']
socialSecurityTips = data['response']['forms'][2]['raw_fields']['socialSecurityTips']['value']
allocatedTips = data['response']['forms'][2]['raw_fields']['allocatedTips']['value']
# Box
box9 = data['response']['forms'][2]['raw_fields']['box9']['value']
box12aAmount = data['response']['forms'][2]['raw_fields']['box12aAmount']['value']
box12bAmount = data['response']['forms'][2]['raw_fields']['box12bAmount']['value']
box12cAmount = data['response']['forms'][2]['raw_fields']['box12cAmount']['value']
box12dAmount = data['response']['forms'][2]['raw_fields']['box12dAmount']['value']
box14Other = data['response']['forms'][2]['raw_fields']['box14Other']['value']
dependentCareBenefits = data['response']['forms'][2]['raw_fields']['dependentCareBenefits']['value']
# Employee Information
employeeLastName = data['response']['forms'][2]['raw_fields']['employeeName']['value'].split(' ')[2]
employeeName = data['response']['forms'][2]['raw_fields']['employeeName']['value'].split(' ')[0]+' '+ data['response']['forms'][2]['raw_fields']['employeeName']['value'].split(' ')[1]
employeeAddressLine1 = data['response']['forms'][2]['raw_fields']['employeeAddressLine1']['value']
employeeAddressLine2 = data['response']['forms'][2]['raw_fields']['employeeAddressLine2']['value']
employeeAddressCity = data['response']['forms'][2]['raw_fields']['employeeAddressCity']['value']
employeeAddressState = data['response']['forms'][2]['raw_fields']['employeeAddressState']['value']
employeeAddressZip = data['response']['forms'][2]['raw_fields']['employeeAddressZip']['value']
employeeInfo = f'{employeeName}{employeeAddressLine1}{employeeAddressLine2}{employeeAddressCity}{employeeAddressState}{employeeAddressZip}'
# -----
year = data['response']['forms'][2]['raw_fields']['year']['value']

# def run():
#     canvas_data = get_overlay_canvas()
#     form = merge(canvas_data, template_path='./a.pdf')
#     save(form, filename='merged.pdf')

# def get_overlay_canvas() -> io.BytesIO:
#     data = io.BytesIO()
#     pdf = canvas.Canvas(data)
#     # pdf.drawString(x=30, y=300, text=employeeName)
#     pdf.drawString(x=85, y=590, text=employeeName)
#     pdf.drawString(x=200, y=590, text=employeeLastName)
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
 