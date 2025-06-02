from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

os.makedirs("records", exist_ok=True)

class FormData(BaseModel):
    date: str
    q1: str
    q2: str
    q3: str
    q4: str
    q5: str
    q6: str
    q7: str

@app.post("/submit_entry")
def submit(data: FormData):
    try:
        # 讀取舊資料，如果沒有就建立空 list
        if os.path.exists("records.json"):
            with open("records.json", "r", encoding="utf-8") as f:
                records = json.load(f)
        else:
            records = []

        # 新資料 append 進去
        records.append(data.dict())

        # 寫回去
        with open("records.json", "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

        return {"status": "success"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
