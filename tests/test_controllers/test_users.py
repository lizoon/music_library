import pytest
from flask import url_for, request
from hamcrest import *
from app.models.user import User, Role

def test_main(client):
    response = client.get('/')
    assert response.status_code == 200
    assert_that(response.data.decode(), contains_string('Main app page'))
    assert_that(response.data.decode(), contains_string("<!DOCTYPE html>"))
#
#
# def test_invalid_signup(client, session, user_datastore):
#     get_response = client.get('/signup')
#     assert get_response.status_code == 200
#
#
#
#     post_response = client.post('/signup', data={
#         'email': 'Test@gmail.com',
#         'nickname': 'TestNickname',
#         'password': 'TestPassword'
#     })
#     assert post_response.status_code == 302
#     assert post_response.location == 'http://localhost/login'
#     login_response = client.get(post_response.location)
#     assert login_response.status_code == 200
#     assert 'Login' in login_response.get_data(as_text=True)
#

def test_login(client, session, user_datastore):
    user = user_datastore.create_user(password='TestPassword', email='Test@gmail.com', nickname='TestNickname', active=True)
    session.commit()

    response = client.post('/login', data={'nickname': 'TestNickname', 'password': 'TestPassword'}, follow_redirects=True)
    assert response.status_code == 200
    assert 'Log in' in response.data.decode()

    assert user.is_authenticated
    assert user.email == 'Test@gmail.com'
    assert user.nickname == 'TestNickname'
    assert user.password == 'TestPassword'




# def test_homepage(client, session):
#     user = User(password='testtest', email='test2@gmail.com', nickname='test2', active=True)
#     session.add(user)
#     session.commit()
#
#     test_login(client)
#     response = client.get('/homepage')
#     assert response.status_code == 200
#     assert user.nickname in response.get_data(as_text=True)

    # user = User.query.first()
    # login_user(client)
    # response = client.get('/homepage')
    # assert_that(response.status_code, equal_to(200))
    # assert_that(response.data.decode(), contains_string(user.nickname))


