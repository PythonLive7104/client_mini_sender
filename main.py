import csv
import smtplib
from email.message import EmailMessage
import random
import time 
import concurrent.futures
from datetime import datetime
import getpass

now = datetime.now()
formatted_date = now.strftime("%m-%Y")

advert_display = '''
                  MAILIONDEV
            ----------------------
            |    EMAIL SENDER    |
            |   for text letter  |
            |   Built for ROYAL  |
            ----------------------
            telegram: @MailionDev
        '''
print(advert_display)


with open('letter.txt', 'r', encoding='utf-8') as file:
    letter = file.read()

with open('reply_to.txt', 'r', encoding='utf-8') as file:
    reply_to = file.readline()
    

def sort_csv(file_name):
    rows = []
    with open(file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)

    return rows[1:]

def sort_smtp(file_name):
    rows = []
    with open(file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)

    return rows[1:]

def sending_email(email_address, email_password, host_server, host_port, letter, to_email, name, _subject):
    msg = EmailMessage()
    msg['Subject'] = _subject.strip()
    msg['From'] = f'{name.strip()} <{email_address.strip()}>'
    msg['To'] = to_email.strip()
    msg['Reply-To'] = reply_to.strip()

    # Plain text fallback
    plain_text = letter

    # Add the plain text as base content
    msg.set_content(plain_text, charset='utf-8')

    # Send the email via SMTP
    try:
        with smtplib.SMTP_SSL(host_server, host_port) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
            print(f'MAIL SENT TO {to_email} SUCCESSFULLY')
        time.sleep(2)
    except Exception as e:
        print(f'FAILED TO SEND TO {to_email}: {e}')

    
if __name__ == '__main__':

    data = sort_csv('info.csv')
    smtp_data = sort_smtp('smtp.csv')
    
    
    def setup(item):
        name = item[0].strip()
        to_email = item[1].strip()
        subject = item[2].strip()
        
        smtp_cred  = random.choice(smtp_data)
        host = smtp_cred[0].strip()
        port = int(smtp_cred[1].strip())
        email = smtp_cred[2].strip()
        passw = smtp_cred[3].strip()
        
        personalized_letter = letter.replace('##NAME##', name).replace('##EMAIL##', email).replace('##SUBJECT##', subject)
        sending_email(email, passw, host, port, personalized_letter , to_email, name, subject)


    time_list = ['08-2025', '09-2025', '10-2025', '11-2025', '12-2025']
    if formatted_date in time_list:
        
        input_v = getpass.getpass("Enter 'SERIAL CODE' to begin sending: ").strip()
        if input_v == '57763-77889-76789':

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(setup, item) for item in data]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result() 
                    except Exception as e:
                        print("Error:", e)


            print('TASK COMPLETE!')
            time.sleep(1000)
        else:
            wrong_input = '''
                    WRONG SERIAL CODE
                    -----------------
                    | RUN APP AGAIN |
                    -----------------
                '''
            print(wrong_input)
            time.sleep(1000)

    else:
        wrong_input = '''
                         APP EXPIRED
                    ---------------------
                    | CONTACT DEVELOPER |
                    ---------------------
                    telegram: @MailionDev
                '''
        print(wrong_input)
        time.sleep(1000)

