from fastapi import APIRouter, Body
from pydantic import BaseModel
import json
import datetime

# Router 建立
router = APIRouter()

# 模型儲存（由 main.py 傳入）
_model = None

def set_model(model):
    global _model
    _model = model

# 表單資料模型
class FormData(BaseModel):
    date: str
    q1: str
    q2: str
    q3: str
    q4: str
    q5: str
    q6: str
    q7: str

# 儲存輸入資料
@router.post("/submit_entry")
def submit(data: FormData):
    with open("last_input.json", "w", encoding="utf-8") as f:
        json.dump(data.dict(), f, ensure_ascii=False)
    return {"status": "success"}

# 產生健康建議
@router.post("/api/wellness/summary")
def get_summary(record: dict = Body(...)):
    if _model is None:
        return {"error": "❌ AI 模型尚未初始化，請稍後再試"}

    print("✅ 收到使用者傳來的紀錄")
 
    record_text = f"""
年齡：{record['q7']}
病症：{record['q1']}
病史：{record['q2']}
生活習慣：{record['q3']}
用藥：{record['q4']}
診斷：{record['q5']}
注意事項：{record['q6']}
"""

    print("📤 要送出給 Gemini 了")


    result = generate_daily_health_summary({
        "record_text": record_text,
        "date": record["date"]
    })

    return result

class HealthAgent:
    def __init__(self, model):
        self.model = model
        self.memory = {}

    def analyze_medical_record(self, record_text):
        """Step 1: 解析病歷摘要"""
        prompt = f"""
請閱讀以下病歷資料，摘要出關鍵健康問題或症狀，不超過100字：，(如果使用者輸入英文請用英文回應，如果用繁體中文回應請用繁體中文回應，如果兩者語言皆有，用使用比例較多的語言回應，如果是其他外文，一律用英文回應)
{record_text}
"""
        response = self.model.generate_content(prompt)
        self.memory['record_summary'] = response.text.strip()
        return self.memory['record_summary']

    def generate_diet_plan(self, record_summary):
        """Step 2: 給出飲食建議"""
        prompt = f"""
請針對以下健康摘要，給出今日的飲食建議，分成 早餐、午餐、晚餐，幾大卡，多少量，怎麼製作烹飪，一餐控制在100字左右：
{record_summary}
"""
        response = self.model.generate_content(prompt)
        self.memory['diet_plan'] = response.text.strip()
        return self.memory['diet_plan']

    def generate_exercise_plan(self, record_summary):
        """Step 3: 給出運動建議"""
        prompt = f"""
請針對以下健康摘要，建議1~2項適合的運動，詳細幾分鐘，如何做，操作步驟，一項控制在100字左右：
{record_summary}
"""
        response = self.model.generate_content(prompt)
        self.memory['exercise_plan'] = response.text.strip()
        return self.memory['exercise_plan']

    def generate_extra_tips(self, record_summary):
        """Step 4: 額外提醒"""
        prompt = f"""
請針對以下健康摘要，提出1項額外健康提醒：
{record_summary}
"""
        response = self.model.generate_content(prompt)
        self.memory['extra_tips'] = response.text.strip()
        return self.memory['extra_tips']

    def generate_full_summary(self):
        """組合所有建議，生成完整總結"""
        diet_plan = self.memory['diet_plan'].replace('\n', '<br>')
        exercise_plan = self.memory['exercise_plan'].replace('\n', '<br>')
        extra_tips = self.memory['extra_tips'].replace('\n', '<br>')
        return f"""
【今日健康建議】<br><br>
🔹 飲食建議：<br>
{diet_plan}<br><br>
🔹 運動建議：<br>
{exercise_plan}<br><br>
🔹 額外提醒：<br>
{extra_tips}<br><br>
"""

    def run(self, record_text):
        """Agent完整流程"""
        self.analyze_medical_record(record_text)
        self.generate_diet_plan(self.memory['record_summary'])
        self.generate_exercise_plan(self.memory['record_summary'])
        self.generate_extra_tips(self.memory['record_summary'])

        return self.generate_full_summary()

# --- 你的使用方式不變 ---
def generate_daily_health_summary(record):
    record_text = record.get("record_text", "")
    summary_date = record.get("date", datetime.date.today().isoformat())

    agent = HealthAgent(_model)
    summary_text = agent.run(record_text)

    return {
        "date": summary_date,
        "summary": summary_text
    }

# 顯示最新輸入紀錄
@router.get("/medical_entry")
def show_last_entry():
    try:
        with open("last_input.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "status": "success",
            "data": data
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": "沒有找到資料"
        }

__all__ = ["router", "set_model"]