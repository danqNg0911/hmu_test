import pytest


@pytest.mark.anyio
async def test_exam_manager(client_test):
    #======== Đăng ký/ Đăng nhập =====
    signup_resp = client.post("/user/signup", json={
        "email": "HMU@teacher.com",
        "name": "Nguyen Van A",
        "password": "123456",
        "role": "teacher",
        "username": "teacher001"
    })

    assert signup_resp.status_code in [200,201]

    login_resp = client.post("/user/login", json={
        "password": "123456",
        "username": "teacher001"
    })

    assert login_resp.status_code == 200

    headers = {}

    #======== Thao tác hồ sơ bệnh nhân =======
    patient_payload = {
        "version": "v1",
        "name": "Nguyễn Văn ABC",
        "age": 50,
        "gender": "Nam",
        "avt_url": "ava01",
        "voice_id": "voice01",
        "description": "Đau chân abc..."
    }

    create_patient_resp = await client_test.post("/patient-info/", json=patient_payload, headers=headers)
    assert create_patient_resp.status_code in [200, 201]
    
    patient_id = create_patient_resp.json().get("id")
    assert patient_id is not None

    get_patient_resp = await client_test.get(f"/patient-info/{patient_id}", headers=headers)
    assert get_patient_resp.status_code == 200

    update_patient_resp = await client_test.put(f"/patient-info/{patient_id}", json={
        "age": 46 #Đổi tuổi
    }, headers=headers)
    assert update_patient_resp.status_code == 200

    #======== Thao tác trạm thi ========
    station_payload = {
        "patient_info_id": patient_id,
        "name": "Trả lời câu khỏi y khoa",
        "type": "question_answer",
        "presented_findings": [
            {
            "section_id": "sect1",
            "type": "image",
            "title": "Ảnh chụp X-quang chân",
            "content": "Khớp ..."
            }
        ],
        "questions": [
            {
            "question_content": "Nêu 3 chẩn đoán ...",
            "expected_ans": "Vôi hóa, đau cấp, ...",
            "rubrics": [
                {
                "description": "trả lời đúng ...",
                "max_score": 6
                }
            ]
            }
        ],
        "time": 100
    }
    create_station_resp = await client_test.post(f"/patient-info/{patient_id}/station/", json=station_payload, headers=headers)
    assert create_station_resp.status_code in [200, 201]
    
    station_id = create_station_resp.json().get("station_id") or create_station_resp.json().get("id")
    assert station_id is not None

    update_station_resp = await client_test.put(f"/patient-info/{patient_id}/station/{station_id}", json={
        "time_limit": 300 # Đổi thời gian
    }, headers=headers)
    assert update_station_resp.status_code == 200