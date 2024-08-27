from fastapi import Body, APIRouter
from fastapi.responses import JSONResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import secrets
import string
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter
from dotenv import load_dotenv

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


class SendEmail(BaseModel):
    name: str
    reg: str
    gender: str
    mail: str
    # password: str


@router.post("/send-email")
async def send_email(
        request: SendEmail = Body(...)
):
    try:
        if not firebase_admin._apps:
            load_dotenv()
            cred = credentials.Certificate("static/credentials.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print(request.name, request.reg, request.gender, request.mail)

        # Check if a user with the same registration number already exists in users db
        query = db.collection("users").where(filter=FieldFilter("reg", "==", request.reg.upper()))
        existing_user = query.get()
        if existing_user:
            return JSONResponse(content={"message": "User with similar registration number already exists."},
                                status_code=409)

        # delete existing otp in otp db for the current user
        query1 = db.collection("otp").where(filter=FieldFilter("reg", "==", request.reg.upper()))
        existing_users1 = query1.get()
        for user in existing_users1:
            user.reference.delete()

        # generate random otp
        characters = string.ascii_letters + string.digits
        otp = ''.join(secrets.choice(characters) for _ in range(5))

        # store otp in db
        luv_dict = {'name': request.name.upper(), 'reg': request.reg.upper(), 'gender': request.gender.upper(),
                    'mail': request.mail,
                    # 'password': request.password,
                    'otp': otp}
        db.collection("otp").add(luv_dict)

        # now send the otp to email
        print(request.mail)
        # server = smtplib.SMTP('smtp.gmail.com', 587, "ayushbhandarifor787@gmail.com", timeout=120)
        html_text = f'''<p>Dear <strong>{request.name},</strong></p>
                        <p>OTP to generate password for LuvHub platform is <strong>{otp}</strong></p>
                        <p>Thank You & Regards,<br>LuvHub Platform.</p>'''
        msg = MIMEMultipart()
        msg.attach(MIMEText(html_text, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('ayushbhandarifor787@gmail.com', 'iuoxmyerilueujex')
        server.sendmail('ayushbhandarifor787@gmail.com', request.mail, msg.as_string())
        print("Mail Sent")
        server.quit()
        return JSONResponse(content={"message": "Email sent successfully to all recipients"})
    except (smtplib.SMTPException, Exception) as e:
        # Handle other exceptions
        return JSONResponse(content={"error": f"Email sending error: {str(e)}"}, status_code=400)
