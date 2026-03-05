import asyncio
from typing import AsyncGenerator, Tuple

#=================== Agent interaction =================
async def process_qa(msg_format: str, content: str) -> str:
    """Xử lý trạm QA """
    if msg_format == "audio":
        # Giả lập tgian gọi S2T
        await asyncio.sleep(0.5)
        return "Đây là câu trả lời text được giải mã từ audio của sinh viên."
    return content

async def mock_llm_stream(user_text: str) -> AsyncGenerator[str, None]:
    """Giả lập LLM suy nghĩ và trả về từng chữ"""
    await asyncio.sleep(0.3) 

    # Giả lập 1 câu trả lời của LLM
    response_chunks = ["Chào bác sĩ, ", "tôi ", "cảm thấy ", "đau nhức ", "ở vùng ", "trán."]
    
    for chunk in response_chunks:
        await asyncio.sleep(0.1)
        yield chunk

async def process_interview_streaming(msg_format: str, content: str) -> Tuple[str, AsyncGenerator[str, None]]:
    """Xử lý trạm Interview"""
    
    # S2t user hỏi
    if msg_format == "audio":
        await asyncio.sleep(0.5) 
        user_text = "Bác sĩ: Bác cho em hỏi bác đau ở đâu?"
    else:
        user_text = content

    # LLM sinh câu trả lời
    ai_reply_stream = mock_llm_stream(user_text)
    
    return user_text, ai_reply_stream
