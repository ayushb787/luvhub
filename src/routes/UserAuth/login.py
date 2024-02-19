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


@router.post("/login/")
async def login(
        request: Request,
        reg: str = Form(...),
        password: str = Form(...)
):
    try:
        if not firebase_admin._apps:
            load_dotenv()
            cred = credentials.Certificate("static/credentials.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print(reg)
        # Query the database for the user with the specified registration number
        user_query = db.collection("users").where(filter=FieldFilter("reg", "==", reg.upper())).limit(1)
        user_result = user_query.get()

        if not user_result:
            return JSONResponse(content={"message": "User not found"}, status_code=404)

        user_data = user_result[0].to_dict()

        # Check if the password matches
        if user_data.get("password") != password:
            return JSONResponse(content={"message": "Incorrect password"}, status_code=401)

        # # Check the status
        # status = user_data.get("status", "0")
        # if status == "0":
        #     firebase_admin.delete_app(firebase_admin.get_app())
        #     return JSONResponse(content={"message": "Not Verified"}, status_code=401)
        else:
            return JSONResponse(content={"message": "Login successful"}, status_code=200)

    except Exception as e:
        error_msg = "error" + str(e)
        print(error_msg)
        return HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        firebase_admin.delete_app(firebase_admin.get_app())
