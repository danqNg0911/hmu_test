import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from app import app 
from beanie import PydanticObjectId

client = TestClient(app)

async def test_exam_flow(client: AsyncClient):
    #=== Đăng ký/ đăng nhập sinh viên
    signup_resp = client.post("/user/signup", json={
        "email": "abc@test.com",
        "name": "Nguyen Van Y",
        "password": "123456",
        "role": "student",
        "username": "OSCE_100"
    })

    assert signup_resp.status_code in [200,201]
    
    login_resp = client.post("/user/login", json={
        "password": "123456",
        "username": "OSCE_100"
    })

    assert login_resp.status_code == 200

    user_id = signup_resp.json().get("id")
    token = login_resp.json().get("access_token")
    headers = {"Authorization" : f"Bearer {token}"}

    #======= Bắt đầu phiên thi
    start_session_payload = {
        "user_id": user_id, 
        "total_patients": 1
    }
    session_resp = client.post("/session/", json=start_session_payload, headers=headers)
    assert session_resp.status_code in [200, 201]
    
    session_data = session_resp.json()
    session_id = session_data["id"]
    assert session_data["status"] == "IN_PROGRESS"

    #===== lấy đề bài và thi
    current_station_resp = client.get(f"/session/{session_id}/station", headers=headers)
    assert current_station_resp.status_code == 200
    
    station_data = current_station_resp.json()
    assert "station" in station_data
    # Lấy ID của trạm hiện tại (nếu cần gửi kèm khi submit)
    current_station_id = station_data["station"]["_id"]

    #===== Nộp bài 
    submission_payload = {
        # Giả định body nộp bài của bạn như sau
        "answers": [
            {
                "question_id": "abc-123", # Bạn có thể bỏ qua nếu chưa validate chặt
                "answer_text": "Bệnh nhân bị viêm ruột thừa"
            }
        ]
    }
    submit_resp = client.post(f"/session/{session_id}/station/submission", json=submission_payload, headers=headers)
    assert submit_resp.status_code in [200, 201]
    
    # Ở đây submit_resp có thể trả về thông tin của trạm MỚI (nếu còn trạm), 
    # hoặc trả về status COMPLETED nếu đã hết trạm.

    # ==========================================
    # Bước 5: Xem lại kết quả (Get Result)
    # ==========================================
    # Giả định bài thi đã kết thúc (COMPLETED), gọi API lấy bảng điểm
    result_resp = client.get(f"/result/exam/{session_id}", headers=headers)
    
    # Nếu đang thi dở thì có thể trả về 400 hoặc 404, tùy logic bạn set. 
    # Giả định ở đây là success 200.
    if result_resp.status_code == 200:
        result_data = result_resp.json()
        assert "session_id" in result_data
        assert "stations_summary" in result_data
        assert type(result_data["stations_summary"]) == list