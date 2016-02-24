from distutils.core import setup
import py2exe
setup(
		console=['GUI.py'],
		data_files =[('', ['UserDetails.pem', 'UserDetails.db','README.txt','AddressList.txt'])],
		options={"py2exe":{"includes":["email.mime.multipart","email.mime.text"]}}
)