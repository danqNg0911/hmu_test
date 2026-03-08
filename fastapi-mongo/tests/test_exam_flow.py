import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from app import app 
from beanie import PydanticObjectId

client = TestClient(app)

async def test_exam_flow(client: AsyncClient):
    test_user_id = str(PydanticObjectId())
    total_stations_test = 2

    response = client.post("/session", json={"user_id": test_user_id, "total_stations": total_stations_test})
    assert response.status_code == 201
    session_data = response.json()

    assert session_data["status"] == "IN_PROGRESS"
    assert session_data["current_station"] == 1
    session_id = session_data["id"]

    print(f"\n Đã tạo phiên thi thành công: {session_id}")

    for current_step in range(total_stations_test):
        # Hiển thị đề
        print(f"\n--- Đang vào trạm số {current_step + 1}/{total_stations_test} ---")
        response = client.get(f"/session/{session_id}/station")
        assert response.status_code == 200
        station_data = response.json()

        assert station_data["current_station"] == current_step + 1
        print(f"\n Đã lấy thông tin trạm hiện tại: {station_data}")

        # Kết nối WebSocket để thi trạm
        station_id = station_data["station"]["_id"]

        with client.websocket_connect(f"/ws/exam/{session_id}/{station_id}?token=mock_token") as ws:
            ws.send_json({"type": "text", "content": "Chào bác sĩ"})
            while True:
                resp = ws.receive_json()
                if resp.get("event") == "agent_response_end" or resp.get("event") == "system_ack":
                    break
        print(f"    -> Đã hoàn thành bài thi tại trạm {current_step + 1}")

        # Nộp bài và chuyển trạm (hoặc hoàn thành kỳ thi nếu đây là trạm cuối)
        response = client.post(f"/session/{session_id}/station/submission")
        assert response.status_code == 200
        submission_data = response.json()
        if current_step < total_stations_test - 1:
            assert submission_data["current_station"] == current_step + 2
            print(f"\n Đã nộp trạm hiện tại và chuyển trạm tiếp theo: {submission_data}")
        else:
            # cuối cùng, nên nhận trạng thái COMPLETED
            assert submission_data["status"] == "COMPLETED"
            print(f"\n Đã hoàn tất kỳ thi: {submission_data}")

    # Xem lại kết quả bài thi
    response = client.get(f"/exam-result/{session_id}")
    assert response.status_code == 200
    exam_results = response.json()
    assert isinstance(exam_results, list)
    assert len(exam_results) == 1
    result = exam_results[0]
    assert result["total_score"] == 100
    assert result.get("overall_feedback") is None

    # Xem lại kết quả 1 trạm chi tiết