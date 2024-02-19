from fastapi import APIRouter

from src.routes.addEntry.addcrush import router as add_crush
from src.routes.UserAuth.userauth import router as user_auth
from src.routes.UserAuth.send_email import router as send_email
from src.routes.UserAuth.login import router as login

router = APIRouter()

router.include_router(add_crush)
router.include_router(user_auth)
router.include_router(send_email)
router.include_router(login)