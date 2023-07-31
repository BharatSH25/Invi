from celery import shared_task
from django.core.mail import send_mail



@shared_task
def send_scheduled_email(subject, message, recipient):
    try:
        send_mail(subject, message, 'bharatharikant25@gmail.com', [recipient])
    except Exception as e:
        print(str(e))

'''
from myapp.tasks import send_scheduled_email
from datetime import datetime

def schedule_emails(request):
    # Assuming you have fetched the data from the database and stored it in a variable called `rows`
    rows = [
        {
            'id': 1,
            'exam_date': '2023-07-08',
            'exam_stime': '03:00:00',
            'exam_etime': '04:00:00',
            'Room': 20,
            'Department': 'ECE',
            'Invigilator': 'gajju',
            'Superintendent': 'Babu',
            'Deputy': 'Govinda',
        },
        {
            'id': 7,
            'exam_date': '2023-07-22',
            'exam_stime': '17:00:00',
            'exam_etime': '06:07:00',
            'Room': 200,
            'Department': 'CSE',
            'Invigilator': 'Shona',
            'Superintendent': 'Bharat',
            'Deputy': 'Govinda',
        },
        # Add more rows if necessary
    ]

    for row in rows:
        # Extract the necessary data from the row
        email_subject = f"Exam Reminder - {row['Department']} Department"
        email_message = f"Dear {row['Invigilator']},\n\nThis is a reminder for your invigilation duty on {row['exam_date']} from {row['exam_stime']} to {row['exam_etime']} in Room {row['Room']}."
        email_recipient = 'recipient@example.com'  # Replace with the actual recipient email address

        # Convert the date and time strings to a datetime object
        scheduled_datetime = datetime.strptime(f"{row['exam_date']} {row['exam_stime']}", "%Y-%m-%d %H:%M:%S")

        # Schedule the email task using Celery's apply_async method
        send_scheduled_email.apply_async(args=[email_subject, email_message, email_recipient], eta=scheduled_datetime)

    return HttpResponse("Email tasks scheduled successfully.")
'''


#in tasks.py

'''
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_scheduled_email(subject, message, recipient):
    send_mail(subject, message, 'sender@example.com', [recipient])
'''