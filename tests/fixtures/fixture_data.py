import pytest
import tempfile


@pytest.fixture
def post(admin):
    from support_api.models import Post
    return Post.objects.create(text='Тестовый пост 1', author=admin,)


@pytest.fixture
def comment_1_post(post, admin):
    from support_api.models import Comment
    return Comment.objects.create(author=admin, post=post, text='Коммент 1')


@pytest.fixture
def comment_2_post(post, another_user):
    from support_api.models import Comment
    return Comment.objects.create(author=another_user, post=post, text='Коммент 2')


@pytest.fixture
def another_post(admin):
    from support_api.models import Post
    return Post.objects.create(text='Тестовый пост 2', author=admin)


@pytest.fixture
def comment_1_another_post(another_post, another_user):
    from support_api.models import Comment
    return Comment.objects.create(author=another_user, post=another_post, text='Коммент 12')
