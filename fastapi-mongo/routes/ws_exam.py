from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
import json
import asyncio
from beanie import PydanticObjectId
from auth.jwt_handler import decode_jwt

from database.database import retrieve_station, add_message
from models.message import Message

from service.ExamService.agent_service import process_interview_streaming, process_qa

router = APIRouter()

@router.websocket("/{session_id}/{station_id}")
async def exam_websocket_endpoint(websocket: WebSocket, session_id: str, station_id: str, token: str = Query(None)):
    await websocket.accept()

    if token is None:
        await websocket.send_json({"error": "Token xác thực không được cung cấp"})
        await websocket.close(code=1008)
        return
    
    user_data = decode_jwt(token)
    if not user_data:
        await websocket.send_json({"error": "Token xác thực không hợp lệ"})
        await websocket.close(code=1008)
        return
    
    try:
        station = await retrieve_station(PydanticObjectId(station_id))
        if not station:
            await websocket.send_json({"error": "Không tìm thấy trạm thi"})
            await websocket.close(code=1008)
            return
    except Exception:
        await websocket.send_json({"error": "ID trạm thi không hợp lệ"})
        await websocket.close(code=1008)
        return

    station_type = station.type

    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            
            msg_format = data.get("type") 
            content = data.get("content")
            question_id = data.get("question_id")

            if station_type == "patient_interview" or station_type == "medical_advice":
                # Gọi Service để lấy câu của User và Dialog-gen luồng trả lời của AI
                user_text, ai_reply_stream = await process_interview_streaming(msg_format, content)
                
                asyncio.create_task(add_message(Message(
                    sender=session_id, recipient="agent", messageType=msg_format, content=user_text
                )))
                
                await websocket.send_json({"event": "agent_response_start"})
                
                full_ai_reply = ""
                async for chunk in ai_reply_stream:
                    full_ai_reply += chunk
                    await websocket.send_json({
                        "event": "agent_response_chunk",
                        "content": chunk
                    })
                
                await websocket.send_json({"event": "agent_response_end"})

                asyncio.create_task(add_message(Message(
                    sender="agent", recipient=session_id, messageType="text", content=full_ai_reply
                )))

            elif station_type == "question_answer":
                user_text = await process_qa(msg_format, content)
                
                asyncio.create_task(add_message(Message(
                    sender=session_id, 
                    recipient="system", 
                    messageType=msg_format, 
                    content=user_text
                )))
                
                await websocket.send_json({
                    "event": "system_ack",
                    "status": "success",
                    "message": "Đã ghi nhận câu trả lời",
                    "question_id": question_id
                })

    except WebSocketDisconnect:
        print(f"Client disconnected: Session {session_id} - Station {station_id}")
    except Exception as e:
        print(f"WebSocket Error: {e}")