from .utils import *
from ..routers.admin import get_current_user, get_db
from fastapi import status
from ..models import ToDos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_auth(test_todo):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title':'learn fastapi','description':'need money','priority':1,
                                'complete':False,'owner_id':1, 'id':1}]

def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(ToDos).filter(ToDos.id ==1).first()
    assert model is None


def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail' : 'Todo Not Found !'}


