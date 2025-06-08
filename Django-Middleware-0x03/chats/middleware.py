from datetime import datetime,timedelta
import logging
from django.http import HttpResponseForbidden
from collections import defaultdict


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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to hold message timestamps per IP
        self.message_log = defaultdict(list)

    def __call__(self, request):
        # Only limit POST requests (i.e., sending chat messages)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Filter out timestamps older than 1 minute
            self.message_log[ip] = [
                timestamp for timestamp in self.message_log[ip]
                if now - timestamp < timedelta(minutes=1)
            ]

            # Check if the number of messages exceeds 5
            if len(self.message_log[ip]) >= 5:
                return HttpResponseForbidden(
                    "You have exceeded the 5 messages per minute limit."
                )

            # Log the new message timestamp
            self.message_log[ip].append(now)

        # Proceed with the request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extract client IP address (supports proxy headers)"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
