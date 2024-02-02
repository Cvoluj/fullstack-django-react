import pytest
from core.user.models import User

data_user = {
    'username': 'test_user',
    'email': 'test@gmail.com',
    'first_name': 'Test',
    'last_name': 'User',
    'password': 'test_password'
}

data_superuser = {
    'username': 'test_superuser',
    'email': 'supermail@gmail.com',
    'first_name': 'Test',
    'last_name': 'superuser',
    'password': 'super_password'
}


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(**data_user)
    assert user.username == data_user['username']
    assert user.email == data_user['email']
    assert user.first_name == data_user['first_name']
    assert user.last_name == data_user['last_name']
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_superuser():
    superuser = User.objects.create_superuser(**data_superuser)
    assert superuser.username == data_superuser['username']
    assert superuser.email == data_superuser['email']
    assert superuser.first_name == data_superuser['first_name']
    assert superuser.last_name == data_superuser['last_name']
    assert superuser.is_superuser is True
