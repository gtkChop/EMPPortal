from django.core.mail import EmailMessage
from emappcore.utils import validators, errors as err
from emappcore.common import config, utilities as u

import logging

log = logging.getLogger(__name__)


def send_email_create_employee(to):
    """
    Sends Subject and body to the recently created employee
    :return: tuple
    """
    log.info("Sending an email to the new employee")
    log.info(to)
    if isinstance(to, list) or isinstance(to, tuple):
        if len(to) > 1:
            raise err.ValidationError("This should not happen. On create employee, email is sent to employee only")

    validators.email_validator("work_email", to[0])
    user = u.get_user_given_email(to[0])
    sub = "Admin has created your profile. Please reset your password"
    body = """
    Hi {first_name} {last_name},

    Welcome to {application_name}!!

    Please use this link to reset your password and login to your account to update your profile.

    Password reset link:{reset_link}

    Yours,

    Admin,
    {company_name}
    """.format(
        first_name=user.first_name,
        last_name=user.last_name,
        application_name=config.get("APPLICATION_TITLE"),
        reset_link="",
        company_name=config.get("COMPANY_NAME")
    )

    return sub, body


def send_email(subject=None, body=None, to=None):
    """
    Send an email given subject body and user list

    :param subject: str Email subject
    :param body: str Email body
    :param to: str To who?
    :return: None
    """
    log.info("Sending email to: ")
    log.info(to)
    for _email in to:
        validators.email_validator(_email)

    if not subject or not body:
        raise err.ValidationError("Subject or body is required parameter")
    email = EmailMessage(subject, body, to=to)
    email.send()
