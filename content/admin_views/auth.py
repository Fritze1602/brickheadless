"""Authentication views for the BricksCMS admin interface."""

from django.contrib.auth.views import LoginView


class BricksCMSLoginView(LoginView):
    """Custom login view for the BricksCMS UI (not Django admin)."""

    template_name = "bricks_admin/login.html"
