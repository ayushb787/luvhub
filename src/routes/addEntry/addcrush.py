import datetime

from dotenv import load_dotenv
from fastapi import APIRouter, Form
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import json

from google.cloud.firestore_v1 import FieldFilter

templates = Jinja2Templates(directory="templates")  # Directory where your HTML templates are located

router = APIRouter()


@router.get("/add_luv")
def open_luv(request: Request):
    return templates.TemplateResponse('/LuvList/add_luv.html', {"request": request})


@router.post("/add_luv/")
async def upload_luv(
        request: Request,
        name: str = Form(...),
        reg: str = Form(...),
        gender: str = Form(...),
        studyYear: int = Form(...),
        crushName: list[str] = Form(...),
        crushRegNumber: list[str] = Form(...)
):
    try:
        load_dotenv()
        # firebase_project_id = os.environ.get("PROJECT_ID")
        # firebase_project_key_id = os.environ.get("PROJECT_KEY_ID")
        # firebase_private_key = os.environ.get("PRIVATE_KEY").replace('\\n', '\n')
        # firebase_client_email = os.environ.get("CLIENT_EMAIL")
        # cred = credentials.Certificate({
        #     "type": os.environ.get("TYPE"),
        #     "project_id": firebase_project_id,
        #     "private_key_id": firebase_project_key_id,
        #     "private_key": firebase_private_key,
        #     "client_email": firebase_client_email,
        #     "client_id": os.environ.get("CLIENT_ID"),
        #     "auth_uri": os.environ.get("AUTH_URI"),
        #     "token_uri": os.environ.get("TOKEN_URI"),
        #     "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_URI"),
        #     "client_x509_cert_url": os.environ.get("CLIENT_URI"),
        # })

        cred = credentials.Certificate("static/credentials.json")
        firebase_admin.initialize_app(cred)

        db = firestore.client()
        print(name);
        # for item in data:
        #     print(item)
        #     existing_docs = (
        #         db.collection("vanlist")
        #         # .where(filter=FieldFilter("date", "==", item["date"]))
        #         # .where(filter=FieldFilter("route", "==", item["route"]))
        #         # .where(filter=FieldFilter("customer", "==", item["customer"]))
        #         .where(filter=FieldFilter("ra_bill_no", "==", item["ra_bill_no"]))
        #         .where(filter=FieldFilter("at_bill_no", "==", item["at_bill_no"]))
        #         .stream()
        #     )
        luv_dict = {'name':name, 'reg':reg, 'gender': gender, 'studyYear':studyYear, 'crushNames':crushName, 'crushRegNumber': crushRegNumber}
        db.collection("luvlist").add(luv_dict)

        firebase_admin.delete_app(firebase_admin.get_app())
        return templates.TemplateResponse('/Notifications/success.html',
                                          {"request": request, "success_header": "Luv Added "
                                                                                 "Successfully!!",
                                           "success_msg": "Luv List has been added to your firebase account. Thankyou "
                                                          "for using our service!!!"})

    except Exception as e:
        error_msg = "error" + str(e)
        print(error_msg)
        return templates.TemplateResponse('/Notifications/error.html',
                                          {"request": request, "error_msg": error_msg})
