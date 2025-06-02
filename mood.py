from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

_model = None

def set_model(model):
    global _model
    _model = model

# 定義輸入格式
class MoodChatInput(BaseModel):
    message: str

@router.post("/api/moodchat")
async def mood_chat_endpoint(input: MoodChatInput):
    if _model is None:
        return {"reply": "❌ AI 模型尚未初始化"}

    prompt = f"""
你是一位溫柔的 AI 心情陪伴者，使用者剛剛說了這句話：「{input.message}」。
請根據這段話判斷他的心情語氣，並給予一段同理、親切、溫暖的回應。
請使用中文，只說一句話，不超過 30 字，避免說教或命令口吻。
    """

    try:
        response = _model.generate_content(prompt)
        return {"reply": response.text.strip()}
    except Exception as e:
        print("❌ Gemini 回應錯誤：", e)
        return {"reply": "抱歉，AI 現在無法回應你的心情。"}

__all__ = ["router", "set_model"]
