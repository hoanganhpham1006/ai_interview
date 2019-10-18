from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from underthesea import ner

import os
import re
import datefinder as df
import datetime

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# path = os.path.join(BASE_DIR, 'cv1.pdf')

def getName(content):
	text = ner(content)
	names = []
	trigger = True;
	for word in text:
		if (word[-1].find('PER') != -1):
		    names.append(word[0])
		    if (word[-1] == 'B-PER'):
		      trigger = False
		elif not trigger:
		  break;
	nameEnt = ' '.join(names)
	return nameEnt

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def extract_text(content, path):
	email_regex = r'[\w\.-]+@[\w\.-]+'
	phone_regex = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
	
	data = {
		"name":
		{	
			"value":"",
			"available":True
		},
		"email":
		{	
			"value":"",
			"available":True
		},
		"dob":
		{	
			"value":"",
			"available":True
		},
		"phone":
		{	
			"value":"",
			"available":True
		},
		"link": path
	}
	
	# Name
	if data['name']['available']:
		name_detected = getName(content)
		if name_detected != '':
			data['name']['value'] = name_detected
			data['name']['available'] = False
	# Email
	if data['email']['available']:
		match = re.search(email_regex, content)
		if match != None:
			mail = match.group(0)
			data['email']["value"] = mail
			data['email']['available'] = False
			
	# Day of birth
	if data['dob']['available']:
		match = df.find_dates(content)
		for d in match:
			if datetime.datetime(year=1970, month=1,day=1) < d <= datetime.datetime(year=2003, month=1,day=1):
				data['dob']['value'] = d.strftime("%Y-%m-%d")
				data['dob']['available'] = False
				break
	# Phone
	if data['phone']['available']:
		match = re.search(phone_regex, content)
		if match != None:
			phone = match.group(0)
			data['phone']["value"] = phone
			data['phone']['available'] = False
		

	return data


def extract_pdf(path):
	textFromPDF = convert_pdf_to_txt(path)
	information = extract_text(textFromPDF, path)
	return information

# print(extract_pdf(path))
# content = convert_pdf_to_txt(path)
# match = df.find_dates(content)
# for d in match:
# 	if datetime.datetime(year=1970, month=1,day=1) < d <= datetime.datetime(year=2003, month=1,day=1):
# 		print(d.strftime("%d-%m-%Y"))
# 		break