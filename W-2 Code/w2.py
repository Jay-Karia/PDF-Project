import json
import PyPDF2

# Taking all the data required
with open('form_field_mapping.json') as json_file:
    data = json.load(json_file)

employeeSocialSecurity = data['response']['forms'][2]['raw_fields']['employeeSocialSecurityNumber']['value']
employerIdNo = data['response']['forms'][2]['raw_fields']['employerIdNo']['value']
wagesTipsOtherComp = data['response']['forms'][2]['raw_fields']['wagesTipsOtherComp']['value']
federalIncomeTaxWithheld = data['response']['forms'][2]['raw_fields']['federalIncomeTaxWithheld']['value']
employerName = data['response']['forms'][2]['raw_fields']['employerName']['value']
employerAddressLine1 = data['response']['forms'][2]['raw_fields']['employerAddressLine1']['value']
employerAddressLine2 = data['response']['forms'][2]['raw_fields']['employerAddressLine2']['value']
employerAddressCity = data['response']['forms'][2]['raw_fields']['employerAddressCity']['value']
employerAddressState = data['response']['forms'][2]['raw_fields']['employerAddressState']['value']
employerAddressZip = data['response']['forms'][2]['raw_fields']['employerAddressZip']['value']
socialSecurityWages = data['response']['forms'][2]['raw_fields']['socialSecurityWages']['value']
socialSecurityTaxWithheld = data['response']['forms'][2]['raw_fields']['socialSecurityTaxWithheld']['value']
medicareWagesAndTips = data['response']['forms'][2]['raw_fields']['medicareWagesAndTips']['value']
medicareTaxWithheld = data['response']['forms'][2]['raw_fields']['medicareTaxWithheld']['value']
socialSecurityTips = data['response']['forms'][2]['raw_fields']['socialSecurityTips']['value']
allocatedTips = data['response']['forms'][2]['raw_fields']['allocatedTips']['value']
box9 = data['response']['forms'][2]['raw_fields']['box9']['value']
dependentCareBenefits = data['response']['forms'][2]['raw_fields']['dependentCareBenefits']['value']
# e (row) remaining