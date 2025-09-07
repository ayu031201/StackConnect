from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .tasks import send_test_email

@receiver(user_logged_in)
def handle_user_logged_in(sender, request, user, **kwargs):
    send_test_email.delay()
