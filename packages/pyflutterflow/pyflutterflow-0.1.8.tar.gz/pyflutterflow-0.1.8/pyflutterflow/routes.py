from fastapi import APIRouter, Depends, UploadFile, File
from starlette.responses import FileResponse
from pyflutterflow.logs import get_logger
from pyflutterflow.auth import set_user_role, get_users_list, get_current_user
from pyflutterflow.database.supabase.supabase_functions import proxy, proxy_with_body
from pyflutterflow.services.cloudinary_service import CloudinaryService

logger = get_logger(__name__)

router = APIRouter(
    prefix='',
    tags=['Pyflutterflow internal routes'],
)


@router.get("/configure")
async def serve_vue_config():
    file_path = "admin_config.json"
    return FileResponse(file_path)


@router.post("/create-admin", dependencies=[Depends(set_user_role)])
async def create_admin():
    pass


@router.get("/admin/users")
async def get_users(users: list = Depends(get_users_list)):
    # TODO users pagination
    return users


@router.get("/supabase/{path:path}")
async def supabase_get_proxy(response = Depends(proxy)):
    return response


@router.post("/supabase/{path:path}")
async def supabase_post_proxy(response = Depends(proxy_with_body)):
    return response


@router.patch("/supabase/{path:path}")
async def supabase_update_proxy(response = Depends(proxy_with_body)):
    return response


@router.delete("/supabase/{path:path}")
async def supabase_delete_proxy(response = Depends(proxy)):
    return response


@router.post("/cloudinary-upload", dependencies=[Depends(get_current_user)])
async def cloudinary_upload(image: UploadFile = File(...)):
    cloudinary_service = CloudinaryService(image.file)
    return await cloudinary_service.upload_to_cloudinary()
