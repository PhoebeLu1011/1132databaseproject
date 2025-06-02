from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

# === 新增模型相關 ===
from google import generativeai as genai
from wellness import router as wellness_router, set_model as wellness_set_model
from mood import router as mood_router, set_model as mood_set_model
# ===================

from sign import router as sign_router

# 載入環境變數
load_dotenv()

# 建立主 app
app = FastAPI()

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET"))


# === 初始化共享模型 ===
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
shared_model = genai.GenerativeModel("gemini-2.0-flash")
wellness_set_model(shared_model)
mood_set_model(shared_model)

# === 註冊 router ===
app.include_router(sign_router)
app.include_router(wellness_router)
app.include_router(mood_router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

