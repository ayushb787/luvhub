from fastapi import Body, Form, Request, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    reg: str
    password: str


@router.post("/login/")
async def login(
        request: LoginRequest = Body(...)
):
    try:
        print(request.reg.upper())
        if not firebase_admin._apps:
            load_dotenv()
            cred = credentials.Certificate("static/credentials.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print(request.reg)
        # Query the database for the user with the specified registration number
        user_query = db.collection("users").where(filter=FieldFilter("reg", "==", request.reg.upper())).limit(1)
        user_result = user_query.get()

        if not user_result:
            return JSONResponse(content={"message": "User not found"}, status_code=404)

        user_data = user_result[0].to_dict()

        # Check if the password matches
        if user_data.get("password") != request.password:
            return JSONResponse(content={"message": "Incorrect password"}, status_code=401)

        # # Check the status
        # status = user_data.get("status", "0")
        # if status == "0":
        #     firebase_admin.delete_app(firebase_admin.get_app())
        #     return JSONResponse(content={"message": "Not Verified"}, status_code=401)
        else:
            user_query = db.collection("users").where(filter=FieldFilter("reg", "==", request.reg.upper())).limit(1)
            user_result = user_query.get()
            name = ''
            gender = ''
            reg = ''
            for doc in user_result:
                # Access the 'name' field
                name = doc.get('name')
                gender = doc.get('gender')
                reg = doc.get('reg')
            return JSONResponse(content={"message": f"Login successfully", "reg": reg, "name": name, 'gender': gender},
                                status_code=200)

    except Exception as e:
        error_msg = "error" + str(e)
        print(error_msg)
        return HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        firebase_admin.delete_app(firebase_admin.get_app())
