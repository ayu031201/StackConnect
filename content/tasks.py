from celery import shared_task
from .models import User_Question, User_Answer
from django.core.mail import send_mail
from django.conf import settings
from content.views import fetch_stackoverflow_questions, save_questions_to_db

@shared_task
def send_test_email(to_email):
    subject = 'Thanks from StackConnect!'
    message = 'Thank you for visiting StackConnect. Your feedbacks will be read.'  
    html_message = (
        'Thank you for visiting '
        '<a href="https://stackconnect-r3qa.onrender.com">StackConnect</a>. <br> '
        'Your feedbacks to this email <strong>will be </strong>read.'
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

    return "Email sent"

@shared_task
def get_new_questions():
    print('Getting New Tasks')
    questions_data = fetch_stackoverflow_questions()
    save_questions_to_db(questions_data)
    return "Ok!"
    
