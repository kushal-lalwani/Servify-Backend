from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import threading


def send_email(subject, message, recipient_list):
    def email_task():
        send_mail(
            subject=subject,
            message=message,
            from_email='servify.notifications@gmail.com',
            recipient_list=recipient_list,
        )
    
    # Create and start the thread
    thread = threading.Thread(target=email_task)
    thread.start()
