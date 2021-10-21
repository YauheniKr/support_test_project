import pytest
from django.conf import settings


class TestAuthAPI:

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, client, admin):
        response = client.post('/auth/jwt/create/',
                               data={'username': admin.username, 'password': '1234567'})

        assert response.status_code != 404, \
            'Page `auth/jwt/create/` not found'

        assert response.status_code == 200, \
            'Page `auth/jwt/create/` works incorrect'

        auth_data = response.json()
        assert 'access' in auth_data and auth_data.get('access'), 'POST request `/auth/jwt/create/` not return токен'
