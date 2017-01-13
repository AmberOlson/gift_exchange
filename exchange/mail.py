from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import Context


# def sendmail(receiver, party):
#     send_mail(
#         'HI',
#         'THIS IS WRONG, WOW signup {{url "signup" party.id%}}',
#         'from@example.com',
#         [receiver],
#         fail_silently=False,
#     )

# def sendmail(receiver, participant):
#     plaintext = get_template('email.txt')
#     htmly = get_template('email.html')
#
#     link = "www.localhost/8000/signup/invited/" + str(participant.id)
#
#     context = Context({'participant': participant}, {'link': link})
#
#     subject, from_email, to = 'HI', 'from@example.com', receiver
#     text_content = plaintext.render(context)
#     html_content = htmly.render(context)
#     msg = EmailMessage(subject, html_content, from_email, [to])
#     # msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
#     msg.content_subtype = "html"  # Main content is now text/html
#     # msg.attach_alternative(html_content, "text/html")
#     msg.send()

def sendmail(reciever, participant):
    link = "www.localhost/8000/signup/invited/" + str(participant.id)
    msg_plain = render_to_string('email.txt', {'participant': participant}, {"link": link})
    msg_html = render_to_string('email.html', {'participant': participant}, {"link": link})

    send_mail(
        'HI',
        msg_plain,
        'some@sender.com',
        [reciever],
        html_message=msg_html,
    )
