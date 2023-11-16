# TODO доработать
import sys

sys.path.append(".")

from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_success_form_one():
    response = client.post(
        "/get_form",
        data={'email': "test@ya.ru"},
    )
    data = response.json()
    assert data.get("name") == "Order Form"
    assert response.status_code == 200


def test_success_form_two():
    response = client.post(
        "/get_form",
        data={
            "lead_email": "tester@ya.ru",
            "user_phone": '+7 999 888 77 66'
        },
    )

    data = response.json()
    assert data.get("name") == "MyForm"
    assert response.status_code == 200


def test_fail_form_one():
    prediction_response = {
        "f_name11": "date",
        "f_name22": 'text'
    }
    response = client.post(
        "/get_form",
        data={
            "f_name11": "15.11.2023",
            "f_name22": 'text'
        },
    )
    data = response.json()
    assert data == prediction_response
    assert response.status_code == 200


def test_fail_form_two():
    prediction_response = {
        "f_name_phone": "phone",
        "f_name_email": 'email',
        "wrong_phone": "text",
    }
    response = client.post(
        "/get_form",
        data={
            "f_name_phone": "+7 999 666 44 55",
            "f_name_email": 'test@ya.ru',
            "wrong_phone": "+79996664455"
        },
    )
    data = response.json()
    assert data == prediction_response
    assert response.status_code == 200
