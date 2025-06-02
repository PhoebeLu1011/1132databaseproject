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
只說一句話，不超過 30 字，避免說教或命令口吻。
(如果使用者輸入英文請用英文回應，如果用繁體中文回應請用繁體中文回應，如果兩者語言皆有，用使用比例較多的語言回應，如果是其他外文，一律用英文回應)
    """

    try:
        response = _model.generate_content(prompt)
        return {"reply": response.text.strip()}
    except Exception as e:
        print("❌ Gemini 回應錯誤：", e)
        return {"reply": "抱歉，AI 現在無法回應你的心情。"}
    
# 回覆格式
class ChatInput(BaseModel):
    message: str
    
@router.post("/api/chat")
async def chat_endpoint(input: ChatInput):
    try:
        # 可以根據需要微調提示詞
        prompt = (
            "你是 MediMate 健康管理 App 的 AI 助理，請用簡單清楚的方式回答與此 App 相關的問題。(如果使用者輸入英文請用英文回應(包括hi/hello)，如果用繁體中文回應請用繁體中文回應，如果兩者語言皆有，用使用比例較多的語言回應，如果是其他外文，一律用英文回應)"
            "像是功能操作、輸入健康紀錄、查看報告、個人資訊設定等。\n\n"
            "(編輯)註冊資料: 進入到右上角有一個人像的圖像，點下去之後可以查看自己的資料與修改個人資料"
            "輸入健康紀錄:右上寫著Enter Medical Infor的按鈕按下去就可以輸入"
            "查看ai生成的建議(Wellness Dashboard):點下左下角的Wellness Dashboard紫色按鈕，可以看到每天針對疾病或傷害的復健建議或是飲食菜單"
            "記錄(輸入或查看)心情(心得): 點下右下角的紫色按鈕就可以輸入或查看心情心得"
            "想找人聊天: 就找左上角的ai聊天機器人吧"
            f"使用者提問：{input.message}"
        )

        response = _model.generate_content(prompt)

        return {"reply": response.text}

    except Exception as e:
        print(e)
        return {"reply": "抱歉，AI 目前無法回應。"}
    


__all__ = ["router", "set_model"]