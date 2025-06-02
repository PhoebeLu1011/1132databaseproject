import asyncio
import datetime
from google import generativeai as genai
from dotenv import load_dotenv
import os
import pandas as pd

# 設定環境變數 & Gemini API Key
load_dotenv()
gemini_api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# 1. 用 input() 互動輸入病歷資料（回傳 dict）
def collect_medical_record():
    name = input("請輸入姓名：").strip()
    age = input("請輸入年齡：").strip()
    gender = input("請輸入性別（男/女）：").strip()
    symptoms = input("請描述目前的症狀或不適：").strip()
    history = input("有沒有過去的重大病史？").strip()
    habits = input("請描述你的生活習慣（如：抽菸、喝酒、運動）：").strip()
    medicine = input("現在有沒有在服用什麼藥物？").strip()
    doctor_diagnosis = input("醫生有診斷什麼病嗎？").strip()
    special_notes = input("有沒有特別需要注意的事項？").strip()

    medical_record = f"""
姓名：{name}
年齡：{age}
性別：{gender}
症狀：{symptoms}
既往病史：{history}
生活習慣：{habits}
目前用藥：{medicine}
醫師診斷：{doctor_diagnosis}
特別注意事項：{special_notes}
"""
    return {
        "name": name,
        "age": age,
        "gender": gender,
        "record_text": medical_record
    }

# 2. 呼叫 Gemini 生成建議
async def ask_ai_agent(medical_record):
    prompt = f"""
依據下列病歷，請分成兩大部分：
1. 飲食建議（簡單列出早餐、午餐、晚餐）
2. 復健運動（每天建議1-2次，包含步驟與注意事項）

病歷內容：
{medical_record}
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# 3. 將 AI 建議轉成行事曆事件（目前沒用到）
def parse_to_events(plan_text):
    today = datetime.date.today()
    events = []
    events.append((f"早餐提醒：{plan_text}", today, "07:00"))
    events.append((f"午餐提醒：{plan_text}", today, "12:00"))
    events.append((f"晚餐提醒：{plan_text}", today, "18:00"))
    events.append((f"復健運動提醒：{plan_text}", today, "20:00"))
    return events

# 4. 主流程
async def main():
    patient = collect_medical_record()
    ai_reply = await ask_ai_agent(patient["record_text"])

    print("\n✅ Gemini AI 建議：\n")
    print(ai_reply)

    df = pd.DataFrame([{
        "姓名": patient["name"],
        "年齡": patient["age"],
        "性別": patient["gender"],
        "病歷內容": patient["record_text"],
        "Gemini建議": ai_reply
    }])
    df.to_csv("suggestion.csv", index=False, encoding="utf-8-sig")

    print("\n✅ 已儲存建議到 suggestion.csv")

# 5. 執行程式
if __name__ == "__main__":
    asyncio.run(main())
