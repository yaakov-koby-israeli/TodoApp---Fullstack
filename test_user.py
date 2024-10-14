from .utils import *
from ..routers.users import get_current_user,get_db
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ['username'] == 'koby'
    assert response.json()['email'] == 'koby@gmai.com'
    assert response.json()['first_name'] == 'koby'
    assert response.json()['last_name'] == 'israeli'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '0584176451'


def test_change_password_success(test_user):
    response = client.put("/user/password", json={"password" : "testpass",
                                                  "new_password": "newtestpass"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_curr_pass(test_user):
    response = client.put("/user/password", json={"password": "wrong_pass",
                                                  "new_password": "newtestpass"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail' : 'Error on password change'}

def test_change_phone_number_success(test_user):
    response = client.put("/user/phone_number/222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT




