from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


from core.fixtures.user import user


class TestUserViewSet:

    endpoint = '/api/user/'
    client = APIClient()

    def test_list(self, user):
        self.client.force_authenticate(user=user)
        response: Response = self.client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_retrieve(self, user):
        self.client.force_authenticate(user=user)
        response: Response = self.client.get(self.endpoint + str(user.public_id) + '/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user.public_id.hex
        assert response.data['username'] == user.username
        assert response.data['email'] == user.email

    def test_create(self, user):
        self.client.force_authenticate(user=user)

        data = {}

        response: Response = self.client.post(self.endpoint, data)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update(self, user):
        self.client.force_authenticate(user=user)

        data = {
            'username': 'NewName'
        }

        response: Response = self.client.patch(self.endpoint + str(user.public_id) + '/', data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == data['username']
