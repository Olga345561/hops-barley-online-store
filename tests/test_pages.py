import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_guides_page_renders_with_base_layout(client) -> None:
    response = client.get(reverse("guides"))
    assert response.status_code == 200
    content = response.content.decode()
    assert "Hop & Barley" in content          # текст логотипу заголовка
    assert "Guides & Recipes" in content      # сторінка h1
    assert "Sign in" in content               # блок заголовка гостьового сервера