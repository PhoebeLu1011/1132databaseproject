from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()


router = APIRouter()

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# 🛠️ 新增記憶使用者登入（存在 cookie）
@router.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    print("🔐 token:", token)

    # ✨ 無論有沒有 id_token，都 fallback 到 userinfo
    try:
        user_info = await oauth.google.parse_id_token(request, token)
    except Exception as e:
        print("⚠️ parse_id_token 失敗，改用 userinfo()", e)
        user_info = await oauth.google.userinfo(token=token)

    print("👤 user_info:", user_info)

    email = user_info.get("email")
    response = RedirectResponse(url="/main.html")
    response.set_cookie(key="user_email", value=email, httponly=True)
    return response

@router.get("/login")
async def login(request: Request):
    redirect_uri = "http://127.0.0.1:8000/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)
