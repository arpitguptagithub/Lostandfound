import gspread
from oauth2client.service_account import ServiceAccountCredentials

#libraries for email 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

# libraries for lost section 
import cv2 
from skimage.metrics import structural_similarity as compare_ssim
import imutils
import numpy as np
import matplotlib.pyplot as plt 
import requests
import os

threshold =0.8




def send_email(subject, message, to_email):
    # Email credentials and settings
    email_address = 'randomusermanas1@gmail.com'
    email_password = 'evvljoypsecsqzgw'

    
    message['From'] = email_address
    message['To'] = to_email
    message['Subject'] = subject
    # msg.attach(MIMEText(message, 'plain'))

    # Connect to the server and send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    
    
    server.sendmail(email_address, to_email, message.as_string())
    server.quit()

# 
# Authenticate using the credentials JSON file you downloaded
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credSheets.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheets document by its title
spreadsheet = client.open("LostAndFound")

# Access a specific worksheet (sheet) within the document
worksheet = spreadsheet.get_worksheet(0)  # Assuming responses are in the first sheet

# Get all responses as a list of dictionaries
responses = worksheet.get_all_records()

# Create dictionaries to store lost and found items
lost_items = {}
found_items = {}

# Process responses
for response in responses:
    tStamp = response['Timestamp']
    email_address = response['Email Address']
    itemLF = response["Item lost or found "]
    name = response["Your name"]
    contact_info = response["Your Contact info"]
    item_name = response["Item Name "]
    description = response['Item description ']
    category = response["Item category"]
    brand = response['Item brand ']
    attachments = response.get('Attachments', '').split(',') 

    
    
    

    # Add item to the appropriate dictionary based on lost/found status
    if itemLF.lower() == "lost":
        lost_items[item_name] = {
            'category': category,
            'description': description,
            'brand': brand,
            'contact_info': contact_info,
            'name': name,
            'email': email_address,
            'attachments': attachments
        }
    elif itemLF.lower() == "found":
        found_items[item_name] = {
            'category': category,
            'description': description,
            'brand': brand,
            'attachments': attachments
        }

message = MIMEMultipart() 
subject = "ssss"
# Match found items with lost items
for found_item_name, found_item in found_items.items():
    found_item_category = found_item['category']
    found_item_description = found_item['description']
    found_item_brand = found_item['brand']

    # Search for matching lost items
    for lost_item_name, lost_item in lost_items.items():
        if (
            lost_item['category'] == found_item_category and
            (found_item_description in lost_item['description'] or found_item_brand in lost_item['brand'])
        ):
            # Send email to the person who lost the item
            subject = f"Your lost item '{lost_item_name}' has been found!"
            Emessage = f"Your {lost_item_name} has been found. Please contact {lost_item['name']} at {lost_item['contact_info']} for details."
            EmessageD = MIMEText(Emessage)
            message.attach(EmessageD)
            
            
        if found_item['attachments']:
            for attachment_url in found_item['attachments']:
                # Read the image from the attachment URL
                response = requests.get(attachment_url)
                if response.status_code ==200:
                    attachment_content =response.content
                    attachment_image = cv2.imdecode(np.frombuffer(attachment_content, np.uint8), cv2.IMREAD_COLOR)
                
                # Compare the attachment image with each lost item's image

            ssim_score = -111111
            for lost_attachment_url in lost_item['attachments']:
                response = requests.get(lost_attachment_url)
                if response.status_code ==200:
                    lost_attachment_content = response.content
                    lost_attachment_image = cv2.imdecode(np.frombuffer(lost_attachment_content, np.uint8), cv2.IMREAD_COLOR)
                    
                    try:
                        ssim_score = compare_ssim(attachment_image, lost_attachment_image, multichannel=True)
                    except AttributeError:
                         ssim_score =0 
                    
            #  if ssim_score > threshold :
            try:
                
                for attachment_url in found_item['attachments']:
                  response = requests.get(attachment_url)
                  img_data = response.content
                
                  img = MIMEImage(img_data, 'jpg')
                # img = MIMEBase('application', 'octet-stream')
                # img.set_payload(img_data)
                # encoders.encode_base64(img)
                  img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_url))
                  img.add_header('Content-ID', f'<{attachment_url}>')
                  img.add_header('X-Attachment-Id', f'{attachment_url}')
                  message.attach(img)
         

           
        #  # Exit loop after sending email
            except AttributeError:
                print("Yaar url ki maa ki ")
          
        send_email(subject, message, lost_item['email'])
        break
print("Processing completed.")

