import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email_user, password_for_email, to_email, server, port, subject, text):
    """This function will send an HTML email message email_user:Write email address here password:Documantation in
    site https://github.com/alikushbaev/send_email_free server: Documentation in site https://domar.com/pages/smtp_pop3_server?srsltid=AfmBOoo4tLfSvCkpPEieRFXbYFC6aEHBgpKAnajvHCxAj04s-odRXdby
    port: Documentation in site https://domar.com/pages/smtp_pop3_server?srsltid=AfmBOoo4tLfSvCkpPEieRFXbYFC6aEHBgpKAnajvHCxAj04s-odRXdby
    subject: Write subject here
    text: Write text message here
    """
    connection = smtplib.SMTP(server, port)
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=email_user, password=password_for_email)
        connection.sendmail(
            from_addr=email_user,
            to_addrs=to_email,
            msg=f"Subject:{subject}\n\n{text}"

        )
    print("Email sent!")


def send_email_html(email_user, password_email, to_email, server, port, subject, html_text_file,text):
    """This function will send an HTML email message email_user:Write email address here password:Documantation in
    site https://github.com/alikushbaev/send_email_free server: Documentation in site https://domar.com/pages/smtp_pop3_server?srsltid=AfmBOoo4tLfSvCkpPEieRFXbYFC6aEHBgpKAnajvHCxAj04s-odRXdby
    port: Documentation in site https://domar.com/pages/smtp_pop3_server?srsltid=AfmBOoo4tLfSvCkpPEieRFXbYFC6aEHBgpKAnajvHCxAj04s-odRXdby
    subject: Write subject here
    html_text_file: Write HTML message here
    text: Write text message here
    """
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = to_email

    # Create the body of the message (a plain-text and an HTML version).
    text = text
    html = html_text_file

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP(server, port)
    s.starttls()
    s.login(email_user, password_email)

    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(email_user, to_email, msg.as_string())
    s.quit()
    print("Email sent successfully!")