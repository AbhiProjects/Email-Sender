import UserDetails
import os
import sys
import shutil
import string
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from xlrd import open_workbook

AddressList='AddressList'

def CreateFolder(FolderName):
	try:
		os.makedirs(FolderName)
	except OSError:
		pass	

def CreateAddressList(FileName,EmailList):
	try:
		with open(FileName+'.txt','w') as f:
			for email in EmailList:
				f.write(email+"\n")
	except IOError:
		print "The File Named",FileName,".txt was not found"
		
def ExtractingAddressList(FileName):
	RecipientAddress=None
	try:
		with open(FileName+'.txt','r') as f:
			Data=f.read().splitlines()
	except IOError:
		print "The File Named",FileName,".txt was not found"
		return RecipientAddress
	except:
		print "Error Occurred during Text File Processing"
		return RecipientAddress
	
	RecipientAddress = [line.strip() for line in Data]

	return RecipientAddress
	
def CreateSubjectLine():
	ExcelFiles=[]
	name=''

	try:
		for file in os.listdir(os.getcwd()):
			os.rename(file, file.replace(" ", "-"))
		
		for file in os.listdir(os.getcwd()):
			if(file.split(".")[-1]=="xls"):
				ExcelFiles.append(file)
			elif(file.split(".")[-1]=="xlsx"):
				ExcelFiles.append(file)
	except:
		print 'Error in appearing Excel Processing'

	try:
		for file in ExcelFiles:
			with open_workbook(file) as wb:
				for sheet in wb.sheets():
					name+=sheet.name+' '
	except:
		print 'Error in processing Sheet Names'
		
	return (ExcelFiles,name)

def SendEmail(RecipientAddress):
	
	UserName,Password=UserDetails.ObtainUserCredentials()
	ExcelFiles,Subject=CreateSubjectLine()
	
	if(ExcelFiles==[] or Subject==''):
		print 'No Excel Files Found'
		return False
	
	print 'Subject Line Generated'
	
	msg = MIMEMultipart()
 
	msg['From'] = UserName
	msg['To'] = ",".join(RecipientAddress)
	msg['Subject'] = Subject
	
	print 'Recipient Address List Ready'
 
	body = " "
 
	msg.attach(MIMEText(body, 'plain'))
 
	for file in ExcelFiles:
		attachment = open(file, "rb")

		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % file)
 
		msg.attach(part)
		attachment.close()
		
	Data=msg.as_string()
	
	print 'Attachment Ready'
	
	try:
		server = smtplib.SMTP('smtp.rediffmail.com', 25)
		server.starttls()
		server.ehlo()
		server.esmtp_features["auth"] = "LOGIN PLAIN"
		server.login(UserName, Password)
		print 'User Credentials Authenticated'
		Details=server.sendmail(UserName, RecipientAddress, Data)
		server.quit()
		
	except smtplib.SMTPAuthenticationError:
		print 'User Name / Password Incorrect. Please check details again'
	except smtplib.SMTPSenderRefused:
		print 'Sender Address is Incorrect'
	except smtplib.SMTPRecipientsRefused:
		print 'Recipient Address is Incorrect'
	except smtplib.SMTPDataError:
		print 'Message Creation Incorrect'
	except smtplib.SMTPConnectError:
		print 'Connection to the Server refused'
	except smtplib.SMTPException:
		print 'SMTP Error'
	except:
		print 'Error Except SMTP But While Sending E Mail'
	
	if (Details=={}):
		print 'Mail Sent Succesfully'
		
		CreateFolder('Sent')
		for file in ExcelFiles:
			shutil.copy2(file, 'Sent')
			UserDetails.deleteFile(file)
		
		print 'File Saved To Sent Folder'
		
		return True
		
	else:
		print 'Something Went Wrong While Sending The Mails'
		print Details
		return False

def MailSender():

	RecipientAddress=ExtractingAddressList(AddressList)

	if (RecipientAddress==None):
		print 'Address List Extraction Error'
		return

	Result=SendEmail(RecipientAddress)
	
	return Result
	
if __name__ == "__main__":

	if(len(sys.argv)>=3):
		if(str(sys.argv[1]).strip()=="CREATE"):
			lst=sys.argv[2:]
			EmailList = [email.strip() for email in lst if(email!='')]
			CreateAddressList(AddressList,EmailList)
			print 'Address List Generated'
		else:
			print 'Incorrect Command'