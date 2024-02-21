from fastapi import Form, Body, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter
from pydantic import BaseModel

router = APIRouter()


class SignupRequest(BaseModel):
    name: str
    reg: str
    gender: str
    mail: str
    password: str


@router.post("/add-user/")
async def add_user(
        request: SignupRequest = Body(...)
):
    try:
        if not firebase_admin._apps:
            load_dotenv()
            cred = credentials.Certificate("static/credentials.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print(request.name, request.reg, request.gender, request.mail)

        # Check if a user with the same registration number already exists
        query = db.collection("users").where(filter=FieldFilter("reg", "==", request.reg.upper()))
        existing_user = query.get()

        if existing_user:
            return JSONResponse(content={"message": "User with similar registration number already exists"},
                                status_code=409)
        luv_dict = {'name': request.name.upper(), 'reg': request.reg.upper(), 'gender': request.gender.upper(),
                    'mail': request.mail,
                    'password': request.password,
                    'status': '0'}
        db.collection("users").add(luv_dict)

        return JSONResponse(content={"message": "Done"}, status_code=200)
    except Exception as e:
        error_msg = "error" + str(e)
        print(error_msg)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        firebase_admin.delete_app(firebase_admin.get_app())
