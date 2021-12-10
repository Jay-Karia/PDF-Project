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
employeeInfo = f'{employeeName}\r\n{employeeAddressLine1}\r\n{employeeAddressLine2}\r\n{employeeAddressCity}\r\n{employeeAddressState}\r\n{employeeAddressZip}'
year = data['response']['forms'][2]['raw_fields']['year']['value']
# last 2 rows
statePrimary = data['response']['forms'][2]['raw_fields']['statePrimary']['value']
stateSecondary = data['response']['forms'][2]['raw_fields']['stateSecondary']['value']
employerStateIdNumberPrimary = data['response']['forms'][2]['raw_fields']['employerStateIdNumberPrimary']['value']
employerStateIdNumberSecondary = data['response']['forms'][2]['raw_fields']['employerStateIdNumberSecondary']['value']
stateWagesTipsPrimary = data['response']['forms'][2]['raw_fields']['stateWagesTipsPrimary']['value']
stateWagesTipsSecondary = data['response']['forms'][2]['raw_fields']['stateWagesTipsSecondary']['value']
stateIncomeTaxPrimary = data['response']['forms'][2]['raw_fields']['stateIncomeTaxPrimary']['value']
stateIncomeTaxSecondary = data['response']['forms'][2]['raw_fields']['stateIncomeTaxSecondary']['value']
localWagesTipsPrimary = data['response']['forms'][2]['raw_fields']['localWagesTipsPrimary']['value']
localWagesTipsSecondary = data['response']['forms'][2]['raw_fields']['localWagesTipsSecondary']['value']
localIncomeTaxPrimary = data['response']['forms'][2]['raw_fields']['localIncomeTaxPrimary']['value']
localIncomeTaxSecondary = data['response']['forms'][2]['raw_fields']['localIncomeTaxSecondary']['value']
localityNamePrimary = data['response']['forms'][2]['raw_fields']['localityNamePrimary']['value']
localityNameSecondary = data['response']['forms'][2]['raw_fields']['localityNameSecondary']['value']

box12aCode = data['response']['forms'][2]['raw_fields']['box12aCode']['value']
box12bCode = data['response']['forms'][2]['raw_fields']['box12bCode']['value']
box12cCode = data['response']['forms'][2]['raw_fields']['box12cCode']['value']
box12dCode = data['response']['forms'][2]['raw_fields']['box12dcode']['value']

keys = ['employeeSocialSecurity','employerIdNo','wagesTipsOtherComp','federalIncomeTaxWithheld','employerName','employerAddressLine1','employerAddressLine2','employerAddressCity','employerAddressState','employerAddressZip','employerInfo','socialSecurityWages','socialSecurityTaxWithheld','medicareWagesAndTips','medicareTaxWithheld','socialSecurityTips','allocatedTips','box9','box12aAmount','box12bAmount','box12cAmount','box12dAmount','box14Other','dependentCareBenefits','employeeLastName','employeeName','employeeAddressLine1','employeeAddressLine2','employeeAddressCity','employeeAddressState','employeeAddressZip','employeeInfo','year','statePrimary','stateSecondary','employerStateIdNumberPrimary','employerStateIdNumberSecondary','stateWagesTipsPrimary','stateWagesTipsSecondary','stateIncomeTaxPrimary','stateIncomeTaxSecondary','localWagesTipsPrimary','localWagesTipsSecondary','localIncomeTaxPrimary','localIncomeTaxSecondary','localityNamePrimary','localityNameSecondary']

values = [employeeSocialSecurity,employerIdNo,wagesTipsOtherComp,federalIncomeTaxWithheld,employerName,employerAddressLine1,employerAddressLine2,employerAddressCity,employerAddressState,employerAddressZip,employerInfo,socialSecurityWages,socialSecurityTaxWithheld,medicareWagesAndTips,medicareTaxWithheld,socialSecurityTips,allocatedTips,box9,box12aAmount,box12bAmount,box12cAmount,box12dAmount,box14Other,dependentCareBenefits,employeeLastName,employeeName,employeeAddressLine1,employeeAddressLine2,employeeAddressCity,employeeAddressState,employeeAddressZip,employeeInfo,year,statePrimary,stateSecondary,employerStateIdNumberPrimary,employerStateIdNumberSecondary,stateWagesTipsPrimary,stateWagesTipsSecondary,stateIncomeTaxPrimary,stateIncomeTaxSecondary,localWagesTipsPrimary,localWagesTipsSecondary,localIncomeTaxPrimary,localIncomeTaxSecondary,localityNamePrimary,localityNameSecondary]

fillpdfs.get_form_fields('a.pdf')
dict_ = {
    'topmostSubform[0].CopyA[0].f1_1[0]': employeeSocialSecurity,
    'topmostSubform[0].CopyA[0].LeftCol[0].f1_3[0]': employerIdNo,
    'topmostSubform[0].CopyA[0].LeftCol[0].f1_4[0]': employerInfo,
    'topmostSubform[0].CopyA[0].RightCol[0].c1_2[0]': 1,
    'topmostSubform[0].CopyA[0].LeftCol[0].f1_6[0]': employeeName,
    'topmostSubform[0].CopyA[0].LeftCol[0].f1_7[0]': employeeLastName,
    'topmostSubform[0].CopyA[0].LeftCol[0].f1_9[0]': employeeInfo,
    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_20[0]': box12aCode,
    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_21[0]': box12aAmount,
    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_22[0]': box12bCode,
    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_23[0]': box12bAmount,
    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_24[0]': box12cCode,
    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_25[0]': box12cAmount,
    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_26[0]': box12dCode,
    'topmostSubform[0].CopyA[0].RightCol[0].Line12[0].f1_27[0]': box12dAmount,
}

fillpdfs.print_form_fields('a.pdf')

fillpdfs.write_fillable_pdf('a.pdf', 'new.pdf', dict_)
fillpdfs.flatten_pdf('new.pdf', 'edited.pdf')
os.remove('new.pdf')
