from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from fastapi import APIRouter, Body, Request, HTTPException
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter
from pydantic import BaseModel

router = APIRouter()


class FindMatch(BaseModel):
    name: str
    reg: str
    gender: str


@router.post("/find-match/")
async def find_match(
        request: FindMatch = Body(...)
):
    try:
        if not firebase_admin._apps:
            load_dotenv()
            cred = credentials.Certificate("static/credentials.json")
            firebase_admin.initialize_app(cred)

        db = firestore.client()

        user_query = db.collection("luvlist").where(filter=FieldFilter("reg", "==", request.reg.upper())).limit(1)
        user_result = user_query.stream()
        matched_users = []
        for user_doc in user_result:
            existing_crush_list = user_doc.to_dict().get('crushRegNumber', [])
            for crush_reg in existing_crush_list:
                crush_query = db.collection("luvlist").where(filter=FieldFilter("reg", "==", crush_reg)).limit(1)
                crush_result = crush_query.stream()
                for crush_doc in crush_result:
                    crush_name = crush_doc.to_dict().get('name', '')
                    crush_crush_list = crush_doc.to_dict().get('crushRegNumber', [])
                    if request.reg in crush_crush_list:
                        matched_users.append({
                            "crush_name": crush_name,
                            "crush_reg": crush_reg
                        })
        return JSONResponse(content={"matches": matched_users},
                            status_code=200)


    except Exception as e:
        error_msg = "error" + str(e)
        print(error_msg)
        return HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        firebase_admin.delete_app(firebase_admin.get_app())
