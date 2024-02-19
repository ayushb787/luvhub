from fastapi import FastAPI, Form, UploadFile, APIRouter, Depends
from fastapi.responses import JSONResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os
import email.utils
import secrets
import string

router = APIRouter()

# SMTP Server Configuration
# SMTP_SERVER: str = os.getenv("SMTP_SERVER")
# SMTP_PORT: int = os.getenv("SMTP_PORT")
# SMTP_USERNAME: str = os.getenv("SMTP_USERNAME")
# SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
SMTP_PASSWORD = "pskogjjdptkspguj"
SMTP_PORT = 587
SMTP_SERVER = "smtp.gmail.com"
SMTP_USERNAME = "ayushbhandarifor787@gmail.com"


@router.post("/send_email")
async def sendreport(
        name: str = Form(...),
        reg: str = Form(...),
        gender: str = Form(...),
        mail: str = Form(...),
        age: int = Form(...)
):
    try:
        print(mail)
        characters = string.ascii_letters + string.digits
        otp = ''.join(secrets.choice(characters) for _ in range(5))
        # server = smtplib.SMTP('smtp.gmail.com', 587, "ayushbhandarifor787@gmail.com", timeout=120)
        html_text = f'''<p>Dear <strong>{name},</strong></p>
                        <p>OTP to generate password for LuvHub platform is <strong>{otp}</strong></p>
                        <p>Thank You & Regards,<br>LuvHub Platform.</p>'''
        msg = MIMEMultipart()
        msg.attach(MIMEText(html_text, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('ayushbhandarifor787@gmail.com', 'iuoxmyerilueujex')
        server.sendmail('ayushbhandarifor787@gmail.com', mail, msg.as_string())
        print("Mail Sent")
        server.quit()
        return JSONResponse(content={"message": "Email sent successfully to all recipients"})
    except (smtplib.SMTPException, Exception) as e:
        # Handle other exceptions
        return JSONResponse(content={"error": f"Email sending error: {str(e)}"}, status_code=400)
