from os import getenv
import resend

from .default import get_default_signature

resend.api_key = getenv("RESEND_API_KEY")

to_email = getenv("TO_EMAIL")
signature = getenv("SIGNATURE") or get_default_signature()


def send_raw(subject: str, html: str):
    params: resend.Emails.SendParams = {"from": signature, "to": [to_email], "subject": subject, "html": html}

    email = resend.Emails.send(params)

    print(email)

    return email
