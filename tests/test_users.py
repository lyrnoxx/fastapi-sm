from app import schemas
from .database import client, session
import pytest

@pytest.fixture
def test_user(client):
    user_data={"email":"random12334@gmail.com","password":"password123"}
    res=client.post('/users/',json=user_data)
    assert res.status_code == 201
    

def test_create_user(client):
    res=client.post("/users/",json={"email":"random12334@gmail.com","password":"password123"})
    new_user=schemas.UserOut(**res.json())
    assert new_user.email=="random12334@gmail.com"
    assert res.status_code ==201

def test_user_login(client):
    res=client.post("/login",data={"username":"random12334@gmail.com","password":"password123"})
    assert res.status_code ==200