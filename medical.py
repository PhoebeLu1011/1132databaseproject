from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

@app.get("/medical_entry")
def show_last_entry():
    try:
        with open("records.json", "r", encoding="utf-8") as f:
            records = json.load(f)

        sorted_records = sorted(
            records,
            key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),
            reverse=True
        )

        return {
            "status": "success",
            "data": datasorted_records
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": "沒有找到資料"
        }
