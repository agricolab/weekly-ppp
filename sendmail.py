import smtplib
from contextlib import contextmanager
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from timeit import default_timer as timer
from pathlib import Path
from os import environ

# %%
smtp_host = environ.get("SMTPHOST", "smtp.gmail.com")
port = environ.get("PORT", 587)
sender_email = environ.get("SENDER", "your.account@gmail.com")
receiver_email = environ.get("RECEIVER", sender_email)
receiver_email = [
    receiver_email,
    sender_email,
]
password = environ.get("PASSWORD", None)
if password is None:
    print("No password set in environment")
    exit(1)


@contextmanager
def SMTP(sender, password, smtp_host="smtp.gmail.com", smtp_port=587):
    start = timer()
    smtp_serv = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
    try:  # make smtp server and login
        smtp_serv.ehlo_or_helo_if_needed()
        smtp_serv.starttls()
        smtp_serv.ehlo()
        print("smtp setup took (%.2f seconds passed)" % (timer() - start,))
        start = timer()
        smtp_serv.login(sender, password)
        print("login took %.2f seconds" % (timer() - start,))
        start = timer()
        yield smtp_serv
    finally:
        print(
            "Operations with smtp_serv took %.2f seconds" % (timer() - start,)
        )
        start = timer()
        smtp_serv.quit()
        print("Quiting took %.2f seconds" % (timer() - start,))


with SMTP(sender_email, password, smtp_host) as smtp_serv:
    reports = (Path("_file__").parent / "build").glob("*.html")
    report = list(reports)[-1]
    with report.open() as fp:
        html_content = "<html><body>" + fp.read().strip() + "</html></body>"
    with report.with_suffix(".md").open() as fp:
        md_content = fp.read().strip()
    pdf = report.with_suffix(".pdf")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Weekly Report {report.stem}"
    msg["From"] = sender_email
    if type(receiver_email) == list:
        msg["To"] = ", ".join(receiver_email)
    else:
        msg["To"] = receiver_email
    part1 = MIMEText(md_content, "plain")
    part2 = MIMEText(html_content, "html")
    msg.attach(part1)
    msg.attach(part2)

    if pdf.exists():
        with pdf.open("rb") as attachment:
            part3 = MIMEBase("application", "octet-stream")
            part3.set_payload(attachment.read())
            encoders.encode_base64(part3)
            part3.add_header(
                "Content-Disposition",
                f"attachment; filename= {str(pdf.name)}",
            )
            msg.attach(part3)
    smtp_serv.send_message(msg)
