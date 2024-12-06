import logging
from .models import MailTemplate
from typing import Dict, Any

from django.template import Context, Template
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)

from dataclasses import dataclass


@dataclass
class MailTemplateParams:
    name: str
    subject: str
    body: str
    html: str


def get_mail_template(name: str, params: Dict[str, Any]) -> MailTemplateParams:
    mail_template = MailTemplate.objects.get(name=name)
    context = Context(params)
    rendered_params = MailTemplateParams(
        name=mail_template.name,
        subject=Template(mail_template.subject).render(context),
        body=Template(mail_template.body).render(context),
        html=Template(mail_template.html).render(context),
    )
    logger.info(rendered_params)
    return rendered_params

def send_html_mail(name: str, params: Dict[str, Any], from_email: str, to_email_list: list[str]):
    mail_template = get_mail_template(name, params)
    email = EmailMessage(
        mail_template.subject,
        mail_template.html,
        from_email,
        to_email_list,
    )
    email.content_subtype = "html"
    email.send()


def send_text_mail(name: str, params: Dict[str, Any], from_email: str, to_email_list: list[str]):
    mail_template = get_mail_template(name, params)
    email = EmailMessage(
        mail_template.subject,
        mail_template.body,
        from_email,
        to_email_list,
    )
    email.content_subtype = "plain"
    email.send()
