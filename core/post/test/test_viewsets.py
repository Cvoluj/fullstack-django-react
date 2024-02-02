from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.test import force_authenticate

from core.fixtures.user import user
from core.fixtures.post import post


class TestPostViewSet:

    endpoint = '/api/post/'
    client = APIClient()

    def test_list(self, user, post):
        response: Response = self.client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_retrieve(self, client, user, post):

        response: Response = client.get(self.endpoint + str(post.public_id) + '/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == post.public_id.hex
        assert response.data['body'] == post.body
        assert response.data['author']['id'] == post.author.public_id.hex

    def test_create(self, user):
        self.client.force_authenticate(user=user)
        data = {
            'body': 'Test Post Body',
            'author': user.public_id.hex
        }
        response = self.client.post(self.endpoint, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['body'] == data['body']
        assert response.data['author']['id'] == user.public_id.hex

    def test_update(self, user, post):
        self.client.force_authenticate(user=user)
        data = {
            'body': 'Test Post Body',
            'author': user.public_id.hex
        }
        response: Response = self.client.put(self.endpoint + str(post.public_id) + '/', data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['body'] == data['body']

    def test_delete(self, user, post):
        self.client.force_authenticate(user=user)
        response: Response = self.client.delete(self.endpoint + str(post.public_id) + '/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
