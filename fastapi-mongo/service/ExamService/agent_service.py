import asyncio
from typing import AsyncGenerator, Tuple

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

async def mock_evaluate_station(station_id: str, station_type: str, user_data: dict) -> dict:
    print(f"Đang đánh giá trạm {station_id}")
    await asyncio.sleep(3)  # tgian đánh giá

    mock_score = 100

    if station_type == "patient_interview" or station_type == "medical_advice":
        feedback = "Nội dung đánh giá trạm phỏng vấn bệnh nhân"
    else:
        feedback = "Nội dung đánh giá trạm QA"

    return {
        "score": mock_score,
        "evaluation": feedback
    }

async def mock_evaluate_exam(session_id: str, list_station_results: list) -> dict:
    print(f"Đang đánh giá bài thi {session_id}")
    await asyncio.sleep(4)  # tgian đánh giá

    total_score = 100

    overall_feedback = "Nội dung đánh giá tổng thể kỳ thi"

    return {
        "score": total_score,
        "overall_evaluation": overall_feedback
    }