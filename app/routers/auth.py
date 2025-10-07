from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from starlette.config import Config
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from app.core.database import get_session
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.user import UserCreate, UserRead
from app.crud.user import get_or_create_user
from app.utils.jwt import create_jwt

config = Config('.env')
oauth = OAuth(config)

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

router = APIRouter()


@router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/auth')
async def auth(request: Request, session: Session = Depends(get_session)):
    # Step 1: Get token from Google
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get("userinfo")
    print(userinfo)
    if not userinfo:
        return JSONResponse({"error": "Failed to get user info from Google"}, status_code=400)

    # Step 2: Map to UserCreate schema
    user_data = UserCreate(
        name=userinfo["name"],
        email=userinfo["email"],
        image=userinfo.get("picture")
    )

    # Step 3: Get or create user in DB
    user = get_or_create_user(user_data, session)

    # Step 4: Generate JWT
    jwt_token = create_jwt(user.id)

    # Step 5: Return JSON to frontend
    return {
        "token": jwt_token,
        "user": UserRead.model_validate(user)
    }
