from django.middleware.common import CommonMiddleware

class CustomCommonMiddleware(CommonMiddleware):
    def process_response(self, request, response):
        if request.method == "POST" and response.status_code == 301:  # Handle POST redirects
            return response
        return super().process_response(request, response)
