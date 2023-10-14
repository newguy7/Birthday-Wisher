import os
import csv
import datetime as dt
import random
import smtplib

from dotenv import load_dotenv

load_dotenv()


my_email = os.environ.get('EMAIL')
password = os.environ.get('APP_PASSWORD')


# 1. Update the birthdays.csv
header_data = [
    ["name", "email", "year", "month", "day"],
]

new_data = [    
    ["Jane", "example@gmail.com", 2000, 1, 1],
]

# Define csv file path
csv_file_path = "birthdays.csv"

# Get current date
today = dt.datetime.now()
current_month = today.month
current_day = today.day

matching_birthdays = []
birthday_emails = []
letter_to_sent = ""

# Update the birthdays.csv
def update_csv():
    try:
        with open(csv_file_path,mode="r") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            
    except FileNotFoundError: 
        with open(csv_file_path,mode="a", newline='') as file:        
            writer = csv.writer(file)
            for row in header_data:
                writer.writerow(row)
            
    finally:
        with open(csv_file_path,mode="a", newline='') as file:
            writer = csv.writer(file)            
            for row in new_data:
                writer.writerow(row)     
            

# Check if today matches a birthday in the birthdays.csv
def check_birthday():
    try:
        with open(csv_file_path,"r") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                # Extract month and day from the csv data
                month, day = map(int,row[3:])

                # check if today matches a birthday
                if month == current_month and day == current_day:
                    # Add the name to the list of matching birthdays
                    matching_birthdays.append(row)
                    birthday_emails.append(row[1])
                                       
    except FileNotFoundError:
        print(f"The file {csv_file_path} does not exist.")


# 3. Personalize the letter
def personalize_letter():
    global letter_to_sent        
    if matching_birthdays:
        letter_number = random.randint(1,3)
        file_path = f"letter_templates/letter_{letter_number}.txt"
        try:
            with open(file_path, "r") as letter_file:
                letter_contents = letter_file.read()
                for birthday in matching_birthdays:
                    name,email  = birthday[0], birthday[1]               
                    letter_to_sent = letter_contents.replace("[NAME]",name)
        except FileNotFoundError:
            print(f"Letter template file {file_path} not found.")
            
    else:
        print("No birthdays today")
    

# Send Birthday Wishes to the Email

def send_email():    
    for email in birthday_emails:              
        to_email = email
        subject = "Happy Birthday"
        message = f"Subject:{subject}\n\n{letter_to_sent}"

        try:
            with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
                # to secure our email connection
                connection.starttls()

                # log in to the email provider
                connection.login(user=my_email, password=password)
                connection.sendmail(
                    from_addr=my_email, 
                    to_addrs=to_email,
                    msg=message)
            print(f"Email sent to {to_email}")
        except Exception as e:
            print(f"Error sending email to {email}: {str(e)}")


update_csv()
check_birthday()
personalize_letter()
send_email()