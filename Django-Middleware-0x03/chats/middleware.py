from datetime import datetime
import logging
from django.http import HttpResponseForbidden

# Configure logger
logger = logging.getLogger('request_logger')
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'AnonymousUser'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server time (24-hour format)
        current_hour = datetime.now().hour

        # Allow access only between 18:00 (6 PM) and 21:00 (9 PM)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to the chat is only allowed between 6 PM and 9 PM.")

        # Proceed with request if within allowed hours
        response = self.get_response(request)
        return response
