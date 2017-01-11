from django.core.mail import send_mail


def sendmail(receiver):
    send_mail(
        'HI',
        'WOW signup',
        'from@example.com',
        [receiver],
        fail_silently=False,
    )
