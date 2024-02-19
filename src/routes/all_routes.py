from fastapi import APIRouter

from src.routes.CrushList.addcrush import router as add_crush
from src.routes.UserAuth.userauth import router as user_auth
from src.routes.UserAuth.send_email import router as send_email
from src.routes.UserAuth.login import router as login
from src.routes.CrushList.delete_crush import router as delete_crush

router = APIRouter()

router.include_router(add_crush)
router.include_router(user_auth)
router.include_router(send_email)
router.include_router(login)
router.include_router(delete_crush)