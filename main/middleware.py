from django.shortcuts import redirect
from django.urls import reverse
import time
import logging

# Set up logger
logger = logging.getLogger('api_requests')

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
        
        # Add this line to return the response for non-restricted URLs
        return self.get_response(request)

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Record the start time
        start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Calculate request processing time
        duration = time.time() - start_time
        
        # Log the request details
        log_data = {
            'path': request.path,
            'method': request.method,
            'status_code': response.status_code,
            'duration': f"{duration:.2f}s",
            'user': request.user.username if request.user.is_authenticated else 'Anonymous',
        }
        
        # Add query parameters if any (excluding sensitive data)
        if request.GET:
            log_data['query_params'] = dict(request.GET)
            
        # Log the data
        logger.info(f"API Request: {log_data}")
        
        return response
