from urllib.parse import urlparse

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_rendered_email(subject, base_template_name, recipient_list, context=None):
    if context is None:
        context = {}

    html_content = get_template(base_template_name + ".html").render(context)
    text_content = get_template(base_template_name + ".txt").render(context)

    # Configure and send an EmailMultiAlternatives
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=None,  # this is settings.DEFAULT_FROM_EMAIL
        to=recipient_list,
    )

    msg.attach_alternative(html_content, "text/html")

    msg.send()


def deduce_allowed_hosts(base_url):
    url = urlparse(base_url)
    if url.hostname == "localhost" or url.hostname == "127.0.0.1":
        # Allow both 127.0.0.1 and localhost as hostname when running locally; useful to avoid understanding why
        # localhost:8000 is not allowed when 127.0.0.1:8000 is and vice versa.
        return ["localhost", "127.0.0.1"]
    return [url.hostname]
