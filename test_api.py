import pytest
from flask_rest import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
        
#Test case -Valid Email & -Valid Phone Number (Unique Too)
def test_identity(client):
    response = client.post("/identify", json = {"email" : "abracadabra@gmail.com", "phone_number" : "1222455565"})
    assert response.status_code == 200
    
#Test case -Valid Email & -No Phone Number (Ensures that system can process email without phone number)
def test_identity1(client):
    response = client.post("/identify", json = {"email" : "helloeveryone@yahoo.in", "phone_number" : ""})
    assert response.status_code == 200
    
#Test case -No Email & -Valid Phone Number (Ensures that system can process phone number without email)
def test_identity2(client):
    response = client.post("/identify", json = {"email" : "", "phone_number" : "9875550214"})
    assert response.status_code == 200

#Test case -Valid Email & -Valid Phone Number (Duplicate email but Unique phone number)
def test_identity3(client):
    response = client.post("/identify", json = {"email" : "helloeveryone@yahoo.in", "phone_number" : "6290548741"})
    assert response.status_code == 200

#Test case -Valid Email & -Valid Phone Number (Duplicate phone number but Unique email)
def test_identity4(client):
    response = client.post("/identify", json = {"email" : "kangaroo5@gmail.com", "phone_number" : "6290548741"})
    assert response.status_code == 200

#Test case -Valid Email & -Valid Phone Number (Duplicate phone number Duplicate email)
def test_identity5(client):
    response = client.post("/identify", json = {"email" : "kangaroo5@gmail.com", "phone_number" : "9875550214"})
    assert response.status_code == 200

#Test case -Valid Email & -Valid Phone Number (Duplicate phone number Duplicate email)
def test_identity6(client):
    response = client.post("/identify", json = {"email" : "kangaroo5@gmail.com", "phone_number" : "123456789"})
    assert response.status_code == 200

#Test case -No Email & -No Phone Number
def test_identity7(client):
    response = client.post("/identify", json = {"email" : "", "phone_number" : ""})
    assert response.status_code == 500












# def test_register(client):
#     response = client.post("/", json = {"email" : "kotafactory@gmail.com", "password": "kota@gmail9"})
#     assert response.status_code == 200
    
# def test_ref(client):
#     headers = {
#         "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTA2NzUyNCwianRpIjoiNDcxMWMxN2ItMjVjMS00YjVlLTg0MGUtNjE3NjgzMDQzNTUxIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJTb3VyeWFnaG9zaEBtb3RhcGFzZXBhcmVzaGFuLmNvbSIsIm5iZiI6MTc0MTA2NzUyNCwiY3NyZiI6ImY3NmQ3ZmRhLTc1N2MtNDg3Yy1hYWZjLTg4ZWE3ZDM1ZWJhMiIsImV4cCI6MTc0MzY1OTUyNH0.Emu8w_BQ9ODn4Ngm5bhvP4XLNHpnD48oinBQBi15F2Q"
#     }
#     response = client.post("/ref",headers=headers)
#     assert response.status_code == 200 
    
# def test_post(client):
#     headers = {
#         "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTA3NDQ3NiwianRpIjoiNmU4ZDU2MjYtYWQ1NC00YjJmLWJiZjgtYjU5NjkzMGMwMmZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlNvdXJ5YWdob3NoQG1vdGFwYXNlcGFyZXNoYW4uY29tIiwibmJmIjoxNzQxMDc0NDc2LCJjc3JmIjoiZjg2MzA0MzYtZWM1MS00OTdkLWExNTgtNWUzOGE0ODViZmEzIiwiZXhwIjoxNzQxMDc1MDc2fQ.ThO_jkP9S93BOD-4DJax6rJScuwjjj8MrNy_chplJ5A"
#     }
#     response = client.post("/task",json = {"title" : "Hey boudi", "desc" : "kamun acho"}, headers=headers)
#     assert response.status_code== 201
    
# def test_put(client):
#     headers = {
#         "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTA3MzYyMywianRpIjoiMTZhMjY5MTQtZjhhNi00MzVmLWJiMTctYzFhYTk2N2M0OTk5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlNvdXJ5YWdob3NoQG1vdGFwYXNlcGFyZXNoYW4uY29tIiwibmJmIjoxNzQxMDczNjIzLCJjc3JmIjoiMDg2NTBmNWEtMDZlMy00OGIzLTg5ODktOWJkMmJiZTE5YmYxIiwiZXhwIjoxNzQxMDc0MjIzfQ.WrkntuNAsHZYVzlwzjmHge_k9nE7GuYlcYjp_0KoccE"
#     }
#     response = client.put("/task/4",json = {"title" : "Hey bodi", "desc" : "kaun acho"}, headers=headers)
#     assert response.status_code== 201

# def test_delete(client):
#     headers = {
#         "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTA3MzYyMywianRpIjoiMTZhMjY5MTQtZjhhNi00MzVmLWJiMTctYzFhYTk2N2M0OTk5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlNvdXJ5YWdob3NoQG1vdGFwYXNlcGFyZXNoYW4uY29tIiwibmJmIjoxNzQxMDczNjIzLCJjc3JmIjoiMDg2NTBmNWEtMDZlMy00OGIzLTg5ODktOWJkMmJiZTE5YmYxIiwiZXhwIjoxNzQxMDc0MjIzfQ.WrkntuNAsHZYVzlwzjmHge_k9nE7GuYlcYjp_0KoccE"
#     }
#     response = client.delete("/task/3",headers=headers)
#     assert response.status_code ==200
    
# def test_get(client):
#     headers = {
#         "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTA3NDQ3NiwianRpIjoiNmU4ZDU2MjYtYWQ1NC00YjJmLWJiZjgtYjU5NjkzMGMwMmZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlNvdXJ5YWdob3NoQG1vdGFwYXNlcGFyZXNoYW4uY29tIiwibmJmIjoxNzQxMDc0NDc2LCJjc3JmIjoiZjg2MzA0MzYtZWM1MS00OTdkLWExNTgtNWUzOGE0ODViZmEzIiwiZXhwIjoxNzQxMDc1MDc2fQ.ThO_jkP9S93BOD-4DJax6rJScuwjjj8MrNy_chplJ5A"
#     }
#     response = client.get("/task",headers=headers)
#     assert response.status_code == 201
