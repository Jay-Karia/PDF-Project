import json
import os

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

# ----------------------------------
import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject


def replace_text(content, replacements = dict()):
    lines = content.splitlines()

    result = ""
    in_text = False

    for line in lines:
        if line == "BT":
            in_text = True

        elif line == "ET":
            in_text = False

        elif in_text:
            cmd = line[-2:]
            if cmd.lower() == 'tj':
                replaced_line = line
                for k, v in replacements.items():
                    replaced_line = replaced_line.replace(k, v)
                result += replaced_line + "\n"
            else:
                result += line + "\n"
            continue

        result += line + "\n"

    return result


def process_data(object, replacements):
    data = object.getData()
    decoded_data = data.decode('utf-8')

    replaced_data = replace_text(decoded_data, replacements)

    encoded_data = replaced_data.encode('utf-8')
    if object.decodedSelf is not None:
        object.decodedSelf.setData(encoded_data)
    else:
        object.setData(encoded_data)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="path to PDF document")
    args = vars(ap.parse_args())

    in_file = args["input"]
    filename_base = in_file.replace(os.path.splitext(in_file)[1], "")

    # Provide replacements list that you need here
    replacements = { r'{employerIdNo}': employerIdNo}

    pdf = PdfFileReader(in_file)
    writer = PdfFileWriter()

    for page_number in range(0, pdf.getNumPages()):

        page = pdf.getPage(page_number)
        contents = page.getContents()

        if isinstance(contents, DecodedStreamObject) or isinstance(contents, EncodedStreamObject):
            process_data(contents, replacements)
        elif len(contents) > 0:
            for obj in contents:
                if isinstance(obj, DecodedStreamObject) or isinstance(obj, EncodedStreamObject):
                    streamObj = obj.getObject()
                    process_data(streamObj, replacements)

        writer.addPage(page)

    with open(filename_base + "edit.pdf", 'wb') as out_file:
        writer.write(out_file)