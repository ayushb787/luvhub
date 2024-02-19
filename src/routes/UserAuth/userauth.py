import datetime
from fastapi import Form, Request, HTTPException
from fastapi.responses import JSONResponse
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

router = APIRouter()



@router.post("/add_user/")
async def add_user(
        request: Request,
        name: str = Form(...),
        reg: str = Form(...),
        gender: str = Form(...),
        mail: str = Form(...),
        age: int = Form(...),
        password: str = Form(...)
):
    try:
        if not firebase_admin._apps:
            load_dotenv()
            cred = credentials.Certificate("static/credentials.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print(name, reg, gender, age, mail)

        # Check if a user with the same registration number already exists
        query = db.collection("users").where(filter=FieldFilter("reg", "==", reg.upper()))
        existing_user = query.get()

        if existing_user:
            return JSONResponse(content={"message": "User with similar registration number already exists"},
                                status_code=409)
        luv_dict = {'name': name.upper(), 'reg': reg.upper(), 'gender': gender.upper(), 'age': age, 'mail': mail, 'password': password,
                    'status': '0'}
        db.collection("users").add(luv_dict)

        return JSONResponse(content={"message": "Done"}, status_code=200)
    except Exception as e:
        error_msg = "error" + str(e)
        print(error_msg)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        firebase_admin.delete_app(firebase_admin.get_app())