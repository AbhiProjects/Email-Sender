# Email-Sender

## The UserDetails.txt File Format
* UserName:<UserName>
* Password:<Password>

## AddressList.txt File Format

* EmailAddress1
* EmailAddress2
* EmailAddress3

To Change the Username/Password,Delete the files UserDetails.db and UserDetails.pem and create a new UserDetails.txt
The UnEncrypted Version of the file UserDetails.txt will be deleted automatically and encrypted version will take its place.

UserDetails.pem is the private key
UserDetails.db contains the encrypted version of the UserDetails.txt

### To Generate A UserDetails Pragmatically Run The Following Command

* UserDetails.pyc CREATE <USERNAME> <PASSWORD>

### To Generate A AddressList Pragmatically Run The Following Command

SenderEmail.pyc CREATE <EmailAddress1> <EmailAddress2> .......

The Sent Orders will appear in the Sent Folder in the Local Machine.
