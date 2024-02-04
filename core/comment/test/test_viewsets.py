from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from core.fixtures.user import user
from core.fixtures.post import post
from core.fixtures.comment import comment


class TestCommentViewSet:

    endpoint = '/api/post/'
    client = APIClient()

    def test_list(self, user, post, comment):
        self.client.force_authenticate(user=user)
        response: Response = self.client.get(self.endpoint + str(post.public_id) + '/comment/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_retrieve(self, user, post, comment):
        self.client.force_authenticate(user=user)
        response: Response = self.client.get(self.endpoint + str(post.public_id) + '/comment/' + str(comment.public_id) + '/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == comment.public_id.hex
        assert response.data['body'] == comment.body
        assert response.data['author']['id'] == comment.author.public_id.hex

    def test_create(self, user, post):
        self.client.force_authenticate(user=user)
        data = {
            'body': 'Test Comment Body',
            'author': user.public_id.hex,
            'post': post.public_id.hex
        }
        response: Response = self.client.post(self.endpoint + str(post.public_id) + '/comment/', data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['body'] == data['body']
        assert response.data['author']['id'] == user.public_id.hex

    def test_update(self, user, post, comment):
        self.client.force_authenticate(user=user)
        data= {
            'body':  'Test Comment Body',
            'author':user.public_id.hex,
            'post': post.public_id.hex
        }
        response: Response = self.client.put(self.endpoint + str(post.public_id) + '/comment/' + str(comment.public_id) + '/', data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['body'] == data['body']

    def test_delete(self, user, post, comment):
        self.client.force_authenticate(user=user)
        response: Response = self.client.delete(self.endpoint + str(post.public_id) + '/comment/' + str(comment.public_id) + '/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
