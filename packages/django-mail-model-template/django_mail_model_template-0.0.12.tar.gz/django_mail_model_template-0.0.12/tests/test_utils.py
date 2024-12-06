from django.test import TestCase
from django_mail_model_template.models import MailTemplate
from django_mail_model_template.utils import get_mail_template, send_html_mail, send_text_mail


class MailTemplateTest(TestCase):
    def test_get_main_template(self):
        MailTemplate.objects.create(
            name="main",
            subject="main subject {{ name }}",
            body="main body {% if name %}{{ name }}{% endif %}",
            html="<p>main html {{ name }}</p>",
        )
        params = {"name": "yamada"}
        result = get_mail_template("main", params)
        self.assertEqual(result.subject, "main subject yamada")
        self.assertEqual(result.body, "main body yamada")
        self.assertEqual(result.html, "<p>main html yamada</p>")

    def test_send_html_mail(self):
        MailTemplate.objects.create(
            name="html_mail",
            subject="HTML subject {{ name }}",
            body="HTML body {% if name %}{{ name }}{% endif %}",
            html="<p>HTML {{ name }}</p>",
        )
        params = {"name": "yamada"}
        from_email = "from@example.com"
        to_email_list = ["to@example.com"]

        with self.assertLogs('django_mail_model_template', level='INFO') as cm:
            send_html_mail("html_mail", params, from_email, to_email_list)
        send_html_mail("html_mail", params, from_email, to_email_list)

        self.assertIn("HTML subject yamada", cm.output[0])
        self.assertIn("<p>HTML yamada</p>", cm.output[0])

    def test_send_text_mail(self):
        MailTemplate.objects.create(
            name="text_mail",
            subject="Text subject {{ name }}",
            body="Text body {% if name %}{{ name }}{% endif %}",
            html="<p>Text {{ name }}</p>",
        )
        params = {"name": "yamada"}
        from_email = "from@example.com"
        to_email_list = ["to@example.com"]

        with self.assertLogs('django_mail_model_template', level='INFO') as cm:
            send_text_mail("text_mail", params, from_email, to_email_list)

        self.assertIn("Text subject yamada", cm.output[0])
        self.assertIn("Text body yamada", cm.output[0])
