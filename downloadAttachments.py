import sys
import imaplib
import getpass
import email
import datetime

def downloadAttachments(emailAddress,password):
	
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(emailAddress,password)
	mail.select('[Gmail]/Sent Mail')

	#get uids of all messages with subject "test upload"
	result, data = mail.uid('search', None, '(HEADER Subject "test upload")')
	uids = data[0].split()
	
	#read the latest message
	result, data = mail.uid('fetch', uids[-1], '(RFC822)')
	m = email.message_from_string(data[0][1])

	
	if m.get_content_maintype() == 'multipart': #multipart messages only
		for part in m.walk():
			#find the attachment part
			if part.get_content_maintype() == 'multipart': continue
			if part.get('Content-Disposition') is None: continue

			#save the attachment in the program directory
			filename =  "../AllDatabases/" + str(emailAddress.split('@')[0]) + ".sqlite3"
			fp = open(filename, 'wb')
			fp.write(part.get_payload(decode=True))
			fp.close()
			print '          New %s saved!' % filename
	

	
# Start execution here!
if __name__ == '__main__':
	print "Starting email download..."

	emails = ['eatscardislekiosk@gmail.com','techcardislekiosk@gmail.com','dietrickcardislekiosk@gmail.com',
              'umallcardislekiosk@gmail.com','1stmaincardislekiosk@gmail.com','16westkiosk@gmail.com',
              'kiosk7cardisle@gmail.com','pharmacycardislekiosk@gmail.com','metalcardislekiosk@gmail.com']
	
	for i in emails:
		password = '5408675309'
		if i == 'eatscardislekiosk@gmail.com' or i == 'techcardislekiosk@gmail.com':
			password = 'Bettergr33tings'
		downloadAttachments(i, password)