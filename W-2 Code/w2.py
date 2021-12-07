from fillpdf import fillpdfs
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

fillpdfs.get_form_fields('a.pdf')
dict_ = {
    'þÿ\x00f\x001\x00_\x001\x00[\x000\x00]': employeeSocialSecurity,
    'þÿ\x00f\x001\x00_\x003\x00[\x000\x00]': employerIdNo,
    'þÿ\x00f\x001\x00_\x006\x00[\x000\x00]': employeeName,
    'þÿ\x00f\x001\x00_\x007\x00[\x000\x00]': employeeLastName,
    'þÿ\x00f\x001\x00_\x001\x000\x00[\x000\x00]': wagesTipsOtherComp,
    'þÿ\x00f\x001\x00_\x001\x001\x00[\x000\x00]': federalIncomeTaxWithheld,
    'þÿ\x00f\x001\x00_\x001\x002\x00[\x000\x00]': socialSecurityWages,
    'þÿ\x00f\x001\x00_\x004\x00[\x000\x00]': employerInfo
}

fillpdfs.print_form_fields('a.pdf')

fillpdfs.write_fillable_pdf('a.pdf', 'new.pdf', dict_)
fillpdfs.flatten_pdf('new.pdf', 'edited.pdf')
os.remove('new.pdf')
