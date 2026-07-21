import pytest

@pytest.mark.django_db
class TestApiDocs:
    def test_schema_available(self, client) -> None:
        assert client.get('/api/schema/').status_code == 200

    def test_swagger_ui_available(self, client) -> None:
        response = client.get('/api/docs/')
        assert response.status_code == 200
        assert b'swagger' in response.content.lower()