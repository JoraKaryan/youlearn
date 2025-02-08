from django.shortcuts import redirect
from django.urls import reverse

class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow admins to access everything
        if hasattr(request.user, "is_admin") and request.user.is_admin():
            return self.get_response(request)

        # Define restricted URLs and their required roles
        restricted_urls = {
            '/admin/': 'admin',  # Only admins can access
            '/tutors/': 'tutor',  # Only tutors can access
            '/students/': 'student',  # Only students can access
        }

        # Check if the current URL is restricted
        for url, required_role in restricted_urls.items():
            if request.path.startswith(url) and not getattr(request.user, f'is_{required_role}', lambda: False)():
                return redirect(reverse('no_permission'))

        response = self.get_response(request)
        return response
