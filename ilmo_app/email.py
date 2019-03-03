import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .localizations import fi
from django.conf import settings


def send_confirmation_mail(event, attendee, template):
    setting_key = 'ILMO_EMAIL_TEMPLATE_PATH'
    template_path = getattr(settings, setting_key)

    if not template_path:
        logging.error('setting %s was not set so confirmation emails are not sent' % setting_key)
        return

    msg_html = render_to_string('%s/%s.html' % (template_path, template),
                                dict(event=event, attendee=attendee), debug=True)
    send_mail(subject=fi.registrationEmailSubject,
              message=msg_html,
              from_email=getattr(settings, 'ILMO_FROM_EMAIL', 'noreply@mysite.com'),
              html_message=msg_html,
              recipient_list=[attendee.attendee_email])
