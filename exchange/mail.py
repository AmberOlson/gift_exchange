from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import Context
from django.conf import settings


def sendmail(reciever, participant):
    msg_plain = render_to_string('email.txt', {'participant': participant, 'env':settings.ENVIRONMENT_DOMAIN})
    msg_html = render_to_string('email.html', {'participant': participant, 'env':settings.ENVIRONMENT_DOMAIN})

    send_mail(
        'HI',
        msg_plain,
        'some@sender.com',
        [reciever],
        html_message=msg_html,
    )
