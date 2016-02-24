from Crypto.PublicKey import RSA
from Crypto import Random
import os
import string
import anydbm
import dbhash
import sys

'''
pem Extension for Private Key
txt Extension for User Details UnEncrypted
db Extension for User Details Encrypted 
'''

FileName='UserDetails'
PassPharase='ABHISHEK'

def deleteFile(FileName):
	if(os.path.isfile(FileName)):
		os.remove(FileName)
		return True
	else:
		print "The File Named",FileName,"Does Not Exist"
		return False
		
def CreateAPrivateKey(FileName,Password):
	
	if(os.path.isfile(FileName+'.pem')==True):
		return True
	
	print 'Creating a Private Key'
	random_generator = Random.new().read
	Key = RSA.generate(1024, random_generator)
	try:
		with open(FileName+'.pem','w') as f:
			f.write(Key.exportKey('PEM',Password))
	except IOError:
		print "The File Named",FileName,".pem was not found"
		return False
	
	return True

def ReadAPrivateKey(FileName,Password):
	try:
		with open(FileName+'.pem','r') as f:
			Key = RSA.importKey(f.read(),Password)
	except IOError:
		print "The File Named",FileName,".pem was not found"
		Key=None
	except ValueError:
		print "The Password is Incorrect or the File is not supported"
		Key=None
	
	return Key
	
def CreateUserCredentials(FileName,UserName,Password):
	try:
		with open(FileName+'.txt','w') as f:
			f.write("UserName:"+UserName+"\n")
			f.write("Password:"+Password+"\n")
	except IOError:
		print "The File Named",FileName,".txt was not found"

def ExtractingUserDetails(FileName):
	UserDetails=None
	try:
		with open(FileName+'.txt','r') as f:
			Data=f.read()
	except IOError:
		print "The File Named",FileName,".txt was not found"
		deleteFile(FileName+'.pem')
		deleteFile(FileName+'.txt')
	except:
		print "Error Occurred during Text File Processing"
		deleteFile(FileName+'.pem')
		deleteFile(FileName+'.txt')
	
	lst=Data.split("\n")
	UserName=lst[0].split(":")[-1].strip()
	Password=lst[1].split(":")[-1].strip()
	UserDetails=(UserName,Password)
	
	return UserDetails
		
def EncryptUserCredentials(FileName,Key):
	publicKey = Key.publickey()
		
	UserName,Password=ExtractingUserDetails(FileName)
	
	try:
		f=anydbm.open(FileName+'.db','c')
		f['UserName']=publicKey.encrypt(UserName,1024)[0]
		f['Password']=publicKey.encrypt(Password,1024)[0]
		f.close()
	except:
		print "Error occurred during Encrypting Data"
		deleteFile(FileName+'.pem')
		deleteFile(FileName+'.db')
		deleteFile(FileName+'.txt')
		return False
				
	if(deleteFile(FileName+'.txt')):
		print 'Deleting UnEncryped Files'
	else:
		return False
	
	return True

def UnEncryptUserCredentials(FileName,Key):
	UserDetails=None
	try:
		f=anydbm.open(FileName+'.db','c')
		UserName=Key.decrypt(f.get('UserName', None))
		Password=Key.decrypt(f.get('Password', None))
		f.close()
		
	except:
		print "Error occurred during UnEncrypting Data"
		UnEncryptedData=None
	
	UserDetails=(UserName,Password)
	
	return UserDetails
	
def intialSetup(FileName):
	
	if(CreateAPrivateKey(FileName,PassPharase)==False):
		print 'The Private Key Has not been created'
		return False
		
	Key=ReadAPrivateKey(FileName,PassPharase)
		
	if(EncryptUserCredentials(FileName,Key)):
		print 'User Details Encrypted'
	else:
		print 'User Details were not Encrypted'
		return False
		
	return True

def ObtainUserCredentials():
	
	if(os.path.isfile(FileName+'.db')==False):
		intialSetup(FileName)
		print 'Intial Setup Done'
		
	Key=ReadAPrivateKey(FileName,PassPharase)
	UnEncryptedData=UnEncryptUserCredentials(FileName,Key)
	return UnEncryptedData
	
if __name__ == "__main__":

	if(len(sys.argv)==4):
		if(str(sys.argv[1]).strip()=="CREATE"):
			UserName=str(sys.argv[2]).strip()
			Password=str(sys.argv[3]).strip()
			CreateUserCredentials(FileName,UserName,Password)
			print 'UnEncrypted User Details Created'
		else:
			print 'Incorrect Command'