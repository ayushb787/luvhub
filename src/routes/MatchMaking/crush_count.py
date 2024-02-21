from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from fastapi import APIRouter, Body, Request, HTTPException
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter
from pydantic import BaseModel
router = APIRouter()

class CrushCount(BaseModel):
    name: str
    reg: str
    gender: str

@router.post("/crush-count/")
async def crush_count(
        request: CrushCount = Body(...)
):
    try:
        if not firebase_admin._apps:
            load_dotenv()
            cred = credentials.Certificate("static/credentials.json")
            firebase_admin.initialize_app(cred)

        db = firestore.client()

        # Check if the user with the provided reg number already has a crush list
        user_query = db.collection("luvlist").where(filter=FieldFilter("reg", "==", request.reg.upper())).limit(1)
        user_result = user_query.stream()
        crush_count = 0
        all_users_query = db.collection("luvlist").stream()

        for user_doc in all_users_query:
            existing_crush_list = user_doc.to_dict().get('crushRegNumber', [])

            if request.reg in existing_crush_list:
                crush_count += 1

        return JSONResponse(content={"crush_count": crush_count},
                            status_code=200)

    except Exception as e:
        error_msg = "error" + str(e)
        print(error_msg)
        return HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        firebase_admin.delete_app(firebase_admin.get_app())