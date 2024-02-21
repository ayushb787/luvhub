from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from fastapi import APIRouter, Body, Request, HTTPException
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter
from pydantic import BaseModel

router = APIRouter()


class GetCrushList(BaseModel):
    name: str
    reg: str
    gender: str


@router.post("/get-crush-list/")
async def get_crush_list(
        request: GetCrushList = Body(...)
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
        existing_crush_list_reg = []
        existing_crush_list_names = []
        # Assuming there is only one document in the result (for the given reg number)
        for user_doc in user_result:
            user_doc_ref = user_doc.reference
            existing_crush_list_reg.append(user_doc.to_dict().get('crushRegNumber', []))
            existing_crush_list_names.append(user_doc.to_dict().get('crushNames', []))

        return JSONResponse(content={"message": f"Fetched Crush List", "crushlistregno": existing_crush_list_reg,
                                     "crushlistnames": existing_crush_list_names},
                            status_code=200)

    except Exception as e:
        error_msg = "error" + str(e)
        print(error_msg)
        return HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        firebase_admin.delete_app(firebase_admin.get_app())
