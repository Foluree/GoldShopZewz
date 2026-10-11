from fastapi import APIRouter, Request, Depends, Form, status, UploadFile, File
from pathlib import Path
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import uuid
from sqlalchemy import select, delete
#from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from app.main_title_router import templates
#from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd_and_config.postgres_engine import get_session
#from app.models.profile_model import UserProfiles
from app.bd_request.local_profile_request import (_load_first_exito,
                                                    response_ho,
                                                    purchase_se,
                                                    response_hos,
                                                    purchase_ses,
                                                    load_auth_user,
                                                    get_username_from_email,
                                                    update_user_profile,
                                                    load_profile_purchases,
                                                    get_or_create_user_profile,
                                                    delete_profile_purchase)
from app.bd_request.hased_password.hased_cookie import verify_accses_token
from app.profil.appeal_dialog import load_user_dialogs
from app.models.profile_model import ImageUploadOut, UserImages
import shutil

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)


UPLOAD_ROOT = Path('/app/image')

MAX_SIZE = (1920, 1080)

ALLOWED_EXT = ('.jpg', '.jpeg', '.png', '.webp')

EXT_TO_FORMAT = {
    '.jpg': 'JPEG',
    '.jpeg': 'JPEG',
    '.png': 'PNG',
    '.webp': 'WEBP',
}


async def delete_all_profile_images(session, user_id: int) -> list[str]:
    rows = await session.execute(
        select(UserImages).where(UserImages.user_id == user_id)
    )
    images = rows.scalars().all()
    paths = [img.path for img in images]

    if images:
        await session.execute(
            delete(UserImages).where(UserImages.user_id == user_id)
        )
        await session.commit()

    return paths

def slugify(value: str) -> str:
    cleaned = ''.join(
        c if (c.isalnum() or c in '-_') else '-'
        for c in value.strip().lower()
    )
    return cleaned or "user"

async def _get_auth_user_or_redirect(requesto: Request, session: AsyncSession = Depends(get_session)):
    token = requesto.cookies.get("booking_accses_token")
    user_id = verify_accses_token(token)
    if not user_id:
        return None

    auth_user = await load_auth_user(session, int(user_id))

    return auth_user

@router.get("", response_class=HTMLResponse)
async def profile(requesto: Request, session: AsyncSession = Depends(get_session)):
    auth_user = await _get_auth_user_or_redirect(requesto, session)
    if not auth_user:
        return RedirectResponse(url="/regist/", status_code=303)

    user = await get_or_create_user_profile(session, auth_user["email_us"])
    user["purchasesAll"] = await load_profile_purchases(session, user["id"])

    dialogs = await load_user_dialogs(session, user['id'])

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": requesto,
            "profile": user,
            "saved": requesto.query_params.get('saved') == "1",
            'dialogs': dialogs,
            'dialogs_new': sum(1 for dialog in dialogs if dialog['awaiting_user']),
        }
    )

@router.post("", response_class=HTMLResponse)
async def update_profile(
    requesto: Request,
    full_name: str = Form(""),
    city: str = Form(""),
    session: AsyncSession = Depends(get_session),
):
    auth_user = await _get_auth_user_or_redirect(requesto, session)
    if not auth_user:
        return RedirectResponse(url="/regist/", status_code=303)

    await get_or_create_user_profile(session, auth_user["email_us"])
    await update_user_profile(session, auth_user["email_us"], full_name, city)

    return RedirectResponse(url="/profile?saved=1", status_code=303)

@router.delete("/purchases/{purchase_id}")
async def cancel_purchase(
    purchase_id: int,
    requesto: Request,
    session: AsyncSession = Depends(get_session),
):
    auth_user = await _get_auth_user_or_redirect(requesto, session)
    if not auth_user:
        return JSONResponse({"detail": "not authenticated"}, status_code=401)

    user = await get_or_create_user_profile(session, auth_user["email_us"])
    deleted = await delete_profile_purchase(session, user["id"], purchase_id)
    if not deleted:
        return JSONResponse({"detail": "purchase not found"}, status_code=404)

    return JSONResponse({"deleted": True})

@router.post('/images', response_model=ImageUploadOut, status_code=status.HTTP_201_CREATED)
async def upload_user_image(
    request: Request,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    auth_user = await _get_auth_user_or_redirect(request, session)
    if not auth_user:
        return RedirectResponse(url='/regist/', status_code=303)

    user = await get_or_create_user_profile(session, auth_user['email_us'])

    ext = Path(file.filename or '').suffix.lower()
    if ext not in ALLOWED_EXT:
        return RedirectResponse(url='/profile/', status_code=303)

    content = await file.read()
    try:
        img = Image.open(BytesIO(content))
        img.load()
    except (UnidentifiedImageError, OSError):
        return RedirectResponse(url='/profile/', status_code=303)

    if img.width > MAX_SIZE[0] or img.height > MAX_SIZE[1]:
        img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)

    user_folder_name = slugify(user['full_name'] or f'user_{user['id']}')
    folder = UPLOAD_ROOT / user_folder_name
    folder.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    full_path = folder / filename

    pil_format = EXT_TO_FORMAT[ext]
    save_kwargs = {}
    if pil_format in {"JPEG", "WEBP"}:
        save_kwargs.update(quality=90, optimize=True)
    if pil_format == 'JPEG' and img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    img.save(full_path, format=pil_format, **save_kwargs)

    db_path = f'/app/image/{user_folder_name}/{filename}'
    db_image = UserImages(path=db_path, user_id=user['id'])
    session.add(db_image)
    await session.commit()
    await session.refresh(db_image)

    return RedirectResponse(url='/profile?saved=1', status_code=303)

@router.get('/images_all_url', response_model=list[ImageUploadOut])
async def list_my_images(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    auth_user = await _get_auth_user_or_redirect(request, session)
    if not auth_user:
        return JSONResponse({'detail': 'not authenticated'}, status_code=401)

    user = await get_or_create_user_profile(session, auth_user['email_us'])

    rows = await session.execute(
        select(UserImages)
        .where(UserImages.user_id == user['id'])
        .order_by(UserImages.id.desc())
    )
    images = rows.scalars().all()

    return [
        {
            'id': img.id,
            'path': img.path,
            'url': f'/static/images/{img.path.split("/app/images", 1)[-1]}'
        } for img in images
    ]


@router.delete('/images')
async def delete_all_my_images(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    auth_user = await _get_auth_user_or_redirect(request, session)
    if not auth_user:
        return JSONResponse({'detail': 'not authenticated'}, status_code=401)

    user = await get_or_create_user_profile(session, auth_user['email_us'])

    paths = await delete_all_profile_images(session, user['id'])

    for p in paths:
        try:
            file_path = Path(p).resolve()
            if UPLOAD_ROOT.resolve() not in file_path.parents:
                continue
            file_path.unlink(missing_ok=True)
        except OSError:
            pass

    user_folder_name = slugify(user['full_name'] or f'user_{user['id']}')
    user_folder = UPLOAD_ROOT / user_folder_name
    if user_folder.exists:
        shutil.rmtree(user_folder, ignore_errors=True)

    return JSONResponse({'delete': True, 'count': len(paths)})

async def delete_profile_image(session, user_id: int, image_id: int) -> str | None:
    row = await session.execute(
        select(UserImages).where(
            UserImages.id == image_id,
            UserImages.user_id == user_id,
        )
    )
    image = row.scalar_one_or_none()
    if image is None:
        return None

    path = image.path
    await session.delete(image)
    await session.commit()
    return path

@router.delete('/images_del_by_id/{image_id}')
async def delete_my_image(
    image_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    auth_user = await _get_auth_user_or_redirect(request, session)
    if not auth_user:
        return JSONResponse({'delail': "not authenticated"}, status_code=401)

    
    user = await get_or_create_user_profile(session, auth_user['email_us'])

    path = await delete_profile_image(session, user['id'], image_id)
    if path is None:
        return JSONResponse({'detail': 'image not found'}, status_code=404)

    try:
        file_path = Path(path).resolve()
        if UPLOAD_ROOT.resolve() in file_path.parents:
            file_path.unlink(missing_ok=True)
    except OSError:
        pass

    return JSONResponse({'deleted': True, 'id': image_id, 'path': path})