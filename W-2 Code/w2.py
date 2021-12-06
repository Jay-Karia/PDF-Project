from fillpdf import fillpdfs
import json

with open('W-2 Code/form_field_mapping.json') as json_file:
    data = json.load(json_file)

employeeSocialSecurity = data['response']['forms'][2]['raw_fields']['employeeSocialSecurityNumber']['value']
employerIdNo = data['response']['forms'][2]['raw_fields']['employerIdNo']['value']

fillpdfs.get_form_fields('Templates/W-2/IRS Form W-2_Blank.pdf')
dict_ = {
    'þÿ\x00f\x001\x00_\x001\x00[\x000\x00]': employeeSocialSecurity,
    'þÿ\x00f\x001\x00_\x003\x00[\x000\x00]': employerIdNo
}

fillpdfs.print_form_fields('Templates/W-2/IRS Form W-2_Blank.pdf')

fillpdfs.write_fillable_pdf('Templates/W-2/IRS Form W-2_Blank.pdf', 'Templates/W-2/new.pdf', dict_)
fillpdfs.flatten_pdf('Templates/W-2/new.pdf', 'Templates/W-2/edited.pdf')
