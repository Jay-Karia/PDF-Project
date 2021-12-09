import json
import pdfrw
from reportlab.pdfgen import canvas
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

box12aCode = data['response']['forms'][2]['raw_fields']['box12aCode']['value']
box12bCode = data['response']['forms'][2]['raw_fields']['box12bCode']['value']
box12cCode = data['response']['forms'][2]['raw_fields']['box12cCode']['value']
box12dCode = data['response']['forms'][2]['raw_fields']['box12dcode']['value']
# -----
year = data['response']['forms'][2]['raw_fields']['year']['value']

def run():
    canvas_data = get_overlay_canvas()
    form = merge(canvas_data, template_path='./a.pdf')
    save(form, filename='merged.pdf')

def get_overlay_canvas() -> io.BytesIO:
    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    # pdf.drawString(x=30, y=300, text=employeeName)
    # row 1
    pdf.drawString(x=180, y=736, text=employeeSocialSecurity)

    pdf.drawString(x=45, y=710, text=employerIdNo)
    pdf.drawString(x=350, y=710, text=wagesTipsOtherComp)
    pdf.drawString(x=470, y=710, text=federalIncomeTaxWithheld)

    pdf.drawString(x=45, y=690, text=employerName)
    pdf.drawString(x=350, y=686, text=socialSecurityWages)
    pdf.drawString(x=470, y=686, text=socialSecurityTaxWithheld)

    pdf.drawString(x=45, y=675, text=employerAddressLine1)
    pdf.drawString(x=55, y=590, text=employeeName)

    pdf.drawString(x=350, y=662, text=medicareWagesAndTips)
    pdf.drawString(x=45, y=660, text=employerAddressLine2)

    pdf.drawString(x=45, y=645, text=employerAddressCity)
    pdf.drawString(x=120, y=645, text=employerAddressState)
    pdf.drawString(x=150, y=645, text=employerAddressZip)

    pdf.drawString(x=200, y=590, text=employeeLastName)

    pdf.drawString(x=350, y=640, text=socialSecurityTips)
    pdf.drawString(x=470, y=640, text=allocatedTips)

    pdf.drawString(x=350, y=615, text=box9)
    pdf.drawString(x=470, y=615, text=dependentCareBenefits)

    pdf.drawString(x=470, y=590, text=box12aCode)
    pdf.drawString(x=470, y=565, text=box12bCode)
    pdf.drawString(x=470, y=543, text=box12cCode)
    pdf.drawString(x=470, y=523, text=box12dCode)

    pdf.drawString(x=500, y=590, text=box12aAmount)
    pdf.drawString(x=500, y=565, text=box12bAmount)
    pdf.drawString(x=500, y=543, text=box12cAmount)
    pdf.drawString(x=500, y=523, text=box12dAmount)

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
