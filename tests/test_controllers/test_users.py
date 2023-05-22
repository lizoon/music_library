from hamcrest import *

def test_main(client):
    response = client.get('/')
    assert response.status_code == 200
    assert_that(response.data.decode(), contains_string('Main app page'))
    assert_that(response.data.decode(), contains_string("<!DOCTYPE html>"))

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

