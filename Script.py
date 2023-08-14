import imaplib
import email
import csv
import re
import os


detach_dir = '/home/arpit/Documents/Script_lost_found/'
if 'attachments' not in os.listdir(detach_dir):
os.mkdir('attachments')

# Email settings ......./// working
EMAIL_HOST = 'imap.gmail.com'
EMAIL_PORT = 993
EMAIL_USERNAME = 'randomusermanas1@gmail.com'
EMAIL_PASSWORD = 'evvljoypsecsqzgw'



# Connect to the email server ............///working
mail = imaplib.IMAP4_SSL(EMAIL_HOST, EMAIL_PORT)
mail.login(EMAIL_USERNAME, EMAIL_PASSWORD)
mail.select("inbox")

# Search for unread emails ............/// working
(retcode, messages) = mail.search(None, '(UNSEEN)')

if retcode == 'OK':

# Search for emails with specific subject or sender, and retrieve the
latest email ......./// working
status, email_ids = mail.search(None, 'SUBJECT "Lost Item Report"')
latest_email_id = email_ids[0].split()[-1]
status, email_data = mail.fetch(latest_email_id, "(RFC822)")

# Parse the email content
raw_email = email_data[0][1]
parsed_email = email.message_from_bytes(raw_email)

# Extract information from the email
subject = parsed_email["subject"]
sender_email = parsed_email["from"]
date_of_losing = parsed_email["date"] # Assuming date of losing is in
the email's "Date" header

# Extract mobile number and reader's name from the email body using
regular expressions needs check..................../
email_body = ""
for part in parsed_email.walk():
if part.get_content_type() == "text/plain":
email_body = part.get_payload(decode=True).decode("utf-8")
break

mobile_number_match = re.search(r'Mobile Number: (\d+)', email_body)
if mobile_number_match:
mobile_number = mobile_number_match.group(1)
else:
mobile_number = "No mobile number found"

item_description_match = re.search(r'item description: (.+)', email_body)
if item_description_match:
item_description = item_description_match.group(1)
else:
item_description = "No description found"

item_location_match = re.search(r'item last seen: (.+)', email_body)
if item_location_match:
item_location = item_location_match.group(1)
else:
item_location = "No description found"

Fp_csv = " "

for part in parsed_email.walk():
# this part comes from the snipped I don't understand yet...
if part.get_content_maintype() == 'multipart':
continue
if part.get('Content-Disposition') is None:
continue
fileName = part.get_filename()

if bool(fileName):
filePath = os.path.join(detach_dir, 'attachments', fileName)
if not os.path.isfile(filePath) :
print (filePath)
fp = open(filePath, 'wb')
fp.write(part.get_payload(decode=True))
fp.close()
# subject = str(parsed_email).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
# print('Downloaded "{file}" from email titled "{subject}" with UID
{uid}.'.format(file=fileName, subject=subject, uid=latest_email_id))
Fp_csv = filePath
# Close the email connection
mail.logout()

# Append information to CSV file
csv_filename = 'lost_items.csv'

item_name = subject
last_seen = item_location # this information needs to be taken from
the system................/
with open(csv_filename, 'a', newline='') as csv_file: # Open CSV in append mode
csv_writer = csv.writer(csv_file)
csv_writer.writerow([item_name, mobile_number, sender_email,
item_description, date_of_losing, last_seen, Fp_csv])

print(f"Lost item information appended to {csv_filename}.")

else:
print("No new emails found.")