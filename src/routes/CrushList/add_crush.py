from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from fastapi import APIRouter, Form, Request, HTTPException
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter

router = APIRouter()


@router.post("/add-crush/")
async def upload_luv(
        request: Request,
        name: str = Form(...),
        reg: str = Form(...),
        gender: str = Form(...),
        crushName: list[str] = Form(...),
        crushRegNumber: list[str] = Form(...)
):
    try:
        if not firebase_admin._apps:
            load_dotenv()
            cred = credentials.Certificate("static/credentials.json")
            firebase_admin.initialize_app(cred)

        db = firestore.client()

        # Check if the user with the provided reg number already has a crush list
        user_query = db.collection("luvlist").where(filter=FieldFilter("reg", "==", reg.upper())).limit(1)
        user_result = user_query.stream()

        # Assuming there is only one document in the result (for the given reg number)
        for user_doc in user_result:
            user_doc_ref = user_doc.reference
            existing_crush_list = user_doc.to_dict().get('crushRegNumber', [])

            # Check if any of the provided crushRegNumber is already in the existing list
            for crush_reg, crush_name in zip(crushRegNumber, crushName):
                if crush_reg in existing_crush_list:
                    return HTTPException(status_code=400, detail=f"Crush {crush_name} already exists in the list")

            # If the code reaches here, it means the user can add the new crush details to the list
            user_doc_ref.update({
                'crushNames': existing_crush_list + crushName,
                'crushRegNumber': existing_crush_list + crushRegNumber
            })

        else:
            # If the user does not exist in the database, create a new entry
            luv_dict = {'name': name, 'reg': reg, 'gender': gender, 'crushNames': crushName,
                        'crushRegNumber': crushRegNumber}
            db.collection("luvlist").add(luv_dict)


        return JSONResponse(content={"message": f"Crush List Added Successfully"},
                            status_code=200)

    except Exception as e:
        error_msg = "error" + str(e)
        print(error_msg)
        return HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        firebase_admin.delete_app(firebase_admin.get_app())