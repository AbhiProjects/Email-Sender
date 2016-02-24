import SenderEmail
import Tkinter
import tkMessageBox

def GUI(Status):
	
	StatusMessage='E Mail Was Not Sent'
	
	if (Status==True):
		StatusMessage='E Mail Sent Successfully'
	
	top = Tkinter.Tk()
	top.withdraw()
	tkMessageBox.showinfo("Email Status", StatusMessage)
	
if __name__ == "__main__":
	Status=SenderEmail.MailSender()
	GUI(Status)