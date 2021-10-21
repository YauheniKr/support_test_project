import pytest
from support_api.models import Comment


class TestCommentAPI:

    @pytest.mark.django_db(transaction=True)
    def test_comments_not_found(self, user_client, post):
        response = user_client.get(f'/api/v1/posts/{post.id}/comments/')

        assert response.status_code != 404, \
            'Page `/api/v1/posts/{post.id}/comments/` not found, check *urls.py*'

    @pytest.mark.django_db(transaction=True)
    def test_comments_get(self, user_client, post, comment_1_post, comment_2_post, comment_1_another_post):
        response = user_client.get(f'/api/v1/posts/{post.id}/comments/')

        assert response.status_code == 200, \
            'GET request `/api/v1/posts/{post.id}/comments/` ' \
            'with authorization token not return status code 200'

    @pytest.mark.django_db(transaction=True)
    def test_comments_create(self, user_client, post, admin, another_user):
        comments_count = Comment.objects.count()

        data = {}
        response = user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        assert response.status_code == 400, \
            'POST request `/api/v1/posts/{post.id}/comments/` with incorrect data not return status 400'

        data = {'author': another_user.id, 'text': 'Новый коммент 1233', 'post': post.id}
        response = user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        assert response.status_code == 201, \
            'POST request `/api/v1/posts/{post.id}/comments/` with correct data return status 201'

        test_data = response.json()
        msg_error = 'POST request `/api/v1/posts/{post.id}/comments/` return dict with new comment'
        assert type(test_data) == dict, msg_error
        assert test_data.get('text') == data['text'], msg_error

        assert test_data.get('author') == admin.username, \
            'POST request `/api/v1/posts/{post.id}/comments/` comment not created from auth user'
        assert comments_count + 1 == Comment.objects.count(), \
            'POST request `/api/v1/posts/{post.id}/comments/` comment not created'

    @pytest.mark.django_db(transaction=True)
    def test_post_get_current(self, user_client, post, comment_1_post, admin):
        response = user_client.get(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/')

        assert response.status_code == 200, \
            'Page `/api/v1/posts/{post.id}/comments/{comment.id}/` not found'

    @pytest.mark.django_db(transaction=True)
    def test_post_patch_current(self, user_client, post, comment_1_post, comment_2_post):
        response = user_client.patch(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/',
                                     data={'text': 'Comments text changed'})

        assert response.status_code == 200, \
            'PATCH request `/api/v1/posts/{post.id}/comments/{comment.id}/` not return status 200'

        test_comment = Comment.objects.filter(id=comment_1_post.id).first()

        assert test_comment.text == 'Comments text changed', \
            'PATCH request `/api/v1/posts/{id}/` comments changed'

        response = user_client.patch(f'/api/v1/posts/{post.id}/comments/{comment_2_post.id}/',
                                     data={'text': 'Comments text changed'})

        assert response.status_code == 403, \
            'PATCH request `/api/v1/posts/{post.id}/comments/{comment.id}/` ' \
            'not own comments returns status code 403'

    @pytest.mark.django_db(transaction=True)
    def test_post_delete_current(self, user_client, post, comment_1_post, comment_2_post):
        response = user_client.delete(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/')

        assert response.status_code == 204, \
            'DELETE request `/api/v1/posts/{post.id}/comments/{comment.id}/` not return status 204'

        test_comment = Comment.objects.filter(id=post.id).first()

        assert not test_comment, \
            'DELETE request `/api/v1/posts/{post.id}/comments/{comment.id}/` not delete comment'

        response = user_client.delete(f'/api/v1/posts/{post.id}/comments/{comment_2_post.id}/')

        assert response.status_code == 403, \
            'DELETE request `/api/v1/posts/{post.id}/comments/{comment.id}/` ' \
            'for not own comments returns status 403'

    def test_status_comment(self, another_user, user_client, post, comment_1_post):
        data = {'author': another_user.id, 'text': 'New comment 1233', 'post': post.id}
        user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        response = user_client.get(f'/api/v1/posts/{post.id}/')
        assert response.json().get('status') == 'In progress', 'Post status not changed to In progress'

    def test_status_comment_close(self, another_user, user_client, post, comment_1_post):
        data = {'author': another_user.id, 'text': 'New comment 1233', 'post': post.id}
        user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        data_status = {'status': 'Close'}
        user_client.patch(f'/api/v1/posts/{post.id}/', data=data_status)
        user_client.get(f'/api/v1/posts/{post.id}/')
        response = user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        assert response.status_code == 400, 'Cant add comment to post with close status'
