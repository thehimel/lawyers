from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def email_appointment_created(customer, lawyer, form_data):
    subject = 'Appointment Booking Confirmation'

    # This format must be followed to show Lawyers as the display name.
    # The email inside the <> will be replaced with the actual email.
    sender_name = 'Lawyers <summershineocean@gmail.com>'

    to_recipients = []

    # We don't want to share the emails of customer and lawyer.
    bcc_recipients = [customer.email, lawyer.email]

    template_name = 'core/email/appointment_created.html'
    context = {
        'customer': customer,
        'lawyer': lawyer,
        'form_data': form_data,
    }

    # render with dynamic value
    html_content = render_to_string(template_name, context)

    # Strip the html tag. So people can see the pure text at least.
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, sender_name,
                                 to_recipients, bcc=bcc_recipients)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
