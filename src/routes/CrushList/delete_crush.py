from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from fastapi import APIRouter, Form, Request, HTTPException
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter

router = APIRouter()


@router.post("/delete-crush/")
async def delete_crush(
        request: Request,
        name: str = Form(...),
        reg: str = Form(...),
        gender: str = Form(...),
        crushName: str = Form(...),
        crushRegNumber: str = Form(...)
):
    try:
        if not firebase_admin._apps:
            load_dotenv()
            cred = credentials.Certificate("static/credentials.json")
            firebase_admin.initialize_app(cred)

        db = firestore.client()
        user_query = db.collection("luvlist").where(filter=FieldFilter("reg", "==", reg.upper())).limit(1)
        user_result = user_query.stream()
        for user_doc in user_result:
            user_doc_ref = user_doc.reference
            existing_crush_list = user_doc.to_dict().get('crushRegNumber', [])
            if crushRegNumber not in existing_crush_list:
                return HTTPException(status_code=400,
                                    detail=f"Crush with reg number {crushRegNumber} not found in the list")
            existing_crush_list.remove(crushRegNumber)
            user_doc_ref.update({
                'crushNames': existing_crush_list,
                'crushRegNumber': existing_crush_list
            })
            return JSONResponse(content={"message": f"Crush Deleted Successfully"},
                                status_code=200)
        else:
            return HTTPException(status_code=400, detail=f"User with reg number {reg} not found in the database")

    except Exception as e:
        error_msg = "error" + str(e)
        print(error_msg)
        return HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        firebase_admin.delete_app(firebase_admin.get_app())